# 13 · Done before it started

`javascript` · ⏳ `async` · level ★★☆

> 🤖 **The prompt:** "Write processAll(ids, fn) that runs an async function on each id and returns the results in order."

`async` and `await` are right there. Surely it waits for them.

```javascript
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
```

**Would you approve this PR?** Take a minute. Then try to break it.

## Your turn

Fix [`batch.js`](./batch.js) so the tests pass. **Don't edit the tests.**

```bash
python tools/check.py 13
```

Want a clean slate? `python tools/check.py --reset 13` restores the original file.

<details>
<summary>💡 Hint</summary>

What does `ids.forEach(...)` return? Does `forEach` wait for the promises that an `async` callback hands back?

</details>

<details>
<summary>🔓 Spoiler: the bug, and why AI writes it</summary>

`forEach` ignores the promises returned by an `async` callback, so `processAll` returns the (still empty) `results` array **before any work has finished**. Rejections inside the callback become unhandled and get lost.

Use `await Promise.all(ids.map(fn))` for parallel work, or a `for...of` loop with `await` for sequential work.

**A fix** (also in [`solutions/13-foreach-async/`](../../solutions/13-foreach-async/))

```javascript
'use strict';

/**
 * Run the async function `fn` on every id and resolve with the results,
 * in the same order as `ids`.
 */
async function processAll(ids, fn) {
  return Promise.all(ids.map((id) => fn(id)));
}

module.exports = { processAll };
```

**Go deeper**

- [MDN: Array.prototype.forEach()](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/forEach)

</details>
