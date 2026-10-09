# 24 · Decode is not verify

`javascript` · 🔐 `security` · level ★★★

> 🤖 **The prompt:** "Verify the signed session token from the cookie."

It parses, it checks expiry, it returns the user. There's a `secret` parameter, too. Look at it go.

```javascript
'use strict';
const crypto = require('node:crypto');

/**
 * Tokens look like  base64url(payloadJSON) + '.' + base64url(HMAC-SHA256(payloadPart, secret)).
 */
function sign(payload, secret) {
  const body = Buffer.from(JSON.stringify(payload)).toString('base64url');
  const signature = crypto.createHmac('sha256', secret).update(body).digest('base64url');
  return `${body}.${signature}`;
}

/**
 * Return the payload if the token is authentic and not expired
 * (`payload.exp` is in unix seconds), otherwise null.
 */
function verify(token, secret, nowSeconds = Math.floor(Date.now() / 1000)) {
  const [body] = String(token).split('.');
  let payload;
  try {
    payload = JSON.parse(Buffer.from(body, 'base64url').toString('utf8'));
  } catch (err) {
    return null;
  }
  if (typeof payload.exp === 'number' && payload.exp < nowSeconds) return null;
  return payload;
}

module.exports = { sign, verify };
```

**Would you approve this PR?** Take a minute. Then try to break it.

## Your turn

Fix [`session.js`](./session.js) so the tests pass. **Don't edit the tests.**

```bash
python tools/check.py 24
```

Want a clean slate? `python tools/check.py --reset 24` restores the original file.

<details>
<summary>💡 Hint</summary>

Where does `verify` ever *use* `secret`? Change one character in the payload part of a valid token and see what happens.

</details>

<details>
<summary>🔓 Spoiler: the bug, and why AI writes it</summary>

The function **decodes** the token but never **verifies** it: the signature is ignored, so anyone can mint a token for any user (here, `admin`). "Decode" and "verify" look nearly identical in library APIs (`jwt.decode` vs `jwt.verify`), and AI assistants mix them up.

Always recompute the signature over the exact signed bytes, compare in constant time (`timingSafeEqual`), and only *then* trust the payload.

**A fix** (also in [`solutions/24-unverified-token/`](../../solutions/24-unverified-token/))

```javascript
'use strict';
const crypto = require('node:crypto');

/**
 * Tokens look like  base64url(payloadJSON) + '.' + base64url(HMAC-SHA256(payloadPart, secret)).
 */
function sign(payload, secret) {
  const body = Buffer.from(JSON.stringify(payload)).toString('base64url');
  const signature = crypto.createHmac('sha256', secret).update(body).digest('base64url');
  return `${body}.${signature}`;
}

/**
 * Return the payload if the token is authentic and not expired
 * (`payload.exp` is in unix seconds), otherwise null.
 */
function verify(token, secret, nowSeconds = Math.floor(Date.now() / 1000)) {
  const parts = String(token).split('.');
  if (parts.length !== 2) return null;
  const [body, signature] = parts;

  const expected = crypto.createHmac('sha256', secret).update(body).digest();
  const given = Buffer.from(signature, 'base64url');
  if (given.length !== expected.length || !crypto.timingSafeEqual(given, expected)) return null;

  let payload;
  try {
    payload = JSON.parse(Buffer.from(body, 'base64url').toString('utf8'));
  } catch (err) {
    return null;
  }
  if (typeof payload.exp === 'number' && payload.exp < nowSeconds) return null;
  return payload;
}

module.exports = { sign, verify };
```

**Go deeper**

- [CWE-347: Improper verification of a cryptographic signature](https://cwe.mitre.org/data/definitions/347.html)

</details>
