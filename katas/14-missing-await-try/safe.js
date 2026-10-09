'use strict';

/**
 * Call `fn` (sync or async) and resolve with its result.
 * If it throws or rejects, resolve with `fallback` instead (default: null).
 */
async function safe(fn, fallback = null) {
  try {
    return fn();
  } catch (err) {
    return fallback;
  }
}

module.exports = { safe };
