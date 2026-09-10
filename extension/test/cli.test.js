// The contract between the extension and the Python scripts.
//
// The extension parses this JSON and feeds paths back as filters, so a change
// to either shape breaks the test panel. These tests run the real scripts.

const { test, describe } = require('node:test');
const assert = require('node:assert/strict');
const { execFileSync } = require('node:child_process');
const fs = require('node:fs');
const path = require('node:path');
const { REPO, loadChartJs } = require('./helpers');

/** Prefer the repo's venv, as the extension does, then fall back to PATH. */
function python() {
    const venv =
        process.platform === 'win32'
            ? path.join(REPO, '.venv', 'Scripts', 'python.exe')
            : path.join(REPO, '.venv', 'bin', 'python');
    if (fs.existsSync(venv)) {
        return venv;
    }
    return process.platform === 'win32' ? 'python' : 'python3';
}

const PY = python();

function run(args, expectFailure = false) {
    try {
        const stdout = execFileSync(PY, args, { cwd: REPO, maxBuffer: 1 << 24 }).toString();
        return { stdout, status: 0 };
    } catch (err) {
        if (!expectFailure) {
            throw new Error(`${args.join(' ')} failed: ${err.stderr || err.message}`);
        }
        return { stdout: (err.stdout || '').toString(), status: err.status };
    }
}

describe('run.py --stats --json', () => {
    const payload = JSON.parse(run(['run.py', '--stats', '--json']).stdout);

    test('stdout is JSON and nothing else', () => {
        assert.equal(payload.schema, 1);
        assert.ok(Array.isArray(payload.solutions));
    });

    test('discovery only, so there is no summary', () => {
        assert.equal(payload.summary, undefined);
    });

    test('every solution carries the fields the tree is built from', () => {
        for (const s of payload.solutions) {
            for (const key of ['language', 'lang', 'platform', 'group', 'name', 'path']) {
                assert.ok(key in s, `${key} missing from ${JSON.stringify(s)}`);
            }
        }
    });

    test('paths are unique, since they are used as test item ids', () => {
        const paths = payload.solutions.map((s) => s.path);
        assert.equal(new Set(paths).size, paths.length);
    });

    test('paths use forward slashes on every OS', () => {
        for (const s of payload.solutions) {
            assert.ok(!s.path.includes('\\'), s.path);
        }
    });

    test('the count matches the text output', () => {
        const text = run(['run.py', '--stats']).stdout;
        const total = Number(text.match(/TOTAL\s+(\d+)/)[1]);
        assert.equal(payload.solutions.length, total);
    });

    test('a reported path selects exactly its own solution', () => {
        // The test panel sends these back as filters. If one matched more than
        // itself, running a single test would run several.
        for (const s of payload.solutions.slice(0, 6)) {
            const one = JSON.parse(run(['run.py', '--stats', '--json', s.path]).stdout);
            assert.deepEqual(one.solutions.map((x) => x.path), [s.path]);
        }
    });

    test('a filter that matches nothing is still valid JSON, and exits 1', () => {
        const { stdout, status } = run(
            ['run.py', '--stats', '--json', 'definitely-not-a-solution'],
            true
        );
        assert.deepEqual(JSON.parse(stdout).solutions, []);
        assert.equal(status, 1);
    });
});

describe('run.py --json', () => {
    const payload = JSON.parse(run(['run.py', '--json', 'leetcode/easy/two_sum']).stdout);

    test('reports a status and a duration per solution', () => {
        assert.ok(payload.solutions.length >= 1);
        for (const s of payload.solutions) {
            assert.ok(['pass', 'fail'].includes(s.status), s.status);
            assert.equal(typeof s.seconds, 'number');
            assert.equal(typeof s.output, 'string');
        }
    });

    test('the summary adds up', () => {
        const { pass, fail, total } = payload.summary;
        assert.equal(pass + fail, total);
        assert.equal(total, payload.solutions.length);
    });

    test('a problem id runs every language it is solved in', () => {
        // This is what Run Current Solution passes.
        assert.ok(payload.solutions.length >= 2, 'two_sum should be solved in py and java');
        assert.deepEqual(
            [...new Set(payload.solutions.map((s) => s.lang))].sort(),
            ['java', 'py']
        );
    });

    test('a failing solution exits 1 and says so in the JSON', () => {
        const temp = path.join(REPO, 'python', 'others', '_cli_test_failure.py');
        fs.writeFileSync(temp, 'import sys\nprint("expected failure")\nsys.exit(1)\n');
        try {
            const { stdout, status } = run(['run.py', '--json', '_cli_test_failure'], true);
            const one = JSON.parse(stdout);
            assert.equal(status, 1);
            assert.equal(one.solutions[0].status, 'fail');
            assert.equal(one.summary.fail, 1);
            assert.match(one.solutions[0].output, /expected failure/);
        } finally {
            fs.unlinkSync(temp);
        }
    });
});

describe('complexity.py --json', () => {
    // Small sizes: this runs the solution for real.
    const payload = JSON.parse(
        run([
            'complexity.py',
            'leetcode/easy/two_sum',
            '--json',
            '--sizes',
            '200,400,800,1600',
        ]).stdout
    );

    test('stdout is JSON, with the hint kept off it', () => {
        // The "also solved in java" hint used to print to stdout and corrupt this.
        assert.equal(payload.schema, 1);
        assert.equal(payload.lang, 'py');
    });

    test('carries the points the chart draws', () => {
        assert.equal(payload.sizes.length, payload.times.length);
        assert.ok(payload.sizes.length >= 3);
        assert.match(payload.time_class, /^O\(/);
    });

    test('the class it reports is the one chart.js would draw', () => {
        const I = loadChartJs();
        const names = I.MODELS.map((m) => m.name);
        assert.ok(names.includes(payload.time_class), payload.time_class);
        if (payload.space_class) {
            assert.ok(names.includes(payload.space_class), payload.space_class);
        }
    });

    test('the fitted curve stays near the measurements', () => {
        const I = loadChartJs();
        const model = I.MODELS.find((m) => m.name === payload.time_class);
        const c = I.fitScale(payload.sizes, payload.times, model.f);
        for (let i = 0; i < payload.sizes.length; i++) {
            const ratio = (c * model.f(payload.sizes[i])) / payload.times[i];
            assert.ok(Math.max(ratio, 1 / ratio) < 3, `point ${i} off by ${ratio.toFixed(2)}x`);
        }
    });
});
