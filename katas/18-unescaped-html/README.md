# 18 · The comment that runs code

`javascript` · 🔐 `security` · level ★★☆

> 🤖 **The prompt:** "Render a comment as an HTML snippet."

Template literals make this a one-liner. Very readable. Very exploitable.

```javascript
'use strict';

/**
 * Render one comment as an HTML snippet:
 *   <div class="comment"><b>AUTHOR</b>: TEXT</div>
 * `author` and `text` come from users, so they must be HTML-escaped.
 */
function renderComment({ author, text }) {
  return `<div class="comment"><b>${author}</b>: ${text}</div>`;
}

module.exports = { renderComment };
```

**Would you approve this PR?** Take a minute. Then try to break it.

## Your turn

Fix [`comments.js`](./comments.js) so the tests pass. **Don't edit the tests.**

```bash
python tools/check.py 18
```

Want a clean slate? `python tools/check.py --reset 18` restores the original file.

<details>
<summary>💡 Hint</summary>

Imagine a comment whose text is `<script>...</script>`. Where does it end up, and whose browser runs it?

</details>

<details>
<summary>🔓 Spoiler: the bug, and why AI writes it</summary>

Interpolating user data into HTML without escaping is textbook **XSS**: whatever a user types becomes markup in other people's browsers. Escape `& < > " '` at the point of output, or better, use a templating engine or DOM API that escapes by default (`textContent`).

Template literals are string *concatenation*, not a safe templating system.

**A fix** (also in [`solutions/18-unescaped-html/`](../../solutions/18-unescaped-html/))

```javascript
'use strict';

const ESCAPES = { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' };
const escapeHtml = (value) => String(value).replace(/[&<>"']/g, (ch) => ESCAPES[ch]);

/**
 * Render one comment as an HTML snippet:
 *   <div class="comment"><b>AUTHOR</b>: TEXT</div>
 * `author` and `text` come from users, so they must be HTML-escaped.
 */
function renderComment({ author, text }) {
  return `<div class="comment"><b>${escapeHtml(author)}</b>: ${escapeHtml(text)}</div>`;
}

module.exports = { renderComment };
```

**Go deeper**

- [OWASP: Cross Site Scripting (XSS)](https://owasp.org/www-community/attacks/xss/)
- [CWE-79: XSS](https://cwe.mitre.org/data/definitions/79.html)

</details>
