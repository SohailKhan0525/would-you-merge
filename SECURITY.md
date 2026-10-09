# Security policy

The katas in this repository contain **intentionally vulnerable code**. That is the point. Those
are not security issues, please don't report them.

Do report real problems in the project itself:

- the tooling in `tools/`
- the GitHub Actions workflows in `.github/workflows/`
- a kata whose tests execute something unsafe on a learner's machine (network access, writes
  outside a temp folder, long-running processes)

Please use GitHub's **private vulnerability reporting** (the *Security* tab, then *Report a
vulnerability*) instead of a public issue.
