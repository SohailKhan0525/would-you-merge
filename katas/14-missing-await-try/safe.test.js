'use strict';
const test = require('node:test');
const assert = require('node:assert/strict');
const { safe } = require('./safe');

test('returns the value on success', async () => {
  assert.equal(await safe(async () => 42, 0), 42);
});

test('returns the fallback when the async function rejects', async () => {
  const result = await safe(async () => {
    throw new Error('boom');
  }, 'fallback');
  assert.equal(result, 'fallback');
});

test('returns the fallback when the function throws synchronously', async () => {
  const result = await safe(() => {
    throw new Error('boom');
  }, 'fallback');
  assert.equal(result, 'fallback');
});

test('the fallback defaults to null', async () => {
  assert.equal(await safe(() => Promise.reject(new Error('nope'))), null);
});
