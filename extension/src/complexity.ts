// Measuring a solution and showing the result in a panel.

import * as vscode from 'vscode';
import { ComplexityResult, page, safeColor } from './complexityPage';
import { problemId, SolutionRef } from './debug';
import { spawnCollect } from './exec';
import { requirePython } from './python';

export { ComplexityResult } from './complexityPage';

/** Measure a solution. Returns undefined when complexity.py refused. */
export async function measure(
    root: vscode.Uri,
    ref: SolutionRef
): Promise<ComplexityResult | undefined> {
    const python = await requirePython(root);
    if (!python) {
        return undefined;
    }

    const args = ['complexity.py', problemId(ref), '--json'];
    if (ref.language === 'java') {
        args.push('--lang', 'java');
    }

    return vscode.window.withProgress(
        {
            location: vscode.ProgressLocation.Notification,
            title: `solvebench: measuring ${problemId(ref)}`,
            cancellable: true,
        },
        async (_progress, token) => {
            const { stdout, stderr, code } = await spawnCollect(
                python,
                args,
                root.fsPath,
                token
            );
            if (token.isCancellationRequested) {
                return undefined;
            }
            if (code !== 0 || !stdout.trim()) {
                // complexity.py explains itself well (needs a complexity_input
                // hook, no matching solution), so show what it said.
                const said = stderr.trim() || stdout.trim() || `exit code ${code}`;
                void vscode.window.showErrorMessage(`solvebench: ${said.split('\n')[0]}`);
                return undefined;
            }
            try {
                return JSON.parse(stdout) as ComplexityResult;
            } catch {
                void vscode.window.showErrorMessage(
                    `solvebench: could not read complexity.py output: ${stdout.slice(0, 160)}`
                );
                return undefined;
            }
        }
    );
}

function nonce(): string {
    const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    let out = '';
    for (let i = 0; i < 32; i++) {
        out += chars[Math.floor(Math.random() * chars.length)];
    }
    return out;
}

/** One reusable panel, so repeated runs do not pile up tabs. */
export class ComplexityView {
    private panel: vscode.WebviewPanel | undefined;

    constructor(private readonly extensionUri: vscode.Uri) {}

    show(result: ComplexityResult): void {
        const mediaRoot = vscode.Uri.joinPath(this.extensionUri, 'media');

        if (!this.panel) {
            this.panel = vscode.window.createWebviewPanel(
                'solvebench.complexity',
                'Complexity',
                { viewColumn: vscode.ViewColumn.Beside, preserveFocus: true },
                {
                    // Needed for zoom, hover and the colour pickers. Nothing is
                    // loaded from outside media/, and the CSP allows only the
                    // one nonced script.
                    enableScripts: true,
                    localResourceRoots: [mediaRoot],
                    retainContextWhenHidden: true,
                }
            );
            this.panel.onDidDispose(() => {
                this.panel = undefined;
            });
            this.panel.webview.onDidReceiveMessage((message: unknown) => {
                void this.onMessage(message);
            });
        }

        const webview = this.panel.webview;
        this.panel.title = `Complexity \u2014 ${result.function}`;
        webview.html = page(result, {
            css: webview.asWebviewUri(vscode.Uri.joinPath(mediaRoot, 'chart.css')).toString(),
            js: webview.asWebviewUri(vscode.Uri.joinPath(mediaRoot, 'chart.js')).toString(),
            nonce: nonce(),
            cspSource: webview.cspSource,
        });
        this.panel.reveal(vscode.ViewColumn.Beside, true);
    }

    /** Colour picked in the panel -> the matching setting. */
    private async onMessage(message: unknown): Promise<void> {
        if (typeof message !== 'object' || message === null) {
            return;
        }
        const { type, role, value } = message as Record<string, unknown>;
        if (type !== 'saveColor' || typeof role !== 'string' || typeof value !== 'string') {
            return;
        }
        const setting =
            role === 'measured'
                ? 'chartMeasuredColor'
                : role === 'fitted'
                  ? 'chartFittedColor'
                  : undefined;
        if (!setting) {
            return;
        }
        // An empty value means "back to the default", so it is allowed through.
        const colour = value === '' ? '' : safeColor(value);
        if (colour === undefined) {
            return;
        }
        await vscode.workspace
            .getConfiguration('solvebench')
            .update(setting, colour, vscode.ConfigurationTarget.Global);
    }

    dispose(): void {
        this.panel?.dispose();
    }
}
