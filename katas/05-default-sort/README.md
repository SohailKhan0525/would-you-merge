# 05 · Ten is smaller than nine

`javascript` · 🧠 `logic` · level ★☆☆

> 🤖 **The prompt:** "Return the three highest scores."

Looks fine on `[3, 1, 2]`. Single-digit examples hide this one.

```javascript
'use strict';

/**
 * Return the three highest scores, in ascending order.
 * Must not modify the array that was passed in.
 */
function topThree(scores) {
  return scores.sort().slice(-3);
}

module.exports = { topThree };
```

**Would you approve this PR?** Take a minute. Then try to break it.

## Your turn

Fix [`leaderboard.js`](./leaderboard.js) so the tests pass. **Don't edit the tests.**

```bash
python tools/check.py 05
```

Want a clean slate? `python tools/check.py --reset 05` restores the original file.

<details>
<summary>💡 Hint</summary>

What does `[10, 9, 1].sort()` print in your console? And does `sort` work on a copy?

</details>

<details>
<summary>🔓 Spoiler: the bug, and why AI writes it</summary>

`Array.prototype.sort()` without a comparator sorts by **string value** (`'10' < '9'`), and it sorts **in place**, mutating the caller's array. Both are invisible with tiny single-digit examples.

Always pass a numeric comparator (`(a, b) => a - b`) and copy first (`[...arr]`, or `toSorted()` on modern runtimes).

**A fix** (also in [`solutions/05-default-sort/`](../../solutions/05-default-sort/))

```javascript
'use strict';

/**
 * Return the three highest scores, in ascending order.
 * Must not modify the array that was passed in.
 */
function topThree(scores) {
  return [...scores].sort((a, b) => a - b).slice(-3);
}

module.exports = { topThree };
```

**Go deeper**

- [MDN: Array.prototype.sort()](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/sort)

</details>
