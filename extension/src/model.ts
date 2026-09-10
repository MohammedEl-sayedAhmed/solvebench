// The JSON that `run.py --json` writes. Keep this in step with sol_payload()
// and emit_json() in run.py.

export interface SolutionJson {
    language: string;   // folder name: python, cpp, java, javascript, go, rust
    lang: string;       // short name: py, cpp, java, js, go, rust
    platform: string;   // leetcode, codewars, adventofcode, ...
    group: string;      // easy | medium | hard | 2021/10 | "" for no group
    name: string;       // file name without the extension
    path: string;       // relative to the repo, forward slashes, used as the id
    status?: 'pass' | 'fail';
    seconds?: number;
    output?: string;
}

export interface RunSummary {
    pass: number;
    fail: number;
    total: number;
    seconds: number;
}

export interface RunPayload {
    schema: number;
    solutions: SolutionJson[];
    summary?: RunSummary;
}

export const SCHEMA = 1;
