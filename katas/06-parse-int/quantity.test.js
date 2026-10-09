'use strict';
const test = require('node:test');
const assert = require('node:assert/strict');
const { parseQuantity } = require('./quantity');

test('parses whole numbers', () => {
  assert.equal(parseQuantity('12'), 12);
  assert.equal(parseQuantity(' 7 '), 7);
});

test('zero is a valid quantity', () => {
  assert.equal(parseQuantity('0'), 0);
});

test('rejects anything that is not a whole number', () => {
  for (const bad of ['', 'abc', '3.5', '12abc', '-2', '1e3']) {
    assert.throws(() => parseQuantity(bad), RangeError, `should reject ${JSON.stringify(bad)}`);
  }
});
