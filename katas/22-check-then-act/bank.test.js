'use strict';
const test = require('node:test');
const assert = require('node:assert/strict');
const { withdraw } = require('./bank');

test('two concurrent withdrawals cannot overdraw the account', async () => {
  const account = { balance: 100 };
  const results = await Promise.all([withdraw(account, 80), withdraw(account, 80)]);
  assert.equal(results.filter(Boolean).length, 1);
  assert.equal(account.balance, 20);
});

test('sequential withdrawals still work', async () => {
  const account = { balance: 100 };
  const results = [];
  for (let i = 0; i < 4; i += 1) results.push(await withdraw(account, 30));
  assert.deepEqual(results, [true, true, true, false]);
  assert.equal(account.balance, 10);
});

test('many parallel small withdrawals never go negative', async () => {
  const account = { balance: 50 };
  const results = await Promise.all(Array.from({ length: 20 }, () => withdraw(account, 10)));
  assert.equal(results.filter(Boolean).length, 5);
  assert.equal(account.balance, 0);
});
