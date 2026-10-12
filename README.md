<div align="center">

# Would you merge it? 🧐

### AI wrote it. It looks right. **Would you merge it?**

24 realistic bugs that AI coding assistants write.<br>
Spot them. Fix them. Turn the tests green.

**Zero install to read · fork to play · share your score**

![Katas](https://img.shields.io/badge/katas-24-blue)
![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-3776AB)
![Node 20+](https://img.shields.io/badge/node-20%2B-339933)
![Dependencies](https://img.shields.io/badge/dependencies-none-brightgreen)
![License MIT](https://img.shields.io/badge/license-MIT-lightgrey)

</div>

---

## Try one right now (60 seconds)

> 🤖 **The prompt:** "Write `processAll(ids, fn)` that runs an async function on each id and returns the results in order."

```javascript
async function processAll(ids, fn) {
  const results = [];
  ids.forEach(async (id) => {
    results.push(await fn(id));
  });
  return results;
}
```

It's three lines, it reads naturally, and every keyword is where you'd expect it. **Would you merge it?**

<details>
<summary>🔓 Reveal the bug</summary>

`forEach` ignores the promises returned by an `async` callback, so `processAll` returns the still-empty `results` array **before any work has finished**: every caller gets `[]`, and any error inside the callback is silently lost.

Fix: `return Promise.all(ids.map((id) => fn(id)));`

That was [kata 13](katas/13-foreach-async/). There are 23 more, from one-line gotchas to security bugs that look completely reasonable.

</details>

## Why this exists

AI assistants write code faster than people can read it. They make the same kinds of mistakes humans do, just more often and at larger scale, so the failure modes are **learnable patterns**. Learn them and you review faster, and you stop merging the plausible-looking bug.

- **Security:** Veracode's [2025 GenAI Code Security Report](https://www.veracode.com/blog/genai-code-security-report/) tested 100+ models across Java, Python, C# and JavaScript: **45%** of the generated samples failed security tests and introduced OWASP Top 10 vulnerabilities (Python 38%, JavaScript 43%).
- **More issues per PR:** CodeRabbit's [AI vs Human report](https://www.coderabbit.ai/blog/state-of-ai-vs-human-code-generation-report) analysed 470 open-source PRs and counted **10.83 issues per AI-co-authored PR versus 6.45** for human-only ones. The biggest gaps: logic and correctness (+75%), error handling (~2×), security (up to 2.74×), excessive I/O (~8×) and concurrency (~2×), which are the same families as the katas below. (CodeRabbit sells AI review, and it inferred authorship from signals, so weigh it accordingly.)
- **Invented dependencies:** a [USENIX Security 2025 study](https://www.usenix.org/conference/usenixsecurity25/presentation/spracklen) ([arXiv](https://arxiv.org/abs/2406.10279)) generated 576,000 code samples with 16 models; **19.7%** of the packages they referenced did not exist.

Reading the diff is the new bottleneck. This repo is a gym for it.

## How it works

| | Mode | What you do |
|---|---|---|
| 👀 | **Read** (no setup) | Open a kata on GitHub. The "PR" is in its README. Decide. Open the spoiler. |
| 🔧 | **Fix** (fork & play) | Fork, clone, edit the buggy file until its tests pass. Don't edit the tests. |
| 📣 | **Share** | Your fork grades itself with GitHub Actions and publishes a score badge for your profile. |

## Quick start

```bash
# 1. Click "Fork" (top right), then clone YOUR fork:
git clone https://github.com/YOUR_USERNAME/would-you-merge.git
cd would-you-merge

# 2. See the scoreboard (it starts at 0/24)
python tools/check.py

# 3. Open a kata, find the bug, fix it, re-run
python tools/check.py 01
```

- **Python 3.10+** (standard library only: there is nothing to `pip install`). Use `python3` or `py` if `python` isn't found.
- **Node.js 20+** for the 10 JavaScript katas. Python-only? The JS katas are simply skipped.
- Each kata lives in `katas/NN-name/`: the **buggy file** you edit, its **tests** (don't touch), and a README with a hint and a spoiler.
- `python tools/check.py --reset 07` puts the original file back. `python tools/check.py --list` lists everything.
- Any correct fix is fine: the tests check *behaviour*, not a specific solution. Reference fixes live in `solutions/` (spoilers!).

> ⚠️ The katas contain **intentionally buggy and vulnerable code**. They never touch the network and only write to temp folders, but don't copy them into real projects.

## The katas

<!-- KATAS:START -->
_24 katas · 14 Python · 10 JavaScript_

| # | Kata | Language | Bug class | Level |
|---|------|----------|-----------|-------|
| 01 | [The package that doesn't exist](katas/01-hallucinated-import/) | python | 👻 hallucination | ★☆☆ |
| 02 | [Page one goes missing](katas/02-pagination-off-by-one/) | python | 📏 boundaries | ★☆☆ |
| 03 | [The discount that wouldn't be zero](katas/03-zero-is-falsy/) | python | 🧠 logic | ★☆☆ |
| 04 | [The log that remembers everything](katas/04-mutable-default/) | python | 🧠 logic | ★☆☆ |
| 05 | [Ten is smaller than nine](katas/05-default-sort/) | javascript | 🧠 logic | ★☆☆ |
| 06 | [Zero items, one in the cart](katas/06-parse-int/) | javascript | 🧮 data | ★☆☆ |
| 07 | [The chunk that fell off the end](katas/07-chunk-off-by-one/) | javascript | 📏 boundaries | ★☆☆ |
| 08 | [A cent short](katas/08-float-money/) | python | 🧮 data | ★★☆ |
| 09 | [Every other expired session](katas/09-mutate-while-iterating/) | python | 🧠 logic | ★★☆ |
| 10 | [Everything saved (probably)](katas/10-swallowed-exception/) | python | 🙈 errors | ★★☆ |
| 11 | [Expired in a different timezone](katas/11-naive-datetime/) | python | 🧮 data | ★★☆ |
| 12 | [Tenant A's database host, now with Tenant B](katas/12-shallow-copy/) | python | 🧮 data | ★★☆ |
| 13 | [Done before it started](katas/13-foreach-async/) | javascript | ⏳ async | ★★☆ |
| 14 | [A try/catch that catches nothing](katas/14-missing-await-try/) | javascript | ⏳ async | ★★☆ |
| 15 | [Little Bobby Tables, again](katas/15-sql-injection/) | python | 🔐 security | ★★☆ |
| 16 | [Download anything](katas/16-path-traversal/) | python | 🔐 security | ★★☆ |
| 17 | [An unguessable token (if you can't guess the seed)](katas/17-predictable-token/) | python | 🔐 security | ★★☆ |
| 18 | [The comment that runs code](katas/18-unescaped-html/) | javascript | 🔐 security | ★★☆ |
| 19 | [Debug logging, with credentials](katas/19-secret-in-logs/) | javascript | 🔐 security | ★★☆ |
| 20 | [Fifty-one queries for fifty orders](katas/20-n-plus-one/) | python | 🐌 performance | ★★★ |
| 21 | [The email regex that melts your CPU](katas/21-redos-email/) | python | 🐌 performance | ★★★ |
| 22 | [Two withdrawals walk into a bank](katas/22-check-then-act/) | javascript | ⏳ async | ★★★ |
| 23 | [Merge, and pollute everything](katas/23-prototype-pollution/) | javascript | 🔐 security | ★★★ |
| 24 | [Decode is not verify](katas/24-unverified-token/) | javascript | 🔐 security | ★★★ |
<!-- KATAS:END -->

<!-- FEATURED:START -->
### 🎯 Kata of the week: [21 · The email regex that melts your CPU](katas/21-redos-email/)

`python` · 🐌 `performance` · level ★★★

> 🤖 **The prompt:** "Write a regex to validate email addresses on the signup form."

**Would you merge it?** [Open the kata →](katas/21-redos-email/)
<!-- FEATURED:END -->

## Share your score

1. In **your fork**, open the **Actions** tab and click *"I understand my workflows, go ahead and enable them"*.
2. Push to `main`. The **Grade my fork** workflow runs your katas, prints a scoreboard in the run summary, and publishes `badge.json` to a `badges` branch of your fork.
3. Put your badge in your profile README (replace `YOUR_USERNAME`):

```md
[![bugs caught](https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2FYOUR_USERNAME%2Fwould-you-merge%2Fbadges%2Fbadge.json)](https://github.com/YOUR_USERNAME/would-you-merge)
```

4. Caught all of them? Add yourself to the [🏆 Hall of Fame](HALL_OF_FAME.md).

It's an honour-system game: you can edit your own fork's grader, but then you've only fooled yourself.

## Bonus: does *your* AI reviewer catch them?

Paste a kata's buggy code into your favourite assistant with "review this pull request" and see whether it finds the planted bug, and how many false alarms it adds. There's a tiny protocol in [docs/BENCH.md](docs/BENCH.md). (Katas may be in some models' training data by now, so treat results as a fun signal, not a benchmark.)

## Add a kata (5 minutes)

Seen an AI write a bug that deserves a spot? The scaffolder creates every file for you:

```bash
python tools/new_kata.py --slug sort-stability --title "The sort that reordered my users" \
  --lang python --module ranking --level 2 --category logic \
  --prompt "Sort the leaderboard by score, then by name."
```

Fill in the `TODO(kata)` markers, run `python tools/verify_katas.py <id>`, open a PR. Rules, checklist and 40+ ready-to-claim ideas are in [CONTRIBUTING.md](CONTRIBUTING.md) and [docs/KATA-IDEAS.md](docs/KATA-IDEAS.md).

## FAQ

**Isn't this just LeetCode?** No. You are not inventing an algorithm; you are reviewing code that *looks right*, which is the skill AI-assisted development demands.

**Are these bugs specific to AI?** No, people write them too (CodeRabbit found humans and AI make the same kinds of mistakes, with AI making more of them). These are the patterns that slip through when code arrives fast, looks tidy and gets a light review.

**Can I use AI to solve them?** Sure. The interesting question is whether you'd have caught the bug *before* the tests told you. Try reading first.

**Why only Python and JavaScript?** They're where most AI-written code lives, and both run with nothing to install. More languages are welcome as PRs.

**Will it break on Windows/macOS?** The tools are plain Python and Node. If something misbehaves, open an issue with your OS and versions.

## If it helped

If this made you look twice at an AI diff, a ⭐ helps other developers find it, and a PR with a new kata helps even more.

## License

[MIT](LICENSE). Contributions are licensed the same way.
