'use strict';
const test = require('node:test');
const assert = require('node:assert/strict');
const { processAll } = require('./batch');

const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

test('resolves with every result, in input order', async () => {
  const out = await processAll([1, 2, 3], async (n) => {
    await sleep(n === 1 ? 20 : 1); // the first one finishes last
    return n * 2;
  });
  assert.deepEqual(out, [2, 4, 6]);
});

test('has finished all the work by the time it resolves', async () => {
  let done = 0;
  await processAll([1, 2, 3, 4], async () => {
    await sleep(5);
    done += 1;
  });
  assert.equal(done, 4);
});

test('handles empty input', async () => {
  assert.deepEqual(await processAll([], async (x) => x), []);
});
