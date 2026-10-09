# 14 · A try/catch that catches nothing

`javascript` · ⏳ `async` · level ★★☆

> 🤖 **The prompt:** "Write safe(fn) that calls an async function and returns a fallback instead of throwing."

It has the try. It has the catch. It even has a default parameter. Ship it?

```javascript
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
```

**Would you approve this PR?** Take a minute. Then try to break it.

## Your turn

Fix [`safe.js`](./safe.js) so the tests pass. **Don't edit the tests.**

```bash
python tools/check.py 14
```

Want a clean slate? `python tools/check.py --reset 14` restores the original file.

<details>
<summary>💡 Hint</summary>

When does the promise returned by `fn()` *reject*: while the `try` block is still running, or after the function has already returned it?

</details>

<details>
<summary>🔓 Spoiler: the bug, and why AI writes it</summary>

`return fn()` hands the **pending promise** back to the caller; the `try` block has already finished by the time it rejects, so the `catch` never runs and the error escapes. Inside a `try`, write `return await fn()`.

Outside `try/catch`, `return promise` and `return await promise` behave the same, which is exactly why this mistake survives so many reviews.

**A fix** (also in [`solutions/14-missing-await-try/`](../../solutions/14-missing-await-try/))

```javascript
'use strict';

/**
 * Call `fn` (sync or async) and resolve with its result.
 * If it throws or rejects, resolve with `fallback` instead (default: null).
 */
async function safe(fn, fallback = null) {
  try {
    return await fn();
  } catch (err) {
    return fallback;
  }
}

module.exports = { safe };
```

</details>
