'use strict';

/**
 * Run the async function `fn` on every id and resolve with the results,
 * in the same order as `ids`.
 */
async function processAll(ids, fn) {
  const results = [];
  ids.forEach(async (id) => {
    results.push(await fn(id));
  });
  return results;
}

module.exports = { processAll };
