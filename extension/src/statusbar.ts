// Solve count in the status bar. Click it to see the full breakdown.

import * as vscode from 'vscode';
import { SolutionJson } from './model';

export class SolveCount implements vscode.Disposable {
    private readonly item: vscode.StatusBarItem;

    constructor() {
        this.item = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, 100);
        this.item.command = 'solvebench.stats';
        this.item.name = 'solvebench';
    }

    update(solutions: SolutionJson[]): void {
        if (solutions.length === 0) {
            this.item.hide();
            return;
        }

        // One problem solved in two languages is one solve, not two.
        const problems = new Set(
            solutions.map((s) => `${s.platform}/${s.group}/${s.name.toLowerCase().replace(/[^a-z0-9]/g, '')}`)
        );
        const languages = new Set(solutions.map((s) => s.lang));

        this.item.text = `$(checklist) ${problems.size} solved`;
        this.item.tooltip =
            `${solutions.length} solution files across ${languages.size} language(s): ` +
            `${[...languages].sort().join(', ')}\nClick for the breakdown by platform.`;
        this.item.show();
    }

    dispose(): void {
        this.item.dispose();
    }
}
