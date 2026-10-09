'use strict';

/**
 * Parse a quantity typed into an order form.
 * - returns a non-negative integer ("0" is a valid quantity)
 * - surrounding whitespace is fine
 * - anything that isn't a whole number ('', 'abc', '3.5', '12abc', '-2', '1e3')
 *   throws a RangeError
 */
function parseQuantity(input) {
  const text = String(input).trim();
  if (!/^\d+$/.test(text)) {
    throw new RangeError(`invalid quantity: ${JSON.stringify(input)}`);
  }
  return Number(text);
}

module.exports = { parseQuantity };
