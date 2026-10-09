'use strict';
const test = require('node:test');
const assert = require('node:assert/strict');
const { topThree } = require('./leaderboard');

test('returns the three highest scores, ascending', () => {
  assert.deepEqual(topThree([5, 10, 1, 100, 25]), [10, 25, 100]);
});

test('works with fewer than three scores', () => {
  assert.deepEqual(topThree([11, 2]), [2, 11]);
});

test('does not modify its input', () => {
  const scores = [5, 10, 1, 100, 25];
  topThree(scores);
  assert.deepEqual(scores, [5, 10, 1, 100, 25]);
});
