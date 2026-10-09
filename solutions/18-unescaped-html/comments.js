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
