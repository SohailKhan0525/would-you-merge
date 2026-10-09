'use strict';
const test = require('node:test');
const assert = require('node:assert/strict');
const { chunk } = require('./chunk');

test('keeps the last, partial chunk', () => {
  assert.deepEqual(chunk([1, 2, 3, 4, 5], 2), [[1, 2], [3, 4], [5]]);
});

test('exact multiples keep every chunk', () => {
  assert.deepEqual(chunk([1, 2, 3, 4], 2), [[1, 2], [3, 4]]);
});

test('size bigger than the array gives one chunk', () => {
  assert.deepEqual(chunk([1, 2], 5), [[1, 2]]);
});

test('empty input gives no chunks', () => {
  assert.deepEqual(chunk([], 3), []);
});

test('rejects sizes below one', () => {
  assert.throws(() => chunk([1, 2, 3], 0), RangeError);
  assert.throws(() => chunk([1, 2, 3], 1.5), RangeError);
});
