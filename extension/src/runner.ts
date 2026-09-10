// Calls `run.py --json` and parses what it writes.

import * as vscode from 'vscode';
import { spawnCollect } from './exec';
import { RunPayload, SCHEMA } from './model';
import { requirePython } from './python';

export interface RunOptions {
    /** List the solutions without running them (`--stats --json`). */
    statsOnly?: boolean;
    /** Repo-relative paths to run. Empty means every solution. */
    filters?: string[];
    token?: vscode.CancellationToken;
}

export class RunnerError extends Error {}

/**
 * Run run.py and return the parsed JSON.
 *
 * run.py exits 1 when a solution fails, which is a normal result and not an
 * error here. We only throw when there is no JSON to read.
 */
export async function runPy(root: vscode.Uri, options: RunOptions = {}): Promise<RunPayload> {
    const python = await requirePython(root);
    if (!python) {
        throw new RunnerError('no Python interpreter');
    }

    const args = ['run.py', '--json'];
    if (options.statsOnly) {
        args.push('--stats');
    }
    args.push(...(options.filters ?? []));

    let stdout: string;
    let stderr: string;
    let code: number | null;
    try {
        ({ stdout, stderr, code } = await spawnCollect(python, args, root.fsPath, options.token));
    } catch (err) {
        // One error type out of here, so callers only handle RunnerError.
        throw new RunnerError(err instanceof Error ? err.message : String(err));
    }

    if (!stdout.trim()) {
        const detail = stderr.trim() || `run.py exited with code ${code}`;
        throw new RunnerError(`run.py produced no output. ${detail}`);
    }

    let payload: RunPayload;
    try {
        payload = JSON.parse(stdout) as RunPayload;
    } catch {
        // Something printed to stdout that is not JSON. Show the start of it,
        // because that is usually the real problem.
        throw new RunnerError(`could not read run.py output: ${stdout.slice(0, 200)}`);
    }

    if (payload.schema !== SCHEMA) {
        throw new RunnerError(
            `run.py speaks schema ${payload.schema}, this extension expects ${SCHEMA}. ` +
                'Update the extension or the repo so they match.'
        );
    }
    return payload;
}
