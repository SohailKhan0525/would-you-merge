'use strict';

const BLOCKED = new Set(['__proto__', 'constructor', 'prototype']);
const isPlainObject = (value) => value !== null && typeof value === 'object' && !Array.isArray(value);

/**
 * Deep-merge `source` into `target` (mutating and returning `target`).
 * Plain objects are merged recursively; everything else is copied over.
 *
 * `source` may come straight from JSON.parse() of an untrusted request body,
 * so it must never be able to change Object.prototype.
 */
function merge(target, source) {
  for (const key of Object.keys(source)) {
    if (BLOCKED.has(key)) continue;
    const value = source[key];
    if (isPlainObject(value)) {
      const existing = Object.prototype.hasOwnProperty.call(target, key) ? target[key] : undefined;
      target[key] = merge(isPlainObject(existing) ? existing : {}, value);
    } else {
      target[key] = value;
    }
  }
  return target;
}

module.exports = { merge };
