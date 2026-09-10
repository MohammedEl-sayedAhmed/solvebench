// Running a child process and collecting its output.

import { spawn } from 'child_process';
import * as vscode from 'vscode';

export interface Collected {
    stdout: string;
    stderr: string;
    code: number | null;
}

export class ProcessError extends Error {}

export function spawnCollect(
    command: string,
    args: string[],
    cwd: string,
    token?: vscode.CancellationToken
): Promise<Collected> {
    return new Promise((resolve, reject) => {
        const child = spawn(command, args, { cwd });
        let stdout = '';
        let stderr = '';

        child.stdout.on('data', (chunk: Buffer) => {
            stdout += chunk.toString();
        });
        child.stderr.on('data', (chunk: Buffer) => {
            stderr += chunk.toString();
        });

        const cancel = token?.onCancellationRequested(() => child.kill());

        child.on('error', (err) => {
            cancel?.dispose();
            reject(new ProcessError(`could not start ${command}: ${err.message}`));
        });
        child.on('close', (code) => {
            cancel?.dispose();
            resolve({ stdout, stderr, code });
        });
    });
}
