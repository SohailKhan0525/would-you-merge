# 07 · The chunk that fell off the end

`javascript` · 📏 `boundaries` · level ★☆☆

> 🤖 **The prompt:** "Split an array into chunks of a given size."

A loop condition that *almost* reads right. Reviewers' eyes slide over `<` versus `<=`.

```javascript
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
```

**Would you approve this PR?** Take a minute. Then try to break it.

## Your turn

Fix [`chunk.js`](./chunk.js) so the tests pass. **Don't edit the tests.**

```bash
python tools/check.py 07
```

Want a clean slate? `python tools/check.py --reset 07` restores the original file.

<details>
<summary>💡 Hint</summary>

Walk through `chunk([1, 2, 3, 4], 2)` by hand: what are the values of `i`, and which ones does the loop condition allow?

</details>

<details>
<summary>🔓 Spoiler: the bug, and why AI writes it</summary>

`i < items.length - size` stops the loop one chunk early, so the final chunk is dropped: data **silently disappears** and nothing crashes. The loop should run while `i < items.length`; `slice` already handles a short final chunk.

Boundary bugs love loops. For every loop, run the tiny cases by hand: empty, one element, exact multiple, one over.

**A fix** (also in [`solutions/07-chunk-off-by-one/`](../../solutions/07-chunk-off-by-one/))

```javascript
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
  for (let i = 0; i < items.length; i += size) {
    out.push(items.slice(i, i + size));
  }
  return out;
}

module.exports = { chunk };
```

</details>
