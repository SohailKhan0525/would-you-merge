'use strict';

/**
 * Run the async function `fn` on every id and resolve with the results,
 * in the same order as `ids`.
 */
async function processAll(ids, fn) {
  return Promise.all(ids.map((id) => fn(id)));
}

module.exports = { processAll };
