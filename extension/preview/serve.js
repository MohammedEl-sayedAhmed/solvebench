#!/usr/bin/env node
// Preview the complexity page in a browser, outside VS Code.
//
//   npm run preview                          # measures leetcode/easy/two_sum
//   npm run preview -- leetcode/medium/three_sum
//   npm run preview -- codewars/flatten --lang java
//
// It runs the real complexity.py, builds the page with the same page() the
// extension uses, and serves it with media/chart.css and media/chart.js. So
// what you see here is what the webview shows, minus the editor theme.

const http = require('http');
const fs = require('fs');
const path = require('path');
const { execFileSync } = require('child_process');
const { page } = require('../out/complexityPage.js');   // no vscode import

const REPO = path.resolve(__dirname, '..', '..');
const MEDIA = path.resolve(__dirname, '..', 'media');
const PORT = Number(process.env.PORT || 5178);

// Flags that take a value, so their value is not mistaken for the problem.
const VALUE_FLAGS = ['--lang', '--method', '--sizes', '--repeat', '--max-seconds'];

const argv = process.argv.slice(2);
let problem = 'leetcode/easy/two_sum';
const extra = [];
for (let i = 0; i < argv.length; i++) {
    const arg = argv[i];
    if (VALUE_FLAGS.includes(arg)) {
        extra.push(arg);
        if (i + 1 < argv.length) { extra.push(argv[++i]); }
    } else if (arg.startsWith('-')) {
        extra.push(arg);
    } else {
        problem = arg;
    }
}

function python() {
    for (const candidate of [
        path.join(REPO, '.venv', 'bin', 'python'),
        'python3',
        'python',
    ]) {
        try {
            execFileSync(candidate, ['--version'], { stdio: 'ignore' });
            return candidate;
        } catch (e) { /* try the next one */ }
    }
    console.error('no python found. Run ./setup.sh, or set PATH.');
    process.exit(1);
}

function measure() {
    const py = python();
    const cmd = ['complexity.py', problem, '--json', ...extra];
    console.log(`> ${py} ${cmd.join(' ')}`);
    const out = execFileSync(py, cmd, { cwd: REPO, maxBuffer: 1 << 24 }).toString();
    return JSON.parse(out);
}

let result;
try {
    result = measure();
} catch (err) {
    console.error(`complexity.py failed:\n${err.stderr ? err.stderr.toString() : err.message}`);
    process.exit(1);
}

const html = page(result, {
    css: '/chart.css',
    js: '/chart.js',
    themeToggle: true,        // the editor is not here to decide, so offer it
});

const TYPES = { '.css': 'text/css', '.js': 'text/javascript', '.html': 'text/html' };

http.createServer((req, res) => {
    const url = req.url.split('?')[0];

    if (url === '/' || url === '/index.html') {
        res.writeHead(200, { 'content-type': 'text/html; charset=utf-8' });
        res.end(html);
        return;
    }

    // Only the two media files are served, by exact name.
    const name = path.basename(url);
    if (name === 'chart.css' || name === 'chart.js') {
        const file = path.join(MEDIA, name);
        res.writeHead(200, {
            'content-type': TYPES[path.extname(name)] + '; charset=utf-8',
            'cache-control': 'no-store',
        });
        res.end(fs.readFileSync(file));
        return;
    }

    res.writeHead(404).end('not found');
}).listen(PORT, '127.0.0.1', () => {
    console.log(`\n  ${result.function} — time ${result.time_class}` +
        (result.space_class ? ` · space ${result.space_class}` : ''));
    console.log(`  http://127.0.0.1:${PORT}\n`);
    console.log('  Edit media/chart.css or media/chart.js and reload the page.');
    console.log('  Ctrl+C to stop.\n');
});
