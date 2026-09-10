// Builds a debug config from a solution file, so nobody has to add one to
// .vscode/launch.json for every new solution.

import * as path from 'path';
import * as vscode from 'vscode';

/** Language folders and their file extensions. Mirrors LANGUAGES in run.py. */
const LANGUAGES: Record<string, string> = {
    python: '.py',
    cpp: '.cpp',
    java: '.java',
    javascript: '.js',
    go: '.go',
    rust: '.rs',
};

/** The extension each debugger needs, so we can say what is missing. */
const DEBUGGER_EXTENSIONS: Record<string, { id: string; name: string }> = {
    python: { id: 'ms-python.debugpy', name: 'Python Debugger' },
    java: { id: 'vscjava.vscode-java-debug', name: 'Debugger for Java' },
    cpp: { id: 'ms-vscode.cpptools', name: 'C/C++' },
    go: { id: 'golang.go', name: 'Go' },
    rust: { id: 'vadimcn.vscode-lldb', name: 'CodeLLDB' },
    // JavaScript uses the debugger built into VS Code, so nothing to install.
};

/** Languages we can build a config for. Go and Rust have no solutions yet. */
const SUPPORTED = new Set(['python', 'java', 'javascript', 'cpp']);

export interface SolutionRef {
    language: string;
    /** Relative to the repo, forward slashes. Same id run.py uses. */
    relPath: string;
    fsPath: string;
}

export type DebugTarget =
    | { kind: 'ok'; config: vscode.DebugConfiguration }
    | { kind: 'missingExtension'; id: string; name: string }
    | { kind: 'unsupported'; reason: string };

/**
 * Work out whether a file is a solvebench solution.
 * Returns undefined for helpers in common/ and for anything outside the
 * language folders.
 */
export function solutionRef(uri: vscode.Uri, root: vscode.Uri): SolutionRef | undefined {
    const rel = path.relative(root.fsPath, uri.fsPath);
    if (!rel || rel.startsWith('..') || path.isAbsolute(rel)) {
        return undefined;
    }
    const parts = rel.split(path.sep);
    const language = parts[0];
    const expected = LANGUAGES[language];
    if (!expected || parts.length < 2) {
        return undefined;
    }
    if (path.extname(uri.fsPath) !== expected) {
        return undefined;
    }
    if (parts.includes('common')) {
        return undefined; // shared test helpers, not solutions
    }
    return { language, relPath: parts.join('/'), fsPath: uri.fsPath };
}

/** Build the debug config for a solution, or say what is in the way. */
export function debugTargetFor(ref: SolutionRef, root: vscode.Uri): DebugTarget {
    if (!SUPPORTED.has(ref.language)) {
        const needed = DEBUGGER_EXTENSIONS[ref.language];
        return {
            kind: 'unsupported',
            reason:
                `debugging ${ref.language} solutions is not set up yet` +
                (needed ? ` (it would need the ${needed.name} extension)` : ''),
        };
    }

    const needed = DEBUGGER_EXTENSIONS[ref.language];
    if (needed && !vscode.extensions.getExtension(needed.id)) {
        return { kind: 'missingExtension', id: needed.id, name: needed.name };
    }

    const dir = path.dirname(ref.fsPath);
    const name = path.basename(ref.fsPath, path.extname(ref.fsPath));
    const repo = root.fsPath;

    switch (ref.language) {
        case 'python':
            return {
                kind: 'ok',
                config: {
                    type: 'debugpy',
                    request: 'launch',
                    name: `solvebench: ${name}`,
                    program: ref.fsPath,
                    cwd: dir,
                    console: 'integratedTerminal',
                    env: { PYTHONPATH: path.join(repo, 'python') },
                },
            };

        case 'javascript':
            return {
                kind: 'ok',
                config: {
                    type: 'node',
                    request: 'launch',
                    name: `solvebench: ${name}`,
                    program: ref.fsPath,
                    cwd: dir,
                    console: 'integratedTerminal',
                    env: { NODE_PATH: path.join(repo, 'javascript') },
                },
            };

        case 'java':
            return {
                kind: 'ok',
                config: {
                    type: 'java',
                    request: 'launch',
                    name: `solvebench: ${name}`,
                    mainClass: javaMainClass(ref.relPath),
                    cwd: dir,
                    // scripts/build_java.py already handles a half-finished file
                    // blocking a finished one, so reuse it instead of copying it.
                    preLaunchTask: 'java: build all',
                    classPaths: [path.join(repo, '.pst', 'build', 'java')],
                    sourcePaths: [path.join(repo, 'java')],
                },
            };

        case 'cpp':
            return {
                kind: 'ok',
                config: {
                    type: 'cppdbg',
                    request: 'launch',
                    name: `solvebench: ${name}`,
                    // The task below writes the binary next to the source.
                    program: path.join(dir, `${name}.out`),
                    args: [],
                    cwd: dir,
                    stopAtEntry: false,
                    MIMode: 'gdb',
                    preLaunchTask: 'cpp: build current file',
                    setupCommands: [
                        {
                            description: 'Enable pretty-printing for gdb',
                            text: '-enable-pretty-printing',
                            ignoreFailures: true,
                        },
                    ],
                },
            };

        default:
            return { kind: 'unsupported', reason: `unknown language ${ref.language}` };
    }
}

/** java/leetcode/easy/TwoSum.java -> leetcode.easy.TwoSum */
export function javaMainClass(relPath: string): string {
    return relPath
        .replace(/^java\//, '')
        .replace(/\.java$/, '')
        .split('/')
        .join('.');
}

/**
 * Start debugging a solution. Offers to install the debugger extension when
 * that is what is missing.
 */
export async function startDebugging(ref: SolutionRef, root: vscode.Uri): Promise<boolean> {
    const target = debugTargetFor(ref, root);

    if (target.kind === 'unsupported') {
        void vscode.window.showWarningMessage(`solvebench: ${target.reason}`);
        return false;
    }

    if (target.kind === 'missingExtension') {
        const install = 'Install';
        const answer = await vscode.window.showWarningMessage(
            `solvebench: debugging this needs the ${target.name} extension.`,
            install
        );
        if (answer === install) {
            await vscode.commands.executeCommand(
                'workbench.extensions.installExtension',
                target.id
            );
            void vscode.window.showInformationMessage(
                `solvebench: ${target.name} installed. Try debugging again.`
            );
        }
        return false;
    }

    const folder = vscode.workspace.getWorkspaceFolder(root);
    return vscode.debug.startDebugging(folder, target.config);
}
