// Runs complexity.py --json and draws the measurements.
//
// The point of the chart is the question the text output cannot answer: the
// estimator says O(n log n), but does the data actually look more like O(n)?
// Plotting the measured points against neighbouring classes shows that.

import * as vscode from 'vscode';
import { problemId, SolutionRef } from './debug';
import { spawnCollect } from './exec';
import { requirePython } from './python';

/** Mirrors MODELS in python/common/complexity.py. Order matters: neighbours. */
export const MODELS: { name: string; f: (n: number) => number }[] = [
    { name: 'O(1)', f: () => 1 },
    { name: 'O(log n)', f: (n) => (n > 1 ? Math.log2(n) : 1) },
    { name: 'O(n)', f: (n) => n },
    { name: 'O(n log n)', f: (n) => (n > 1 ? n * Math.log2(n) : n) },
    { name: 'O(n^2)', f: (n) => n * n },
    { name: 'O(n^3)', f: (n) => n ** 3 },
    { name: 'O(2^n)', f: (n) => 2 ** Math.min(n, 60) },
];

export interface ComplexityResult {
    schema: number;
    solution: string;
    lang: string;
    function: string;
    inputs: string;
    sizes: number[];
    times: number[];
    time_class: string;
    spaces?: number[];
    space_class?: string;
}

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

/**
 * The scale factor c for `c * f(n)`, fitted in log space.
 * Same method as _best_fit in python/common/complexity.py, so the curve drawn
 * for the winning class is the curve that actually won.
 */
export function fitScale(sizes: number[], values: number[], f: (n: number) => number): number {
    const usable = sizes
        .map((n, i) => ({ n, v: values[i] }))
        .filter((p) => p.v > 0 && Number.isFinite(p.v));
    if (usable.length === 0) {
        return 0;
    }
    const offset =
        usable.reduce((sum, p) => sum + (Math.log(p.v) - Math.log(f(p.n))), 0) / usable.length;
    return Math.exp(offset);
}

/** The fitted class plus its neighbours, for comparison. */
function classesToDraw(fitted: string): string[] {
    const i = MODELS.findIndex((m) => m.name === fitted);
    if (i < 0) {
        return [fitted];
    }
    const picked = [MODELS[i].name];
    if (i > 0) {
        picked.push(MODELS[i - 1].name);
    }
    // O(2^n) is unplottable next to the others, so never draw it as a reference.
    if (i + 1 < MODELS.length && MODELS[i + 1].name !== 'O(2^n)') {
        picked.push(MODELS[i + 1].name);
    }
    return picked;
}

const PLOT = { w: 640, h: 300, left: 64, right: 116, top: 16, bottom: 40 };

