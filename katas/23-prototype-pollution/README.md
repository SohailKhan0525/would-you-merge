# 23 · Merge, and pollute everything

`javascript` · 🔐 `security` · level ★★★

> 🤖 **The prompt:** "Write a deep merge for config objects."

Twelve lines, recursive, elegant. Also a historic source of CVEs.

```javascript
'use strict';

/**
 * Deep-merge `source` into `target` (mutating and returning `target`).
 * Plain objects are merged recursively; everything else is copied over.
 *
 * `source` may come straight from JSON.parse() of an untrusted request body,
 * so it must never be able to change Object.prototype.
 */
function merge(target, source) {
  for (const key in source) {
    if (typeof source[key] === 'object' && source[key] !== null) {
      target[key] = merge(target[key] || {}, source[key]);
    } else {
      target[key] = source[key];
    }
  }
  return target;
}

module.exports = { merge };
```

**Would you approve this PR?** Take a minute. Then try to break it.

## Your turn

Fix [`merge.js`](./merge.js) so the tests pass. **Don't edit the tests.**

```bash
python tools/check.py 23
```

Want a clean slate? `python tools/check.py --reset 23` restores the original file.

<details>
<summary>💡 Hint</summary>

What does `({})['__proto__']` return? Now think about what `JSON.parse('{"__proto__": {...}}')` produces, and what the recursion does with that key.

</details>

<details>
<summary>🔓 Spoiler: the bug, and why AI writes it</summary>

A recursive merge that blindly copies keys lets an attacker send `__proto__` (or `constructor.prototype`) and write properties onto `Object.prototype`, which then show up on **every object in the process**: *prototype pollution*. It has been behind real CVEs in popular libraries.

Skip those keys, only recurse into the target's *own* properties, or merge into `Object.create(null)` objects. And don't hand-roll deep merge for untrusted input when a vetted library fits.

**A fix** (also in [`solutions/23-prototype-pollution/`](../../solutions/23-prototype-pollution/))

```javascript
'use strict';

const BLOCKED = new Set(['__proto__', 'constructor', 'prototype']);
const isPlainObject = (value) => value !== null && typeof value === 'object' && !Array.isArray(value);

/**
 * Deep-merge `source` into `target` (mutating and returning `target`).
 * Plain objects are merged recursively; everything else is copied over.
 *
 * `source` may come straight from JSON.parse() of an untrusted request body,
 * so it must never be able to change Object.prototype.
 */
function merge(target, source) {
  for (const key of Object.keys(source)) {
    if (BLOCKED.has(key)) continue;
    const value = source[key];
    if (isPlainObject(value)) {
      const existing = Object.prototype.hasOwnProperty.call(target, key) ? target[key] : undefined;
      target[key] = merge(isPlainObject(existing) ? existing : {}, value);
    } else {
      target[key] = value;
    }
  }
  return target;
}

module.exports = { merge };
```

**Go deeper**

- [CWE-1321: Prototype pollution](https://cwe.mitre.org/data/definitions/1321.html)

</details>
