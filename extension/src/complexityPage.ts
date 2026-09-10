// Building the complexity page. Deliberately free of any vscode import, so
// the localhost preview (preview/serve.js) and the checks can load it in plain
// Node. Anything needing the editor lives in complexity.ts.

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

/** Where the page gets chart.css and chart.js from, and the CSP nonce. */
export interface Resources {
    css: string;
    js: string;
    /** A nonce is required in the webview; the preview has none. */
    nonce?: string;
    /** Extra CSP sources (the webview's cspSource). */
    cspSource?: string;
    /** The preview gets a light/dark toggle; in VS Code the editor decides. */
    themeToggle?: boolean;
}

function esc(s: string): string {
    return s.replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]!));
}

/** Table numbers: one decimal count per column, so it reads as a column. */
function columnDecimals(values: number[]): number {
    const max = Math.max(...values.map(Math.abs), 0);
    return max < 1 ? 3 : max < 10 ? 2 : max < 100 ? 1 : 0;
}

function num(v: number, decimals: number): string {
    return v.toLocaleString('en-US', {
        minimumFractionDigits: decimals,
        maximumFractionDigits: decimals,
    });
}

function table(result: ComplexityResult): string {
    const ms = result.times.map((t) => t * 1e3);
    const kb = (result.spaces ?? []).map((s) => s / 1024);
    const timeDec = columnDecimals(ms);
    const spaceDec = columnDecimals(kb);

    const rows = result.sizes
        .map((n, i) => {
            const space = result.spaces
                ? i < kb.length
                    ? num(kb[i], spaceDec)
                    : '—'
                : '';
            return (
                `<tr><td>${n.toLocaleString('en-US')}</td><td>${num(ms[i], timeDec)}</td>` +
                (result.spaces ? `<td>${space}</td>` : '') +
                '</tr>'
            );
        })
        .join('');

    return `<table>
  <thead><tr><th>n</th><th>time (ms)</th>${result.spaces ? '<th>memory (KB)</th>' : ''}</tr></thead>
  <tbody>${rows}</tbody>
</table>`;
}

function chartBlock(id: string, heading: string): string {
    return `
  <div class="chartHead">
    <h2>${esc(heading)}</h2>
    <span class="zoomState" data-zoom-state="${id}"></span>
    <span class="spacer"></span>
    <div class="zoomBar" role="group" aria-label="Zoom ${esc(heading)}">
      <button type="button" data-zoom="${id}" data-act="out" title="Zoom out" aria-label="Zoom out">&minus;</button>
      <button type="button" data-zoom="${id}" data-act="in" title="Zoom in" aria-label="Zoom in">+</button>
      <button type="button" data-zoom="${id}" data-act="fit" title="Fit to the data">Fit</button>
    </div>
  </div>
  <div class="chartBox" data-chart="${id}">
    <svg viewBox="0 0 820 360" class="chart" role="img" aria-label="${esc(heading)}"></svg>
    <div class="tooltip" role="status"></div>
  </div>
  <p class="chartHint">Drag to pan · <kbd>Ctrl</kbd>+scroll to zoom · double-click to fit</p>`;
}

/**
 * The page shell. Rendering happens in media/chart.js: zoom has to redraw on
 * every interaction, so the marks cannot be baked in here.
 */
