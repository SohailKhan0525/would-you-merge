# Kata ideas (claim one!)

Every idea here is a bug AI assistants (and tired humans) really write, and each can be tested **offline and deterministically**. Pick one, comment on its issue (or open one) so we don't duplicate, then follow [CONTRIBUTING.md](../CONTRIBUTING.md).

Levels: 1 = one concept · 2 = real-world pattern · 3 = subtle.

## Python

| Idea (slug) | Level | Class | The bug in one line |
|-------------|:----:|-------|---------------------|
| `no-timeout` | 1 | errors | `urllib.request.urlopen(url)` with no `timeout`: one slow server hangs the worker forever (test with a mock and assert the `timeout` argument). |
| `dict-get-append` | 1 | logic | `groups.get(key, []).append(x)` appends to a throwaway list; nothing is ever stored. |
| `float-equality` | 1 | data | `if total == 0.3` after adding `0.1 + 0.2`; use `math.isclose` or decimals. |
| `bare-except` | 2 | errors | `except:` also swallows `KeyboardInterrupt` and `SystemExit`; the worker can't be stopped. |
| `assert-validation` | 2 | security | Input validation written as `assert`, which vanishes under `python -O` (run the test in a `-O` subprocess). |
| `isdigit-unicode` | 2 | data | `"²".isdigit()` is `True`, but `int("²")` raises: validation passes, conversion crashes. |
| `regex-dollar-newline` | 2 | security | `re.match(r"^\w+$", "admin\n")` matches because `$` accepts a trailing newline; use `fullmatch`. |
| `fallback-secret` | 2 | security | `os.environ.get("JWT_SECRET", "dev-secret")` silently runs production with a known key. |
| `open-redirect` | 2 | security | `redirect(next)` accepts `//evil.com`, `https://evil.com` and `/\evil.com`. |
| `csv-injection` | 2 | security | Exported cells starting with `=`, `+`, `-` or `@` become spreadsheet formulas. |
| `log-injection` | 2 | security | User input with `\n` forges extra log lines. |
| `mass-assignment` | 2 | security | `User(**payload)` lets a request set `is_admin=True`. |
| `idor` | 2 | security | `get_invoice(user, invoice_id)` never checks the invoice belongs to `user`. |
| `password-hash` | 2 | security | `sha256(password)` with no salt/work factor; expect two hashes of one password to differ and verify to work (`hashlib.scrypt` is in the standard library). |
| `timing-compare` | 2 | security | `token == expected` for secrets; test that `hmac.compare_digest` is used. |
| `banker-rounding` | 2 | data | `round(2.5) == 2`; tax must round half-up (`decimal.ROUND_HALF_UP`). |
| `json-nan` | 2 | data | `json.dumps(float("nan"))` emits `NaN`, which is not valid JSON (`allow_nan=False`). |
| `sqlite-no-commit` | 2 | errors | Writes never committed; a second connection to the same temp file sees nothing. |
| `ssrf-private-ip` | 3 | security | A URL fetcher that allows `127.0.0.1`, `169.254.169.254` and `10.x` targets (check with `ipaddress`, no network needed). |
| `lru-cache-method` | 3 | performance | `@lru_cache` on a method keeps every instance alive forever (test with `weakref` + `gc`). |
| `toctou-file` | 3 | async | `if not os.path.exists(p): open(p, "w")` races; open with mode `"x"`. |

## JavaScript

| Idea (slug) | Level | Class | The bug in one line |
|-------------|:----:|-------|---------------------|
| `loose-equality` | 1 | logic | `if (id == 0)` is also true for `''` and `'0'`. |
| `for-in-array` | 1 | logic | `for (const i in arr)` yields string keys (and inherited properties). |
| `replace-first-only` | 1 | logic | `str.replace('a', 'b')` replaces only the first match. |
| `json-parse-no-try` | 1 | errors | `JSON.parse(userInput)` throws on bad input and crashes the handler. |
| `array-includes-nan` | 1 | logic | `indexOf(NaN)` is `-1` while `includes(NaN)` is `true`. |
| `object-spread-shallow` | 2 | logic | `{...defaults, ...overrides}` replaces a whole nested object instead of merging it. |
| `promise-all-vs-settled` | 2 | async | One failed request rejects the whole `Promise.all` and loses the other results. |
| `regex-g-flag-test` | 2 | logic | A shared `/x/g` regex keeps `lastIndex`, so `re.test(s)` alternates true/false. |
| `sort-comparator-boolean` | 2 | logic | `sort((a, b) => a > b)` returns booleans, so the order is wrong. |
| `bigint-ids` | 2 | data | JSON ids above 2^53 lose precision when parsed as numbers. |
| `date-zero-month` | 2 | data | `new Date(2026, 1, 1)` is **February**; date-only strings parse as UTC but format as local. |
| `math-random-token` | 2 | security | Tokens from `Math.random()` (test: stub it to a constant and expect different tokens anyway). |
| `path-join-traversal` | 2 | security | `path.join(base, name)` lets `../../etc/passwd` escape; use `path.resolve` plus a prefix check with `path.sep`. |
| `cors-reflect-origin` | 2 | security | Reflecting any `Origin` together with `Access-Control-Allow-Credentials: true`. |
| `await-in-loop` | 2 | performance | Independent requests awaited one by one (assert the maximum concurrency). |
| `interval-leak` | 3 | performance | `setInterval` never cleared; the process never exits (use fake timers). |
| `cache-stampede` | 3 | async | Ten concurrent callers all miss the cache and run the expensive call ten times (expect once). |
| `retry-double-charge` | 3 | async | Retrying a non-idempotent POST after a timeout charges the customer twice. |
| `timer-unhandled-error` | 3 | async | An `async` function inside `setTimeout` throws and nobody can catch it. |

## Other languages (a runner has to be added first; see CONTRIBUTING)

Go: goroutine captures the loop variable · `defer` inside a loop · nil-map write.
Java: `==` on strings · `equals` without `hashCode` · `SimpleDateFormat` shared across threads.
Rust: `unwrap()` on user input · integer overflow in release builds.
SQL: `NOT IN` with a NULL · `LIMIT` without `ORDER BY`.
