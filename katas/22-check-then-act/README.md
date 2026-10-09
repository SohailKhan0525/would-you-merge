# 22 · Two withdrawals walk into a bank

`javascript` · ⏳ `async` · level ★★★

> 🤖 **The prompt:** "Write withdraw(account, amount) for our ledger. Don't let the balance go negative."

The balance check is right there on line one. What could possibly go wrong *after* it?

```javascript
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
```

**Would you approve this PR?** Take a minute. Then try to break it.

## Your turn

Fix [`bank.js`](./bank.js) so the tests pass. **Don't edit the tests.**

```bash
python tools/check.py 22
```

Want a clean slate? `python tools/check.py --reset 22` restores the original file.

<details>
<summary>💡 Hint</summary>

Two requests arrive 1 ms apart. Trace both through `withdraw` line by line, remembering that every `await` lets *somebody else* run.

</details>

<details>
<summary>🔓 Spoiler: the bug, and why AI writes it</summary>

A classic **check-then-act race**: both calls pass the balance check *before* either has deducted anything, because `await` yields control in between. JavaScript is single-threaded, but it is **not atomic across awaits**.

Reserve the funds synchronously (check *and* deduct before the first `await`, refund on failure), or serialise per-account work with a queue/mutex. In a real system, use a database transaction or a conditional update (`UPDATE ... WHERE balance >= ?`).

**A fix** (also in [`solutions/22-check-then-act/`](../../solutions/22-check-then-act/))

```javascript
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
```

**Go deeper**

- [CWE-367: Time-of-check time-of-use race condition](https://cwe.mitre.org/data/definitions/367.html)

</details>