export function page(result: ComplexityResult, res: Resources): string {
    const series: Record<string, unknown> = {
        time: {
            sizes: result.sizes,
            values: result.times.map((t) => t * 1e3),
            fitted: result.time_class,
            label: 'time (ms)',
        },
    };
    if (result.spaces && result.space_class) {
        series.space = {
            sizes: result.sizes.slice(0, result.spaces.length),
            values: result.spaces.map((s) => s / 1024),
            fitted: result.space_class,
            label: 'memory (KB)',
        };
    }

    const nonce = res.nonce ? ` nonce="${res.nonce}"` : '';
    // Saving a colour to settings only means anything inside VS Code, and an
    // inline script is only permitted where there is a nonce to mark it with.
    const bridge = res.nonce
        ? `<script nonce="${res.nonce}">
    if (typeof acquireVsCodeApi === 'function') {
      var sbApi = acquireVsCodeApi();
      window.sbHost = {
        saveColor: function (role, value) {
          sbApi.postMessage({ type: 'saveColor', role: role, value: value });
        }
      };
    }
  </script>`
        : '<!-- no host bridge: colours persist in localStorage only -->';
    const scriptSrc = res.nonce ? `'nonce-${res.nonce}'` : "'self'";
    const styleSrc = res.cspSource ? `${res.cspSource} 'unsafe-inline'` : "'self' 'unsafe-inline'";
    const csp =
        `default-src 'none'; img-src data:; style-src ${styleSrc}; script-src ${scriptSrc};`;

    const thin =
        result.sizes.length < 3
            ? '<p class="warn">Only a few data points, so the answer is not reliable. Try smaller sizes with <code>--sizes</code>.</p>'
            : '';

    // JSON in a script tag: </script> inside a string would end the block early.
    const dataJson = JSON.stringify({ series }).replace(/</g, '\\u003c');

    return `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta http-equiv="Content-Security-Policy" content="${csp}">
<title>Complexity — ${esc(result.function)}</title>
<link rel="stylesheet" href="${res.css}">
</head>
<body>
  <h1>${esc(result.function)}</h1>
  <p class="sub"><code>${esc(result.solution)}</code></p>
  <p class="sub">inputs: ${esc(result.inputs)}</p>
  <p class="verdict">time <b>${esc(result.time_class)}</b>${
      result.space_class ? ` · space <b>${esc(result.space_class)}</b>` : ''
  }</p>
  <p class="sub"><span class="swatch m"></span>measured<span class="swatch f" style="margin-left:12px"></span>fitted class</p>
  ${thin}

  <div class="controls">
    <div class="group">
      <span class="ctlLabel">Scale</span>
      <div class="segmented" role="group" aria-label="Axis scale">
        <button type="button" data-scale="linear" aria-pressed="true">Linear</button>
        <button type="button" data-scale="log" aria-pressed="false"
                title="Every growth class is a straight line on a log scale, so the one your points lie along is the answer">Log</button>
      </div>
    </div>

    <div class="group">
      <span class="ctlLabel">Colours</span>
      <label class="colorPick" title="Colour of the measured line">
        <input type="color" id="sb-color-measured"><span>measured</span>
      </label>
      <label class="colorPick" title="Colour of the fitted curve">
        <input type="color" id="sb-color-fitted"><span>fitted</span>
      </label>
      <button type="button" id="sb-reset-colors">Reset</button>
    </div>

    ${
        res.themeToggle
            ? `<div class="group">
      <span class="ctlLabel">Theme</span>
      <div class="segmented" role="group" aria-label="Theme">
        <button type="button" data-theme-set="light" aria-pressed="false">Light</button>
        <button type="button" data-theme-set="dark" aria-pressed="false">Dark</button>
      </div>
    </div>`
            : ''
    }
  </div>

  ${chartBlock('time', `Time — ${result.time_class}`)}
  ${result.space_class ? chartBlock('space', `Memory — ${result.space_class}`) : ''}

  <h2 style="margin-top:26px">Measurements</h2>
  ${table(result)}

  <p class="note">
    The orange dashed line is the class that fits your data best. The faint
    lines are the classes just above and below it, drawn the same way. If your
    points follow a faint line more closely than the orange one, do not trust
    the answer. Turn on the log scale to check: on a log scale every class is a
    straight line, so the one your points lie along is the real answer. All of
    this comes from timing real runs, so treat it as a good guess, not a proof.
  </p>

  <script type="application/json" id="sb-data">${dataJson}</script>
  ${bridge}
  <script${nonce} src="${res.js}"></script>
</body>
</html>`;
}

/**
 * Only a hex colour gets written to settings. The value comes from the
 * webview, and it ends up inside a <style> block when the page is rebuilt.
 */
export function safeColor(value: string): string | undefined {
    const v = value.trim();
    return /^#(?:[0-9a-fA-F]{3,4}|[0-9a-fA-F]{6}|[0-9a-fA-F]{8})$/.test(v) ? v : undefined;
}
