'use strict';
const test = require('node:test');
const assert = require('node:assert/strict');
const { sign, verify } = require('./session');

const SECRET = 'correct horse battery staple';
const NOW = 1_800_000_000;
const encode = (obj) => Buffer.from(JSON.stringify(obj)).toString('base64url');

test('accepts a valid token', () => {
  const token = sign({ user: 'ann', exp: NOW + 60 }, SECRET);
  assert.deepEqual(verify(token, SECRET, NOW), { user: 'ann', exp: NOW + 60 });
});

test('rejects an expired token', () => {
  const token = sign({ user: 'ann', exp: NOW - 1 }, SECRET);
  assert.equal(verify(token, SECRET, NOW), null);
});

test('rejects a token whose payload was tampered with', () => {
  const signature = sign({ user: 'ann', exp: NOW + 60 }, SECRET).split('.')[1];
  const forged = `${encode({ user: 'admin', exp: NOW + 60 })}.${signature}`;
  assert.equal(verify(forged, SECRET, NOW), null);
});

test('rejects a token signed with a different secret', () => {
  const token = sign({ user: 'ann', exp: NOW + 60 }, 'some other secret');
  assert.equal(verify(token, SECRET, NOW), null);
});

test('rejects tokens that carry no signature', () => {
  assert.equal(verify(encode({ user: 'admin', exp: NOW + 60 }), SECRET, NOW), null);
  assert.equal(verify(`${encode({ user: 'admin', exp: NOW + 60 })}.`, SECRET, NOW), null);
});

test('rejects garbage', () => {
  for (const junk of ['', 'abc', 'a.b.c', null, undefined]) {
    assert.equal(verify(junk, SECRET, NOW), null);
  }
});
