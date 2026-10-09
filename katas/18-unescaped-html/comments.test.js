'use strict';
const test = require('node:test');
const assert = require('node:assert/strict');
const { renderComment } = require('./comments');

test('renders a normal comment exactly', () => {
  assert.equal(
    renderComment({ author: 'Ann', text: 'Hi' }),
    '<div class="comment"><b>Ann</b>: Hi</div>',
  );
});

test('escapes ampersands', () => {
  const html = renderComment({ author: 'Ann', text: 'Tom & Jerry' });
  assert.ok(html.includes('Tom &amp; Jerry'), html);
});

test('neutralises script tags in the text', () => {
  const html = renderComment({ author: 'x', text: '<script>alert(1)</script>' });
  assert.ok(!html.includes('<script'), html);
  assert.ok(html.includes('&lt;script&gt;'), html);
});

test('neutralises markup in the author name', () => {
  const html = renderComment({ author: '<img src=x onerror=alert(1)>', text: 'hi' });
  assert.ok(!html.includes('<img'), html);
});
