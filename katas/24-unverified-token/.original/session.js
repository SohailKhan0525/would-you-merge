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
