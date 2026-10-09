# Contributing

Thanks for helping people review AI-written code better. The most valuable contribution is **a new kata**. Fixing a typo or a flaky test is a close second.

## 1. Pick a bug worth teaching

A good kata is:

- **Realistic.** An AI assistant (or a tired human) would plausibly write it, and it *looks right* at a glance.
- **One bug.** Not three. The tests should fail for one reason.
- **Fair.** The contract (what the code must do) is written in the docstring/doc comment, so a correct fix that differs from yours still passes.
- **Deterministic, offline and fast.** No network, no sleeping for seconds, no random failures, under ~3 seconds.
- **Teaching a pattern**, not trivia. The spoiler should explain *why* the bug is easy to miss and *why* AI tends to write it.

Please don't submit: bugs that need third-party packages, databases or API keys; anything that touches the network; real exploit payloads aimed at real systems; code copied from sources you don't have the right to reuse.

Need inspiration? [docs/KATA-IDEAS.md](docs/KATA-IDEAS.md) has 40+ ideas. Comment on the matching issue (or open one) so two people don't build the same kata.

## 2. Scaffold it

```bash
python tools/new_kata.py --slug sort-stability --title "The sort that reordered my users" \
  --lang python --module ranking --level 2 --category logic \
  --prompt "Sort the leaderboard by score, then by name."
```

This creates every file with `TODO(kata)` markers. CI refuses a kata that still contains one.

| File | What it is |
|------|-----------|
| `katas/NN-slug/kata.json` | metadata (id, slug, title, lang, module, level, category, prompt) |
| `katas/NN-slug/<module>.py` or `.js` | the **buggy** file learners edit |
| `katas/NN-slug/.original/<module>` | pristine copy of the buggy file (powers `--reset`; must be identical) |
| `katas/NN-slug/test_<module>.py` or `<module>.test.js` | tests: must **fail** on the buggy file and **pass** on a correct fix |
| `katas/NN-slug/README.md` | the "PR": the prompt, the code, a hint, and a spoiler |
| `solutions/NN-slug/<module>` | your reference fix |

**Level:** 1 = one concept · 2 = a real-world pattern · 3 = subtle (concurrency, security, performance).
**Category:** `hallucination`, `boundaries`, `security`, `async`, `data`, `errors`, `logic`, `performance`.

## 3. Verify it

```bash
python tools/verify_katas.py NN --strict      # fails on the original, passes with the solution
python tools/build_index.py                   # refresh the table in README.md
```

Then try 1-2 *different* correct fixes of your own. If the tests reject a valid fix, the tests are too strict: test behaviour, not implementation.

## 4. Open a pull request

- Branch from the **upstream** `main`. **Never commit a solved kata** (CI runs `--strict` and will tell you).
- One kata per PR keeps review quick.

## Style

- Python: standard library only, `unittest`, works on Python 3.10+. JavaScript: CommonJS, `node:test` + `node:assert/strict`, works on Node 20+.
- No dependencies, no build step, no network.
- Tests may use the temp folder; they must clean up after themselves.

## AI-assisted contributions

Welcome, with one rule: **you** are responsible for the kata. Run it, break it, make sure the bug is real and the explanation is true. Say in the PR if an AI helped. (A repo about catching AI mistakes should hold itself to the same standard.)

## Other ways to help

- Report a kata whose test is too strict, too loose, or flaky (use the "Problem with a kata" issue form).
- Try a kata on a different OS or Python/Node version and tell us what broke.
- Add a new language runner: open an issue first. It means touching `tools/kata_lib.py` (`EXT`, `run_tests`) and the CI matrix.
