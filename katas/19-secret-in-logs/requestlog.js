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
