// Grouping solutions in the test tree.

const { test, describe } = require('node:test');
const assert = require('node:assert/strict');
const { load } = require('./helpers');

const { normalise, problemTitle } = load('tests.js');

describe('normalise', () => {
    // Must match norm() in run.py, or the two languages of one problem end up
    // in different branches of the tree.
    test('two_sum and TwoSum collapse to the same key', () => {
        assert.equal(normalise('two_sum'), normalise('TwoSum'));
        assert.equal(normalise('two_sum'), 'twosum');
    });
    test('strips a leading underscore', () => {
        assert.equal(normalise('_3sum'), '3sum');
    });
});

describe('problemTitle', () => {
    test('one label for the snake_case and PascalCase spellings', () => {
        assert.equal(problemTitle('two_sum'), 'Two Sum');
        assert.equal(problemTitle('TwoSum'), 'Two Sum');
    });
    test('title-cases each word', () => {
        assert.equal(problemTitle('syntax_scoring'), 'Syntax Scoring');
    });
    test('leaves a leading-digit name alone', () => {
        assert.equal(problemTitle('_3sum'), '3sum');
    });
});
