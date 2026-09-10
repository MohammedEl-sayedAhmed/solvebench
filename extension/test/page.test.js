// The complexity page: security posture, controls, and the table.

const { test, describe } = require('node:test');
const assert = require('node:assert/strict');
const { load, sampleResult } = require('./helpers');

const { page, safeColor } = load('complexityPage.js');
const result = sampleResult();

const webview = () =>
    page(result, {
        css: 'https://file+.vscode-resource/x/chart.css',
        js: 'https://file+.vscode-resource/x/chart.js',
        nonce: 'testnonce123',
        cspSource: 'https://file+.vscode-resource',
    });
const preview = () => page(result, { css: '/chart.css', js: '/chart.js', themeToggle: true });

describe('content security policy', () => {
    test('nothing loads by default', () => {
        assert.match(webview(), /default-src 'none'/);
    });

    test('only the nonced script may run', () => {
        assert.match(webview(), /script-src 'nonce-testnonce123'/);
    });

    test('every executable script tag carries the nonce', () => {
        const html = webview();
        const tags = html.match(/<script[^>]*>/g) || [];
        for (const tag of tags) {
            const isData = tag.includes('type="application/json"');
            assert.ok(
                isData || tag.includes('nonce="testnonce123"'),
                `script tag without a nonce: ${tag}`
            );
        }
    });

    test('the preview emits no inline script at all', () => {
        // Its CSP has no nonce, so an inline script would just be blocked.
        const html = preview();
        const inline = (html.match(/<script(?![^>]*(?:src=|type="application\/json"))[^>]*>/g) || []);
        assert.deepEqual(inline, []);
    });

    test('the host bridge is webview-only', () => {
        assert.match(webview(), /acquireVsCodeApi/);
        assert.ok(!preview().includes('acquireVsCodeApi'));
    });
});

describe('controls', () => {
    test('scale is a two-state segmented control, not a lone toggle', () => {
        const html = webview();
        assert.match(html, /data-scale="linear"[^>]*aria-pressed="true"/);
        assert.match(html, /data-scale="log"[^>]*aria-pressed="false"/);
    });

    test('each chart gets its own zoom buttons', () => {
        const html = webview();
        for (const act of ['out', 'in', 'fit']) {
            assert.match(html, new RegExp(`data-zoom="time" data-act="${act}"`));
            assert.match(html, new RegExp(`data-zoom="space" data-act="${act}"`));
        }
    });

    test('zoom and pan are explained next to each chart', () => {
        const hints = webview().match(/class="chartHint"/g) || [];
        assert.equal(hints.length, 2);
        assert.match(webview(), /Drag to pan/);
    });

    test('the theme switch is preview-only; the editor decides in VS Code', () => {
        assert.match(preview(), /data-theme-set="dark"/);
        assert.ok(!webview().includes('data-theme-set'));
    });
});

describe('data handed to the browser', () => {
    const parse = (html) =>
        JSON.parse(html.match(/id="sb-data">([\s\S]*?)<\/script>/)[1].replace(/\\u003c/g, '<'));

    test('both series are present with their fitted class', () => {
        const data = parse(webview());
        assert.equal(data.series.time.fitted, 'O(n log n)');
        assert.equal(data.series.space.fitted, 'O(n log n)');
    });

    test('seconds become milliseconds and bytes become KB', () => {
        const data = parse(webview());
        assert.ok(Math.abs(data.series.time.values.at(-1) - 1.2) < 1e-9);
        assert.ok(Math.abs(data.series.space.values.at(-1) - 293) < 1e-9);
    });

    test('a "</script>" in the data cannot end the block early', () => {
        const nasty = { ...sampleResult(), function: 'x', inputs: '</script><script>bad()</script>' };
        const html = page(nasty, { css: '/c', js: '/j' });
        const dataBlock = html.match(/id="sb-data">([\s\S]*?)<\/script>/)[1];
        assert.ok(!dataBlock.includes('<script'));
    });

    test('svgs ship empty; the browser draws them', () => {
        assert.match(webview(), /<svg[^>]*><\/svg>/);
    });
});

describe('measurements table', () => {
    test('a column uses one decimal count throughout', () => {
        // It showed 0.060, 0.126, ... and then a bare 1.2, which read as a typo.
        const body = webview().match(/<tbody>([\s\S]*?)<\/tbody>/)[1];
        const times = [...body.matchAll(/<td>[\d,]+<\/td><td>([\d.,]+)<\/td>/g)].map((m) => m[1]);
        assert.equal(times.length, 5);
        const widths = new Set(times.map((s) => (s.split('.')[1] || '').length));
        assert.equal(widths.size, 1, `mixed decimals: ${times.join(', ')}`);
    });

    test('a shorter space series leaves a gap rather than a wrong number', () => {
        const partial = { ...sampleResult(), spaces: [14336, 30720] };
        const body = page(partial, { css: '/c', js: '/j' }).match(/<tbody>([\s\S]*?)<\/tbody>/)[1];
        assert.equal((body.match(/—/g) || []).length, 3);
    });
});

describe('safeColor', () => {
    // The value reaches a <style> block, so it must not be able to close it.
    for (const good of ['#fff', '#ffff', '#2a78d6', '#2a78d6ff']) {
        test(`accepts ${good}`, () => assert.equal(safeColor(good), good));
    }
    for (const bad of [
        'red',
        'rgb(1,2,3)',
        '#fff; } body { display: none',
        'url(http://example.test/x)',
        '</style><script>bad()</script>',
        'var(--sb-measured)',
        '',
    ]) {
        test(`rejects ${JSON.stringify(bad)}`, () => assert.equal(safeColor(bad), undefined));
    }
});
