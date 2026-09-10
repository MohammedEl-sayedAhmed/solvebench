// Run / Debug / Complexity links above the code, so these do not need the
// command palette.

import * as vscode from 'vscode';
import { solutionRef } from './debug';

/**
 * Where to put the links in each language. First line that matches wins; if
 * nothing matches we fall back to the top of the file, so the links always
 * show up somewhere sensible.
 */
const ANCHORS: Record<string, RegExp> = {
    python: /^\s*(class\s+\w+|def\s+\w+)/,
    java: /^\s*(public\s+)?(final\s+)?(abstract\s+)?class\s+\w+/,
    cpp: /^\s*(class|struct)\s+\w+/,
    javascript: /^\s*(class\s+\w+|function\s+\w+|(?:const|let|var)\s+\w+\s*=)/,
    go: /^\s*func\s+\w+/,
    rust: /^\s*(fn|impl|struct)\s+\w+/,
};

/** complexity.py only measures these two. */
const MEASURABLE = new Set(['python', 'java']);

export class SolutionCodeLens implements vscode.CodeLensProvider {
    private readonly changed = new vscode.EventEmitter<void>();
    readonly onDidChangeCodeLenses = this.changed.event;

    constructor(private readonly root: vscode.Uri) {}

    refresh(): void {
        this.changed.fire();
    }

    provideCodeLenses(document: vscode.TextDocument): vscode.CodeLens[] {
        const enabled = vscode.workspace
            .getConfiguration('solvebench')
            .get<boolean>('showCodeLens', true);
        if (!enabled) {
            return [];
        }

        const ref = solutionRef(document.uri, this.root);
        if (!ref) {
            return [];
        }

        const line = this.anchor(document, ref.language);
        const range = new vscode.Range(line, 0, line, 0);
        // The uri goes along so a click acts on this file even if focus moved.
        const args = [document.uri];

        const lenses = [
            new vscode.CodeLens(range, {
                title: '$(play) Run',
                tooltip: 'Run this problem in every language it is solved in',
                command: 'solvebench.runCurrent',
                arguments: args,
            }),
            new vscode.CodeLens(range, {
                title: '$(debug-alt-small) Debug',
                tooltip: 'Debug this solution',
                command: 'solvebench.debugCurrent',
                arguments: args,
            }),
        ];

        if (MEASURABLE.has(ref.language)) {
            lenses.push(
                new vscode.CodeLens(range, {
                    title: '$(graph) Complexity',
                    tooltip: 'Estimate time and space complexity',
                    command: 'solvebench.complexity',
                    arguments: args,
                })
            );
        }
        return lenses;
    }

    private anchor(document: vscode.TextDocument, language: string): number {
        const pattern = ANCHORS[language];
        if (pattern) {
            // Stop early: the anchor is near the top, past the header comment.
            const limit = Math.min(document.lineCount, 60);
            for (let i = 0; i < limit; i++) {
                if (pattern.test(document.lineAt(i).text)) {
                    return i;
                }
            }
        }
        return 0;
    }
}
