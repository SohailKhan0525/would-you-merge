# 19 · Debug logging, with credentials

`javascript` · 🔐 `security` · level ★★☆

> 🤖 **The prompt:** "Log every outgoing API request so we can debug."

One line, great for debugging. Your log vendor will also enjoy it.

```javascript
'use strict';

/**
 * Log an outgoing request: method, url and headers.
 *
 * Credentials must never reach the logs: the values of the Authorization,
 * Proxy-Authorization, Cookie and Set-Cookie headers (any letter case) must be
 * logged as "[REDACTED]". Do not modify the request object itself.
 */
function logRequest(req) {
  console.log('outgoing request', JSON.stringify(req));
}

module.exports = { logRequest };
```

**Would you approve this PR?** Take a minute. Then try to break it.

## Your turn

Fix [`requestlog.js`](./requestlog.js) so the tests pass. **Don't edit the tests.**

```bash
python tools/check.py 19
```

Want a clean slate? `python tools/check.py --reset 19` restores the original file.

<details>
<summary>💡 Hint</summary>

Run the function and read exactly what ends up in the console. Who else can read your logs, and for how long are they kept?

</details>

<details>
<summary>🔓 Spoiler: the bug, and why AI writes it</summary>

Dumping the whole request object logs credentials in plain text: `Authorization` headers, cookies, API keys. Logs live far longer, and are readable by far more people (and vendors), than secrets should be.

Log an **allow-list** of fields or redact the sensitive ones, and redact in a *copy*, never the live object. Assistants love `console.log(JSON.stringify(obj))` because it's the fastest way to make a bug visible.

**A fix** (also in [`solutions/19-secret-in-logs/`](../../solutions/19-secret-in-logs/))

```javascript
'use strict';

const SENSITIVE = new Set(['authorization', 'proxy-authorization', 'cookie', 'set-cookie']);

/**
 * Log an outgoing request: method, url and headers.
 *
 * Credentials must never reach the logs: the values of the Authorization,
 * Proxy-Authorization, Cookie and Set-Cookie headers (any letter case) must be
 * logged as "[REDACTED]". Do not modify the request object itself.
 */
function logRequest(req) {
  const headers = {};
  for (const [name, value] of Object.entries(req.headers || {})) {
    headers[name] = SENSITIVE.has(name.toLowerCase()) ? '[REDACTED]' : value;
  }
  console.log('outgoing request', JSON.stringify({ method: req.method, url: req.url, headers }));
}

module.exports = { logRequest };
```

**Go deeper**

- [CWE-532: Sensitive information in log files](https://cwe.mitre.org/data/definitions/532.html)

</details>
