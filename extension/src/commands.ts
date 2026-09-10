// The commands in the command palette. Each one calls a script that already
// exists in the repo.

import * as path from 'path';
import * as vscode from 'vscode';
import { solutionRef, startDebugging } from './debug';
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

/** The open file, if it is a solution. Complains if it is not. */
function currentSolution(root: vscode.Uri) {
    const editor = vscode.window.activeTextEditor;
    if (!editor) {
        void vscode.window.showWarningMessage('solvebench: no file is open.');
        return undefined;
    }
    const ref = solutionRef(editor.document.uri, root);
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

    register('solvebench.runCurrent', async () => {
        const ref = currentSolution(root);
        if (!ref) {
            return;
        }
        const command = await runnerCommand(root);
        if (command) {
            // The folder, not the file, so every language it is solved in runs.
            sendToTerminal(root, [...command, path.posix.dirname(ref.relPath)]);
        }
    });

    register('solvebench.debugCurrent', async () => {
        const ref = currentSolution(root);
        if (ref) {
            await startDebugging(ref, root);
        }
    });

    register('solvebench.complexity', async () => {
        const ref = currentSolution(root);
        if (!ref) {
            return;
        }
        if (ref.language !== 'python' && ref.language !== 'java') {
            void vscode.window.showWarningMessage(
                'solvebench: complexity.py measures Python and Java solutions only.'
            );
            return;
        }
        const python = await requirePython(root);
        if (!python) {
            return;
        }
        const args = [python, 'complexity.py', ref.relPath];
        if (ref.language === 'java') {
            args.push('--lang', 'java');
        }
        sendToTerminal(root, args);
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
