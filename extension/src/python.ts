// Finding a Python interpreter. run.py, new.py and complexity.py all need one,
// so this is the single place that looks for it.

import { execFile } from 'child_process';
import * as fs from 'fs';
import * as path from 'path';
import * as vscode from 'vscode';

const NOT_FOUND =
    'solvebench: no Python interpreter found. Run ./setup.sh to make a .venv, ' +
    'pick one with the Python extension, or set solvebench.pythonPath.';

let cached: string | undefined;

/** Clear the cache when the setting or the picked interpreter changes. */
export function resetPythonCache(): void {
    cached = undefined;
}

/**
 * First match wins:
 *   1. the solvebench.pythonPath setting
 *   2. .venv in the workspace (what setup.sh makes)
 *   3. the interpreter the Python extension has selected
 *   4. python3, then python, from PATH
 */
export async function findPython(root: vscode.Uri): Promise<string | undefined> {
    if (cached) {
        return cached;
    }

    const configured = vscode.workspace
        .getConfiguration('solvebench')
        .get<string>('pythonPath', '')
        .trim();
    if (configured) {
        cached = configured;
        return cached;
    }

    const venv =
        process.platform === 'win32'
            ? path.join(root.fsPath, '.venv', 'Scripts', 'python.exe')
            : path.join(root.fsPath, '.venv', 'bin', 'python');
    if (fs.existsSync(venv)) {
        cached = venv;
        return cached;
    }

    const picked = await fromPythonExtension(root);
    if (picked) {
        cached = picked;
        return cached;
    }

    for (const candidate of ['python3', 'python']) {
        if (await canRun(candidate)) {
            cached = candidate;
            return cached;
        }
    }

    return undefined;
}

/** Same as findPython, but shows the error message and returns undefined. */
export async function requirePython(root: vscode.Uri): Promise<string | undefined> {
    const python = await findPython(root);
    if (!python) {
        void vscode.window.showErrorMessage(NOT_FOUND);
    }
    return python;
}

/** Read the interpreter the Python extension has selected, if it is installed. */
async function fromPythonExtension(root: vscode.Uri): Promise<string | undefined> {
    const ext = vscode.extensions.getExtension('ms-python.python');
    if (!ext) {
        return undefined;
    }
    try {
        if (!ext.isActive) {
            await ext.activate();
        }
        // Typed as any on purpose: this is another extension's API and it is
        // optional. Anything unexpected means we fall through to PATH.
        const api = ext.exports as any;
        const active = api?.environments?.getActiveEnvironmentPath?.(root);
        if (!active?.path) {
            return undefined;
        }
        const resolved = await api.environments.resolveEnvironment?.(active);
        const exe = resolved?.executable?.uri?.fsPath;
        return typeof exe === 'string' && exe ? exe : active.path;
    } catch {
        return undefined;
    }
}

function canRun(command: string): Promise<boolean> {
    return new Promise((resolve) => {
        execFile(command, ['--version'], { timeout: 5000 }, (err) => resolve(!err));
    });
}
