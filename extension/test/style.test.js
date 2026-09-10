// chart.js toggles classes that only chart.css gives meaning to. If a rule is
// renamed or dropped on one side, hover and highlighting stop working with no
// error anywhere, so the coupling is asserted here.

const { test, describe } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const { MEDIA } = require('./helpers');

const css = fs.readFileSync(path.join(MEDIA, 'chart.css'), 'utf8');
const js = fs.readFileSync(path.join(MEDIA, 'chart.js'), 'utf8');

describe('classes the script toggles must exist in the stylesheet', () => {
    for (const name of ['curveOn', 'curveOff', 'curveHover', 'panning', 'on']) {
        test(`.${name}`, () => {
            assert.ok(js.includes(`'${name}'`), `chart.js never toggles ${name}`);
            assert.match(css, new RegExp(`\\.${name}\\b`), `chart.css never defines .${name}`);
        });
    }
});

describe('hover targets', () => {
    test('curves get a wide invisible hit path', () => {
        // A 1px dotted line cannot be hovered directly.
        assert.match(css, /\.hit\s*\{[^}]*stroke-width:\s*(\d+)/);
        const width = Number(css.match(/\.hit\s*\{[^}]*stroke-width:\s*(\d+)/)[1]);
        assert.ok(width >= 10, `hit band is only ${width}px wide`);
    });

    test('the hit path catches the stroke, not its bounding box', () => {
        // Without this, one curve's box would swallow hovers meant for another.
        assert.match(css, /\.hit\s*\{[^}]*pointer-events:\s*stroke/);
    });

    test('the script marks every curve and its legend row', () => {
        assert.match(js, /data-curve="/);
        assert.match(js, /data-hit="/);
        assert.match(js, /legendHit/);
    });

    test('the legend row has a transparent box so the whole row is hoverable', () => {
        assert.match(css, /\.legendHit\s*\{[^}]*fill:\s*transparent/);
    });
});

describe('drag must not select the page text', () => {
    test('the chart disables text selection', () => {
        assert.match(css, /\.chart\s*\{[^}]*user-select:\s*none/s);
    });
    test('and the script cancels the default drag', () => {
        assert.match(js, /selectstart/);
        assert.match(js, /preventDefault/);
    });
});

describe('the wheel is not hijacked', () => {
    test('zoom requires ctrl or meta, so a plain wheel scrolls the page', () => {
        assert.match(js, /!evt\.ctrlKey && !evt\.metaKey/);
    });
});

describe('theming', () => {
    test('dark values are declared for the VS Code class and for the OS setting', () => {
        assert.match(css, /body\.vscode-dark/);
        assert.match(css, /prefers-color-scheme: dark/);
    });

    test('an explicit light theme still wins over OS dark', () => {
        assert.match(css, /:not\(\.vscode-light\)/);
    });

    test('marks read their colour from a variable, never a literal', () => {
        for (const rule of ['.measured', '.fit', '.ref']) {
            const body = css.match(new RegExp(`\\${rule}\\s*\\{([^}]*)\\}`))[1];
            assert.match(body, /var\(--sb-/, `${rule} does not use a colour variable`);
        }
    });

    test('text keeps text colours rather than a series colour', () => {
        const tick = css.match(/\.tick,\s*\.legend\s*\{([^}]*)\}/)[1];
        assert.match(tick, /var\(--sb-muted\)/);
        assert.ok(!/--sb-measured|--sb-fitted/.test(tick));
    });
});
