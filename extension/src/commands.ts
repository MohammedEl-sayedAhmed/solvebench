// The commands in the command palette. Each one calls a script that already
// exists in the repo.

import * as vscode from 'vscode';
import { ComplexityView, measure } from './complexity';
import { problemId, solutionRef, startDebugging } from './debug';
import { ProcessError, spawnCollect } from './exec';
import { requirePython } from './python';
import { sendToTerminal } from './terminal';
import { SolutionTests } from './tests';

const LANGUAGE_CHOICES: { label: string; description: string; flag: string }[] = [
    { label: 'Python', description: 'python/', flag: 'py' },
    { label: 'Java', description: 'java/', flag: 'java' },
    { label: 'C++', description: 'cpp/', flag: 'cpp' },
    { label: 'JavaScript', description: 'javascript/', flag: 'js' },
    { label: 'Go', description: 'go/', flag: 'go' },
    { label: 'Rust', description: 'rust/', flag: 'rust' },
];

/** How to start a run: in a container, or with the local Python. */
async function runnerCommand(root: vscode.Uri): Promise<string[] | undefined> {
    const inContainer = vscode.workspace
        .getConfiguration('solvebench')
        .get<boolean>('runInContainer', false);

    if (inContainer) {
        return process.platform === 'win32' ? ['.\\run.ps1'] : ['./run.sh'];
    }
    const python = await requirePython(root);
    return python ? [python, 'run.py'] : undefined;
}

/**
 * The solution to act on: the uri a CodeLens passed, else the open file.
 * Complains if neither is a solution.
 */
function currentSolution(root: vscode.Uri, uri?: vscode.Uri) {
    const target = uri ?? vscode.window.activeTextEditor?.document.uri;
    if (!target) {
        void vscode.window.showWarningMessage('solvebench: no file is open.');
        return undefined;
    }
    const ref = solutionRef(target, root);
    if (!ref) {
        void vscode.window.showWarningMessage(
            'solvebench: this file is not a solution. Open one under python/, java/, cpp/, javascript/, go/ or rust/.'
        );
        return undefined;
    }
    return ref;
}

export function registerCommands(
    context: vscode.ExtensionContext,
    root: vscode.Uri,
    tests: SolutionTests
): void {
    const complexityView = new ComplexityView();
    context.subscriptions.push(complexityView);

    const register = (id: string, run: (...args: any[]) => any) => {
        context.subscriptions.push(vscode.commands.registerCommand(id, run));
    };

    register('solvebench.refreshTests', () => tests.refresh());

    register('solvebench.runAll', async () => {
        const command = await runnerCommand(root);
        if (command) {
            sendToTerminal(root, command);
        }
    });

    register('solvebench.stats', async () => {
        const command = await runnerCommand(root);
        if (command) {
            sendToTerminal(root, [...command, '--stats']);
        }
    });

    register('solvebench.runCurrent', async (uri?: vscode.Uri) => {
        const ref = currentSolution(root, uri);
        if (!ref) {
            return;
        }
        const command = await runnerCommand(root);
        if (command) {
            // problemId, not the folder: the folder would run every problem of
            // that difficulty, not this one in each language.
            sendToTerminal(root, [...command, problemId(ref)]);
        }
    });

    register('solvebench.debugCurrent', async (uri?: vscode.Uri) => {
        const ref = currentSolution(root, uri);
        if (ref) {
            await startDebugging(ref, root);
        }
    });

    register('solvebench.complexity', async (uri?: vscode.Uri) => {
        const ref = currentSolution(root, uri);
        if (!ref) {
            return;
        }
        if (ref.language !== 'python' && ref.language !== 'java') {
            void vscode.window.showWarningMessage(
                'solvebench: complexity.py measures Python and Java solutions only.'
            );
            return;
        }
        const result = await measure(root, ref);
        if (result) {
            complexityView.show(result);
        }
    });

    register('solvebench.newSolution', () => newSolution(root, tests));
}

/**
 * Ask for a language and a URL or path, then call new.py.
 *
 * This one does not use the terminal: new.py prints the file it made, so we
 * read that and open it.
 */
async function newSolution(root: vscode.Uri, tests: SolutionTests): Promise<void> {
    const language = await vscode.window.showQuickPick(LANGUAGE_CHOICES, {
        title: 'New solution: which language?',
        matchOnDescription: true,
    });
    if (!language) {
        return;
    }

    const target = await vscode.window.showInputBox({
        title: 'New solution: problem URL or path',
        prompt: 'A problem URL, or platform/group/name',
        placeHolder: 'https://leetcode.com/problems/two-sum/  or  leetcode/easy/two_sum',
        validateInput: (value) => (value.trim() ? undefined : 'Enter a URL or a path'),
    });
    if (!target) {
        return;
    }

    const python = await requirePython(root);
    if (!python) {
        return;
    }

    const args = ['new.py', target.trim(), '--lang', language.flag];
    const result = await vscode.window.withProgress(
        { location: vscode.ProgressLocation.Notification, title: 'solvebench: creating solution' },
        async () => {
            try {
                return await spawnCollect(python, args, root.fsPath);
            } catch (err) {
                const message = err instanceof ProcessError ? err.message : String(err);
                void vscode.window.showErrorMessage(`solvebench: ${message}`);
                return undefined;
            }
        }
    );
    if (!result) {
        return;
    }

    if (result.code !== 0) {
        // new.py explains itself well (bad URL, file already there, no
        // difficulty), so show what it said rather than a generic message.
        const said = (result.stderr.trim() || result.stdout.trim()).split('\n').pop();
        void vscode.window.showErrorMessage(`solvebench: ${said || 'new.py failed'}`);
        return;
    }

    // new.py prints "Created <path relative to the repo>".
    const created = /^Created (.+)$/m.exec(result.stdout);
    if (created) {
        const file = vscode.Uri.joinPath(root, created[1].trim());
        const doc = await vscode.workspace.openTextDocument(file);
        await vscode.window.showTextDocument(doc);
    }
    await tests.refresh();
}
