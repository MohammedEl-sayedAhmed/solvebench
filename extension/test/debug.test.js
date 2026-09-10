// Path handling: which files are solutions, and what to call the scripts with.

const { test, describe } = require('node:test');
const assert = require('node:assert/strict');
const { load, REPO } = require('./helpers');

const { solutionRef, problemId, javaMainClass, debugTargetFor } = load('debug.js');
const root = { fsPath: REPO };
const uri = (rel) => ({ fsPath: `${REPO}/${rel}` });

describe('solutionRef', () => {
    test('recognises a python solution', () => {
        const ref = solutionRef(uri('python/leetcode/easy/two_sum.py'), root);
        assert.equal(ref.language, 'python');
        assert.equal(ref.relPath, 'python/leetcode/easy/two_sum.py');
    });

    test('recognises a java solution', () => {
        assert.equal(solutionRef(uri('java/leetcode/easy/TwoSum.java'), root).language, 'java');
    });

    for (const [what, rel] of [
        ['a shared test helper', 'python/common/test_framework.py'],
        ['a file at the repo root', 'run.py'],
        ['a non-language folder', 'docs/index.html'],
        ['the wrong extension for its folder', 'python/leetcode/easy/notes.txt'],
    ]) {
        test(`ignores ${what}`, () => {
            assert.equal(solutionRef(uri(rel), root), undefined);
        });
    }

    test('ignores a path outside the repo', () => {
        assert.equal(solutionRef({ fsPath: '/elsewhere/python/leetcode/a.py' }, root), undefined);
    });

    test('accepts a file straight under a language folder, as run.py does', () => {
        // discover() in run.py gives these platform "(root)" rather than
        // skipping them, so the extension has to agree or the tree would miss
        // a solution the runner still runs.
        const ref = solutionRef(uri('python/orphan.py'), root);
        assert.equal(ref.language, 'python');
        assert.equal(ref.relPath, 'python/orphan.py');
    });
});

describe('problemId', () => {
    // run.py and complexity.py both take platform/group/name. Passing a full
    // path made complexity.py fail; passing the folder made run.py run every
    // problem of that difficulty.
    const cases = [
        ['python/leetcode/easy/two_sum.py', 'leetcode/easy/two_sum'],
        ['java/leetcode/easy/TwoSum.java', 'leetcode/easy/TwoSum'],
        ['python/codewars/flatten.py', 'codewars/flatten'],
        ['python/adventofcode/2021/10/syntax_scoring.py', 'adventofcode/2021/10/syntax_scoring'],
    ];
    for (const [rel, want] of cases) {
        test(`${rel} -> ${want}`, () => {
            assert.equal(problemId(solutionRef(uri(rel), root)), want);
        });
    }

    test('never keeps the language folder or the extension', () => {
        for (const [rel] of cases) {
            const id = problemId(solutionRef(uri(rel), root));
            assert.ok(!/^(python|java|cpp|javascript|go|rust)\//.test(id), id);
            assert.ok(!/\.\w+$/.test(id), id);
        }
    });
});

describe('javaMainClass', () => {
    test('builds the class name from the path', () => {
        assert.equal(javaMainClass('java/leetcode/easy/TwoSum.java'), 'leetcode.easy.TwoSum');
    });
    test('keeps a leading underscore (a class cannot start with a digit)', () => {
        assert.equal(javaMainClass('java/leetcode/medium/_3sum.java'), 'leetcode.medium._3sum');
    });
});

describe('debugTargetFor', () => {
    test('says which extension a go solution would need', () => {
        const target = debugTargetFor(
            { language: 'go', relPath: 'go/leetcode/easy/x.go', fsPath: '/repo/go/leetcode/easy/x.go' },
            root
        );
        assert.equal(target.kind, 'unsupported');
        assert.match(target.reason, /Go extension/);
    });
});
