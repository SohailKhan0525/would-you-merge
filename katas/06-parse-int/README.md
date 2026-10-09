# 06 · Zero items, one in the cart

`javascript` · 🧮 `data` · level ★☆☆

> 🤖 **The prompt:** "Parse the quantity field from the order form."

One line, zero dependencies, very confident.

```javascript
'use strict';

/**
 * Parse a quantity typed into an order form.
 * - returns a non-negative integer ("0" is a valid quantity)
 * - surrounding whitespace is fine
 * - anything that isn't a whole number ('', 'abc', '3.5', '12abc', '-2', '1e3')
 *   throws a RangeError
 */
function parseQuantity(input) {
  return parseInt(input) || 1;
}

module.exports = { parseQuantity };
```

**Would you approve this PR?** Take a minute. Then try to break it.

## Your turn

Fix [`quantity.js`](./quantity.js) so the tests pass. **Don't edit the tests.**

```bash
python tools/check.py 06
```

Want a clean slate? `python tools/check.py --reset 06` restores the original file.

<details>
<summary>💡 Hint</summary>

Try `parseInt('0') || 1`, `parseInt('12abc')` and `parseInt('')` in a console. What does the spec say should happen for each?

</details>

<details>
<summary>🔓 Spoiler: the bug, and why AI writes it</summary>

Two classic traps in one line. `|| 1` treats `0` as "missing" (the same bug as kata 03, in another language), and `parseInt` happily parses a **prefix** (`'12abc'` becomes `12`, `'3.5'` becomes `3`) instead of rejecting bad input.

For user input, validate the *whole* string (`/^\d+$/`) before converting it.

**A fix** (also in [`solutions/06-parse-int/`](../../solutions/06-parse-int/))

```javascript
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
```

</details>
