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
