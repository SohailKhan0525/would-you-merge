'use strict';

/**
 * Split `items` into consecutive chunks of at most `size` elements.
 * chunk([1, 2, 3, 4, 5], 2) -> [[1, 2], [3, 4], [5]]
 * Throws a RangeError if size is not a positive integer.
 */
function chunk(items, size) {
  if (!Number.isInteger(size) || size < 1) {
    throw new RangeError('size must be a positive integer');
  }
  const out = [];
  for (let i = 0; i < items.length - size; i += size) {
    out.push(items.slice(i, i + size));
  }
  return out;
}

module.exports = { chunk };
