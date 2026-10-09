'use strict';

const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

/**
 * Withdraw `amount` from `account` ({ balance }).
 * Resolves true on success, false if the funds aren't there.
 * The balance must never go negative, even when requests arrive concurrently.
 */
async function withdraw(account, amount) {
  if (account.balance < amount) return false;
  account.balance -= amount; // reserve the funds *before* the first await
  try {
    await sleep(5); // pretend we call the payment provider here
    return true;
  } catch (err) {
    account.balance += amount; // give the money back if the provider failed
    throw err;
  }
}

module.exports = { withdraw };
