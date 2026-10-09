'use strict';
const test = require('node:test');
const assert = require('node:assert/strict');
const { logRequest } = require('./requestlog');

function makeReq() {
  return {
    method: 'GET',
    url: 'https://api.example.com/v1/me',
    headers: { Authorization: 'Bearer sk-live-123', cookie: 'sid=abc', Accept: 'application/json' },
  };
}

function captureLogs(t, fn) {
  const spy = t.mock.method(console, 'log', () => {});
  fn();
  return spy.mock.calls.map((call) => call.arguments.map(String).join(' ')).join('\n');
}

test('still logs the method, url and harmless headers', (t) => {
  const out = captureLogs(t, () => logRequest(makeReq()));
  for (const needle of ['GET', 'https://api.example.com/v1/me', 'Accept', 'application/json']) {
    assert.ok(out.includes(needle), `missing ${needle} in: ${out}`);
  }
});

test('never logs credentials', (t) => {
  const out = captureLogs(t, () => logRequest(makeReq()));
  assert.ok(!out.includes('sk-live-123'), out);
  assert.ok(!out.includes('sid=abc'), out);
  assert.ok(out.includes('[REDACTED]'), out);
});

test('does not alter the real request', (t) => {
  const req = makeReq();
  captureLogs(t, () => logRequest(req));
  assert.equal(req.headers.Authorization, 'Bearer sk-live-123');
  assert.equal(req.headers.cookie, 'sid=abc');
});
