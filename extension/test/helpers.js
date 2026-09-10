// Shared test helpers.
//
// The extension modules import 'vscode', which only exists inside the editor.
// stubVscode() installs a fake before they are required, so the parts that do
// not actually need the editor can be tested in plain Node.

const Module = require('module');
const path = require('path');

const OUT = path.resolve(__dirname, '..', 'out');
const MEDIA = path.resolve(__dirname, '..', 'media');
const REPO = path.resolve(__dirname, '..', '..');

let installed = false;
let settings = {};

/** Install the 'vscode' stub. Safe to call more than once. */
function stubVscode() {
    if (installed) {
        return;
    }
    const stub = {
        workspace: {
            getConfiguration: () => ({
                get: (key, fallback) => (settings[key] !== undefined ? settings[key] : fallback),
            }),
        },
        window: {},
        ViewColumn: { Beside: 2 },
        ProgressLocation: { Notification: 15 },
        ConfigurationTarget: { Global: 1 },
        Uri: {},
    };
    const realLoad = Module._load;
    Module._load = (request, parent, isMain) =>
        request === 'vscode' ? stub : realLoad(request, parent, isMain);
    installed = true;
}

/** Set the values the stubbed configuration returns. */
function setSettings(values) {
    settings = values || {};
}

/** Load a compiled extension module (stubbing vscode first). */
function load(name) {
    stubVscode();
    return require(path.join(OUT, name));
}

/**
 * Load media/chart.js and return the internals it exposes. It is an IIFE built
 * for a browser, so it gets a global `window` and no DOM; it returns early when
 * there is no `document`.
 */
function loadChartJs() {
    if (!global.window) {
        global.window = global;
    }
    require(path.join(MEDIA, 'chart.js'));
    return global.sbInternals;
}

/** A fixed measurement result, so page tests do not have to run Python. */
function sampleResult() {
    return {
        schema: 1,
        solution: 'python/leetcode/easy/two_sum.py',
        lang: 'py',
        function: 'twoSum',
        inputs: 'auto-generated from type hints (nums: list, target: int)',
        sizes: [500, 1000, 2000, 4000, 8000],
        times: [0.00006, 0.000126, 0.000253, 0.000537, 0.0012],
        time_class: 'O(n log n)',
        spaces: [14336, 30720, 68608, 146432, 300032],
        space_class: 'O(n log n)',
    };
}

module.exports = { stubVscode, setSettings, load, loadChartJs, sampleResult, OUT, MEDIA, REPO };
