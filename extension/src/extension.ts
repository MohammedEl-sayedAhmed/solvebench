// Entry point. Only runs in a folder that has run.py in it, which is what the
// activationEvent in package.json checks.

import * as fs from 'fs';
import * as path from 'path';
import * as vscode from 'vscode';
import { SolutionCodeLens } from './codelens';
import { registerCommands } from './commands';
import { solutionRef } from './debug';
import { resetPythonCache } from './python';
import { SolveCount } from './statusbar';
import { disposeTerminal, onTerminalClosed } from './terminal';
import { SolutionTests } from './tests';

/**
 * VS Code language ids for the CodeLens provider. These are the editor's ids,
 * not our folder names: cpp/ files are 'cpp', javascript/ files are
 * 'javascript', rust/ files are 'rust'.
 */
const SOLUTION_LANGUAGE_IDS = ['python', 'java', 'cpp', 'javascript', 'go', 'rust'];

/** The workspace folder that holds run.py. */
function findRepoRoot(): vscode.Uri | undefined {
    for (const folder of vscode.workspace.workspaceFolders ?? []) {
        if (fs.existsSync(path.join(folder.uri.fsPath, 'run.py'))) {
            return folder.uri;
        }
    }
    return undefined;
}

export async function activate(context: vscode.ExtensionContext): Promise<void> {
    const root = findRepoRoot();
    if (!root) {
        return;
    }

    const tests = new SolutionTests(root);
    context.subscriptions.push(tests);
    registerCommands(context, root, tests);

    // Run / Debug / Complexity links above the code.
    const codeLens = new SolutionCodeLens(root);
    context.subscriptions.push(
        vscode.languages.registerCodeLensProvider(
            SOLUTION_LANGUAGE_IDS.map((language) => ({ language, scheme: 'file' })),
            codeLens
        )
    );

    // Solve count in the status bar, kept in step with discovery.
    const solveCount = new SolveCount();
    context.subscriptions.push(solveCount, tests.onDidRefresh((s) => solveCount.update(s)));

    // Drives the "when" clause on the editor title buttons.
    const updateContext = (editor: vscode.TextEditor | undefined) => {
        const isSolution = Boolean(editor && solutionRef(editor.document.uri, root));
        void vscode.commands.executeCommand('setContext', 'solvebench.isSolution', isSolution);
    };
    updateContext(vscode.window.activeTextEditor);

    context.subscriptions.push(
        vscode.window.onDidChangeActiveTextEditor(updateContext),
        vscode.window.onDidCloseTerminal(onTerminalClosed),
        // A new or deleted solution file changes the tree, so rebuild it.
        watchSolutions(root, tests),
        vscode.workspace.onDidChangeConfiguration((e) => {
            if (e.affectsConfiguration('solvebench.pythonPath')) {
                resetPythonCache();
                void tests.refresh();
            }
            if (e.affectsConfiguration('solvebench.showCodeLens')) {
                codeLens.refresh();
            }
        })
    );

    await tests.refresh();
}

/**
 * Watch the solution folders. Only create and delete matter: editing a file
 * does not change the tree, and a rebuild on every keystroke would be wasteful.
 */
function watchSolutions(root: vscode.Uri, tests: SolutionTests): vscode.Disposable {
    const pattern = new vscode.RelativePattern(
        root,
        '{python,cpp,java,javascript,go,rust}/**/*.{py,cpp,java,js,go,rs}'
    );
    const watcher = vscode.workspace.createFileSystemWatcher(pattern, false, true, false);
    const refresh = () => void tests.refresh();
    watcher.onDidCreate(refresh);
    watcher.onDidDelete(refresh);
    return watcher;
}

export function deactivate(): void {
    disposeTerminal();
}
