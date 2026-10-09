'use strict';

/**
 * Return the three highest scores, in ascending order.
 * Must not modify the array that was passed in.
 */
function topThree(scores) {
  return [...scores].sort((a, b) => a - b).slice(-3);
}

module.exports = { topThree };
