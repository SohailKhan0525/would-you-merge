'use strict';

/**
 * Return the three highest scores, in ascending order.
 * Must not modify the array that was passed in.
 */
function topThree(scores) {
  return scores.sort().slice(-3);
}

module.exports = { topThree };
