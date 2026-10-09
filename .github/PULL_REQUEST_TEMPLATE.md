<!-- Thanks for contributing! Branch from upstream main; don't include solved katas. -->

## What's this PR?

- [ ] A new kata
- [ ] A fix to an existing kata
- [ ] Hall of Fame entry
- [ ] Tooling / docs

## Checklist for a new or changed kata

- [ ] `python tools/verify_katas.py <id> --strict` passes (fails on the original, passes with the solution)
- [ ] `python tools/build_index.py` was run and the README table is updated
- [ ] I tried at least one *different* correct fix and the tests accepted it
- [ ] No `TODO(kata)` markers left, no network, no third-party packages
- [ ] If an AI helped, I say so here and I have verified the bug and the explanation myself

**The bug in one sentence:**
