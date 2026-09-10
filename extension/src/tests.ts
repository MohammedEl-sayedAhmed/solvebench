// The test panel. Builds a tree of solutions from `run.py --stats --json` and
// runs them with `run.py --json`.

import * as vscode from 'vscode';
import { startDebugging } from './debug';
import { SolutionJson } from './model';
import { RunnerError, runPy } from './runner';

/** Same normalising rule as norm() in run.py, so two_sum and TwoSum match. */
export function normalise(name: string): string {
    return name.toLowerCase().replace(/[^a-z0-9]/g, '');
}

/** two_sum -> Two Sum, TwoSum -> Two Sum. One label for both languages. */
export function problemTitle(name: string): string {
    const spaced = name
        .replace(/^_+/, '')
        .replace(/([a-z0-9])([A-Z])/g, '$1 $2')
        .replace(/[_-]+/g, ' ')
        .trim();
    return spaced.replace(/\b\w/g, (c) => c.toUpperCase());
}

export class SolutionTests implements vscode.Disposable {
    private readonly controller: vscode.TestController;
    /** Leaf test item id (the repo-relative path) -> its solution. */
    private readonly byPath = new Map<string, SolutionJson>();
    private readonly disposables: vscode.Disposable[] = [];

    constructor(private readonly root: vscode.Uri) {
        this.controller = vscode.tests.createTestController('solvebench', 'solvebench');
        this.disposables.push(this.controller);

        this.controller.refreshHandler = async () => {
            await this.refresh();
        };

        this.controller.createRunProfile(
            'Run',
            vscode.TestRunProfileKind.Run,
            (request, token) => this.run(request, token),
            true
        );
        this.controller.createRunProfile(
            'Debug',
            vscode.TestRunProfileKind.Debug,
            (request) => this.debug(request),
            false
        );
    }

    dispose(): void {
        for (const d of this.disposables) {
            d.dispose();
        }
    }

    /** Rebuild the tree from run.py. */
    async refresh(): Promise<void> {
        let solutions: SolutionJson[];
        try {
            const payload = await runPy(this.root, { statsOnly: true });
            solutions = payload.solutions;
        } catch (err) {
            if (err instanceof RunnerError) {
                void vscode.window.showErrorMessage(`solvebench: ${err.message}`);
            }
            return;
        }

        this.byPath.clear();
        this.controller.items.replace([]);

        for (const sol of solutions) {
            this.byPath.set(sol.path, sol);
            this.place(sol);
        }
    }

    /** Put one solution in the tree: platform -> group -> problem -> language. */
    private place(sol: SolutionJson): void {
        const platform = this.child(this.controller.items, `platform:${sol.platform}`, sol.platform);

        // Platforms like codewars have no group, so that level is skipped.
        let parent = platform;
        if (sol.group) {
            parent = this.child(
                platform.children,
                `group:${sol.platform}/${sol.group}`,
                sol.group
            );
        }

        const problemKey = `problem:${sol.platform}/${sol.group}/${normalise(sol.name)}`;
        const problem = this.child(parent.children, problemKey, problemTitle(sol.name));

        // The leaf is one language of one problem. Its id is the path run.py
        // reports, which is also what we send back as a filter.
        const leaf = this.controller.createTestItem(
            sol.path,
            sol.lang,
            vscode.Uri.joinPath(this.root, sol.path)
        );
        problem.children.add(leaf);
    }

    private child(
        collection: vscode.TestItemCollection,
        id: string,
        label: string
    ): vscode.TestItem {
        const existing = collection.get(id);
        if (existing) {
            return existing;
        }
        const created = this.controller.createTestItem(id, label);
        collection.add(created);
        return created;
    }

    /** Every leaf under an item, or the item itself if it is a leaf. */
    private leaves(item: vscode.TestItem, into: vscode.TestItem[]): void {
        if (item.children.size === 0) {
            into.push(item);
            return;
        }
        item.children.forEach((c) => this.leaves(c, into));
    }

    /** The leaves the request asks for, minus anything it excludes. */
    private requested(request: vscode.TestRunRequest): vscode.TestItem[] {
        const picked: vscode.TestItem[] = [];
        if (request.include) {
            for (const item of request.include) {
                this.leaves(item, picked);
            }
        } else {
            this.controller.items.forEach((item) => this.leaves(item, picked));
        }

        const excluded = new Set<string>();
        for (const item of request.exclude ?? []) {
            const out: vscode.TestItem[] = [];
            this.leaves(item, out);
            out.forEach((i) => excluded.add(i.id));
        }
        return picked.filter((i) => !excluded.has(i.id) && this.byPath.has(i.id));
    }

    private async run(
        request: vscode.TestRunRequest,
        token: vscode.CancellationToken
    ): Promise<void> {
        const items = this.requested(request);
        if (items.length === 0) {
            return;
        }

        const testRun = this.controller.createTestRun(request);
        for (const item of items) {
            testRun.enqueued(item);
        }

        // No include set means the whole tree, and run.py is faster with no
        // filters at all than with 42 of them.
        const everything = !request.include && !request.exclude?.length;
        const filters = everything ? [] : items.map((i) => i.id);

        try {
            for (const item of items) {
                testRun.started(item);
            }
            const payload = await runPy(this.root, { filters, token });

            const results = new Map(payload.solutions.map((s) => [s.path, s]));
            for (const item of items) {
                const result = results.get(item.id);
                if (!result || !result.status) {
                    // run.py did not report on it, so we do not guess.
                    testRun.skipped(item);
                    continue;
                }
                const ms = (result.seconds ?? 0) * 1000;
                if (result.status === 'pass') {
                    testRun.passed(item, ms);
                } else {
                    const message = new vscode.TestMessage(
                        result.output?.trim() || 'the solution exited non-zero'
                    );
                    if (item.uri) {
                        message.location = new vscode.Location(
                            item.uri,
                            new vscode.Position(0, 0)
                        );
                    }
                    testRun.failed(item, message, ms);
                }
                if (result.output) {
                    testRun.appendOutput(
                        `${result.path}\r\n${result.output.replace(/\n/g, '\r\n')}\r\n\r\n`
                    );
                }
            }
        } catch (err) {
            const message = err instanceof RunnerError ? err.message : String(err);
            testRun.appendOutput(`solvebench: ${message}\r\n`);
            for (const item of items) {
                testRun.errored(item, new vscode.TestMessage(message));
            }
        } finally {
            testRun.end();
        }
    }

    /**
     * Debugging is one solution at a time. Debugging several at once would just
     * fight over the debug console, so we ask for one instead of guessing.
     */
    private async debug(request: vscode.TestRunRequest): Promise<void> {
        const items = this.requested(request);
        if (items.length === 0) {
            return;
        }
        if (items.length > 1) {
            void vscode.window.showWarningMessage(
                'solvebench: pick one solution to debug, not several.'
            );
            return;
        }
        const sol = this.byPath.get(items[0].id);
        if (!sol) {
            return;
        }
        await startDebugging(
            {
                language: sol.language,
                relPath: sol.path,
                fsPath: vscode.Uri.joinPath(this.root, sol.path).fsPath,
            },
            this.root
        );
    }
}
