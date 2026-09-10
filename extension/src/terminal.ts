// A shared terminal for the commands whose output people just read.

import * as vscode from 'vscode';

let terminal: vscode.Terminal | undefined;

export function disposeTerminal(): void {
    terminal?.dispose();
    terminal = undefined;
}

/** Quote only what needs it, so the command stays readable in the terminal. */
function quote(arg: string): string {
    return /[\s"'$`\\]/.test(arg) ? `"${arg.replace(/(["$`\\])/g, '\\$1')}"` : arg;
}

export function sendToTerminal(cwd: vscode.Uri, parts: string[]): void {
    if (!terminal || terminal.exitStatus !== undefined) {
        terminal = vscode.window.createTerminal({ name: 'solvebench', cwd });
    }
    terminal.show(true);
    terminal.sendText(parts.map(quote).join(' '));
}

export function onTerminalClosed(closed: vscode.Terminal): void {
    if (closed === terminal) {
        terminal = undefined;
    }
}
