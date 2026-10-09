'use strict';

const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

/**
 * Withdraw `amount` from `account` ({ balance }).
 * Resolves true on success, false if the funds aren't there.
 * The balance must never go negative, even when requests arrive concurrently.
 */
async function withdraw(account, amount) {
  if (account.balance < amount) return false;
  await sleep(5); // pretend we call the payment provider here
  account.balance -= amount;
  return true;
}

module.exports = { withdraw };
