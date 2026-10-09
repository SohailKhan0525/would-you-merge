'use strict';
const test = require('node:test');
const assert = require('node:assert/strict');
const { merge } = require('./merge');

test('merges nested objects', () => {
  assert.deepEqual(merge({ a: { b: 1 } }, { a: { c: 2 }, d: 3 }), { a: { b: 1, c: 2 }, d: 3 });
});

test('later values win', () => {
  assert.deepEqual(merge({ a: 1, b: { c: 1 } }, { a: 2, b: { c: 2 } }), { a: 2, b: { c: 2 } });
});

test('cannot pollute Object.prototype through __proto__', (t) => {
  t.after(() => {
    delete Object.prototype.polluted;
  });
  merge({}, JSON.parse('{"__proto__": {"polluted": "yes"}}'));
  assert.equal({}.polluted, undefined);
});

test('cannot pollute Object.prototype through constructor.prototype', (t) => {
  t.after(() => {
    delete Object.prototype.polluted2;
  });
  merge({}, JSON.parse('{"constructor": {"prototype": {"polluted2": "yes"}}}'));
  assert.equal({}.polluted2, undefined);
});