function svgChart(
    sizes: number[],
    values: number[],
    fitted: string,
    yLabel: string,
    toDisplay: (v: number) => number
): string {
    if (sizes.length === 0) {
        return '<p class="muted">no data points</p>';
    }

    const shown = values.map(toDisplay);
    const innerW = PLOT.w - PLOT.left - PLOT.right;
    const innerH = PLOT.h - PLOT.top - PLOT.bottom;

    const drawn = classesToDraw(fitted);
    const curves = drawn.map((name) => {
        const model = MODELS.find((m) => m.name === name)!;
        const c = fitScale(sizes, values, model.f);
        return { name, points: sizes.map((n) => toDisplay(c * model.f(n))) };
    });

    const xMax = Math.max(...sizes);
    const yMax = Math.max(...shown, ...curves.flatMap((c) => c.points)) * 1.08 || 1;
    const x = (n: number) => PLOT.left + (n / xMax) * innerW;
    const y = (v: number) => PLOT.top + innerH - (v / yMax) * innerH;

    const grid: string[] = [];
    const labels: string[] = [];
    for (let i = 0; i <= 4; i++) {
        const gy = PLOT.top + (innerH * i) / 4;
        const value = (yMax * (4 - i)) / 4;
        grid.push(`<line x1="${PLOT.left}" y1="${gy}" x2="${PLOT.left + innerW}" y2="${gy}"/>`);
        labels.push(
            `<text class="tick" x="${PLOT.left - 8}" y="${gy + 4}" text-anchor="end">${fmt(value)}</text>`
        );
    }
    for (const n of sizes) {
        labels.push(
            `<text class="tick" x="${x(n)}" y="${PLOT.top + innerH + 18}" text-anchor="middle">${n}</text>`
        );
    }

    // The fitted class is first, so it gets the strong colour.
    const curveSvg = curves
        .map((c, i) => {
            const d = c.points.map((v, j) => `${j === 0 ? 'M' : 'L'}${x(sizes[j])},${y(v)}`).join(' ');
            const cls = i === 0 ? 'fit' : 'ref';
            return `<path class="${cls}" d="${d}"/>`;
        })
        .join('');

    const legend = curves
        .map((c, i) => {
            const ly = PLOT.top + 14 + i * 20;
            const lx = PLOT.left + innerW + 12;
            return (
                `<line class="${i === 0 ? 'fit' : 'ref'}" x1="${lx}" y1="${ly - 4}" x2="${lx + 18}" y2="${ly - 4}"/>` +
                `<text class="legend ${i === 0 ? 'fitText' : ''}" x="${lx + 24}" y="${ly}">${esc(c.name)}</text>`
            );
        })
        .join('');

    const measuredLine = shown
        .map((v, i) => `${i === 0 ? 'M' : 'L'}${x(sizes[i])},${y(v)}`)
        .join(' ');
    const dots = shown
        .map((v, i) => `<circle class="dot" cx="${x(sizes[i])}" cy="${y(v)}" r="4"/>`)
        .join('');

    return `
<svg viewBox="0 0 ${PLOT.w} ${PLOT.h}" class="chart" role="img"
     aria-label="${esc(yLabel)} against input size, fitted ${esc(fitted)}">
  <g class="grid">${grid.join('')}</g>
  <line class="axis" x1="${PLOT.left}" y1="${PLOT.top}" x2="${PLOT.left}" y2="${PLOT.top + innerH}"/>
  <line class="axis" x1="${PLOT.left}" y1="${PLOT.top + innerH}" x2="${PLOT.left + innerW}" y2="${PLOT.top + innerH}"/>
  ${curveSvg}
  <path class="measured" d="${measuredLine}"/>
  ${dots}
  <circle class="dot" cx="${PLOT.left + innerW + 21}" cy="${PLOT.top + innerH - 6}" r="4"/>
  <text class="legend" x="${PLOT.left + innerW + 36}" y="${PLOT.top + innerH - 2}">measured</text>
  ${legend}
  ${labels.join('')}
  <text class="axisLabel" x="${PLOT.left + innerW / 2}" y="${PLOT.h - 4}" text-anchor="middle">input size (n)</text>
  <text class="axisLabel" transform="translate(14,${PLOT.top + innerH / 2}) rotate(-90)" text-anchor="middle">${esc(yLabel)}</text>
</svg>`;
}

function fmt(v: number): string {
    if (v === 0) {
        return '0';
    }
    if (v >= 1000) {
        return Math.round(v).toLocaleString('en-US');
    }
    if (v >= 10) {
        return v.toFixed(0);
    }
    if (v >= 1) {
        return v.toFixed(1);
    }
    return v.toFixed(3);
}

function esc(s: string): string {
    return s.replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]!));
}

function table(result: ComplexityResult): string {
    const rows = result.sizes
        .map((n, i) => {
            const space =
                result.spaces && i < result.spaces.length
                    ? fmt(result.spaces[i] / 1024)
                    : result.spaces
                      ? '—'
                      : '';
            return (
                `<tr><td>${n}</td><td>${fmt(result.times[i] * 1e3)}</td>` +
                (result.spaces ? `<td>${space}</td>` : '') +
                '</tr>'
            );
        })
        .join('');
    return `
<table>
  <thead><tr><th>n</th><th>time (ms)</th>${result.spaces ? '<th>memory (KB)</th>' : ''}</tr></thead>
  <tbody>${rows}</tbody>
</table>`;
}

