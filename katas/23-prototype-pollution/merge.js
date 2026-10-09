'use strict';

/**
 * Deep-merge `source` into `target` (mutating and returning `target`).
 * Plain objects are merged recursively; everything else is copied over.
 *
 * `source` may come straight from JSON.parse() of an untrusted request body,
 * so it must never be able to change Object.prototype.
 */
function merge(target, source) {
  for (const key in source) {
    if (typeof source[key] === 'object' && source[key] !== null) {
      target[key] = merge(target[key] || {}, source[key]);
    } else {
      target[key] = source[key];
    }
  }
  return target;
}

module.exports = { merge };
