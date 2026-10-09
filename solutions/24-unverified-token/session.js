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