export function page(result: ComplexityResult): string {
    const spaceSection =
        result.spaces && result.space_class
            ? `<h2>Memory — ${esc(result.space_class)}</h2>` +
              svgChart(
                  result.sizes.slice(0, result.spaces.length),
                  result.spaces,
                  result.space_class,
                  'memory (KB)',
                  (v) => v / 1024
              )
            : '';

    const thin =
        result.sizes.length < 3
            ? '<p class="warn">Fewer than 3 data points — the fit is unreliable. Try smaller --sizes.</p>'
            : '';

    return `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta http-equiv="Content-Security-Policy"
      content="default-src 'none'; style-src 'unsafe-inline';">
<title>Complexity — ${esc(result.function)}</title>
<style>
  body {
    font-family: var(--vscode-font-family);
    color: var(--vscode-editor-foreground);
    background: var(--vscode-editor-background);
    padding: 16px 20px;
    margin: 0;
  }
  h1 { font-size: 1.25rem; margin: 0 0 2px; }
  h2 { font-size: 1rem; margin: 24px 0 4px; font-weight: 600; }
  .sub { color: var(--vscode-descriptionForeground); font-size: .85rem; margin: 0 0 4px; }
  code { font-family: var(--vscode-editor-font-family); }
  .verdict { font-size: 1.05rem; margin: 12px 0 0; }
  .verdict b { color: var(--vscode-charts-blue); }
  .chart { width: 100%; max-width: 680px; height: auto; display: block; margin: 4px 0 0; }
  .grid line { stroke: var(--vscode-panel-border); stroke-width: 1; }
  .axis { stroke: var(--vscode-editor-foreground); stroke-width: 1; opacity: .6; }
  .measured { fill: none; stroke: var(--vscode-charts-blue); stroke-width: 2; }
  .dot { fill: var(--vscode-charts-blue); }
  .fit { fill: none; stroke: var(--vscode-charts-orange); stroke-width: 2; stroke-dasharray: 6 3; }
  .ref { fill: none; stroke: var(--vscode-descriptionForeground); stroke-width: 1; stroke-dasharray: 2 3; opacity: .8; }
  text { fill: var(--vscode-editor-foreground); }
  .tick, .legend { font-size: 10px; fill: var(--vscode-descriptionForeground); }
  .fitText { fill: var(--vscode-charts-orange); }
  .axisLabel { font-size: 11px; fill: var(--vscode-descriptionForeground); }
  table { border-collapse: collapse; margin-top: 8px; font-size: .85rem; }
  th, td { padding: 3px 14px 3px 0; text-align: right; }
  th { color: var(--vscode-descriptionForeground); font-weight: 600; }
  .note, .warn { font-size: .8rem; color: var(--vscode-descriptionForeground); margin-top: 18px; }
  .warn { color: var(--vscode-editorWarning-foreground); }
</style>
</head>
<body>
  <h1>${esc(result.function)}</h1>
  <p class="sub"><code>${esc(result.solution)}</code></p>
  <p class="sub">inputs: ${esc(result.inputs)}</p>
  <p class="verdict">time <b>${esc(result.time_class)}</b>${
      result.space_class ? ` · space <b>${esc(result.space_class)}</b>` : ''
  }</p>
  ${thin}

  <h2>Time — ${esc(result.time_class)}</h2>
  ${svgChart(result.sizes, result.times, result.time_class, 'time (ms)', (v) => v * 1e3)}
  ${spaceSection}

  <h2>Measurements</h2>
  ${table(result)}

  <p class="note">
    The dashed orange line is the class that fitted best; the faint lines are its
    neighbours, each scaled to the data the same way. If the points track a faint
    line more closely than the orange one, treat the verdict with suspicion.
    This is measured growth fitted to common classes, not a proof.
  </p>
</body>
</html>`;
}

/** One reusable panel, so repeated runs do not pile up tabs. */
export class ComplexityView {
    private panel: vscode.WebviewPanel | undefined;

    show(result: ComplexityResult): void {
        if (!this.panel) {
            this.panel = vscode.window.createWebviewPanel(
                'solvebench.complexity',
                'Complexity',
                { viewColumn: vscode.ViewColumn.Beside, preserveFocus: true },
                { enableScripts: false, retainContextWhenHidden: true }
            );
            this.panel.onDidDispose(() => {
                this.panel = undefined;
            });
        }
        this.panel.title = `Complexity — ${result.function}`;
        this.panel.webview.html = page(result);
        this.panel.reveal(vscode.ViewColumn.Beside, true);
    }

    dispose(): void {
        this.panel?.dispose();
    }
}
