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
