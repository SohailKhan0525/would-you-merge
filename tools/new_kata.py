#!/usr/bin/env python3
"""Scaffold a new kata. You fill in the TODO(kata) markers, then verify.

    python tools/new_kata.py --slug sort-stability --title "The sort that reordered my users" \\
        --lang python --module ranking --level 2 --category logic \\
        --prompt "Sort the leaderboard by score, then by name."

Then:  edit the files  ->  python tools/verify_katas.py <id>  ->  python tools/build_index.py
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import kata_lib as lib

PY_MODULE = '''"""TODO(kata): {module}.py: one line about what this module does."""


def todo_function():
    """TODO(kata): replace this with the AI-written code that hides ONE bug.

    Put the contract in the docstring so the tests are fair.
    """
    raise NotImplementedError
'''

PY_TEST = '''import unittest

# TODO(kata): import the code under test, e.g.  from {module} import something


class TestKata(unittest.TestCase):
    def test_todo(self):
        # TODO(kata): write tests that FAIL on the buggy code and PASS on a correct fix.
        self.fail("write the tests")


if __name__ == "__main__":
    unittest.main()
'''

JS_MODULE = """'use strict';

// TODO(kata): replace this with the AI-written code that hides ONE bug.
// Put the contract in a doc comment so the tests are fair.
function todoFunction() {
  throw new Error('not implemented');
}

module.exports = { todoFunction };
"""

JS_TEST = """'use strict';
const test = require('node:test');
const assert = require('node:assert/strict');
// TODO(kata): require the code under test, e.g.  const { something } = require('./{module}');

test('todo', () => {
  // TODO(kata): write tests that FAIL on the buggy code and PASS on a correct fix.
  assert.fail('write the tests');
});
"""

README = """# {id} · {title}

`{lang}` · {emoji} `{category}` · level {stars}

> 🤖 **The prompt:** "{prompt}"

TODO(kata): one or two sentences of setup. Keep it light.

```{lang}
TODO(kata): paste the buggy code here (same as {module}{ext})
```

**Would you approve this PR?** Take a minute. Then try to break it.

## Your turn

Fix [`{module}{ext}`](./{module}{ext}) so the tests pass. **Don't edit the tests.**

```bash
python tools/check.py {id}
```

Want a clean slate? `python tools/check.py --reset {id}` restores the original file.

<details>
<summary>💡 Hint</summary>

TODO(kata): nudge, don't give it away.

</details>

<details>
<summary>🔓 Spoiler: the bug, and why AI writes it</summary>

TODO(kata): what is wrong, why is it easy to miss, why do LLMs write it, how do you spot it in review.

**A fix** (also in [`solutions/{folder}/`](../../solutions/{folder}/))

```{lang}
TODO(kata): paste the fixed code here
```

**Go deeper**

- TODO(kata): a link to a primary source (docs, CWE, paper). Delete this section if there isn't one.

</details>
"""


def main(argv=None) -> int:
    lib.setup_stdout()
    parser = argparse.ArgumentParser(description="Scaffold a new kata.")
    parser.add_argument("--slug", required=True, help="kebab-case, e.g. sort-stability")
    parser.add_argument("--title", required=True)
    parser.add_argument("--lang", required=True, choices=sorted(lib.EXT))
    parser.add_argument("--module", required=True, help="file name without extension, e.g. ranking")
    parser.add_argument("--level", required=True, type=int, choices=[1, 2, 3])
    parser.add_argument("--category", required=True, choices=sorted(lib.CATEGORY_EMOJI))
    parser.add_argument("--prompt", required=True, help="what the user asked the AI")
    args = parser.parse_args(argv)

    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", args.slug):
        print("--slug must be kebab-case (lowercase letters, digits, hyphens)")
        return 2
    if not re.fullmatch(r"[a-z][a-z0-9_]*", args.module):
        print("--module must be a simple lowercase name like 'ranking' or 'bulk_save'")
        return 2

    existing = lib.load_katas()
    if any(k.slug == args.slug for k in existing):
        print(f"A kata with slug {args.slug!r} already exists.")
        return 2
    next_id = max((int(k.id) for k in existing), default=0) + 1
    if next_id > 99:
        print("The folder scheme supports at most 99 katas.")
        return 2
    kid = f"{next_id:02d}"
    folder = f"{kid}-{args.slug}"
    ext = lib.EXT[args.lang]

    kata_dir = lib.KATAS_DIR / folder
    solution_dir = lib.SOLUTIONS_DIR / folder
    module_text = PY_MODULE.format(module=args.module) if args.lang == "python" else JS_MODULE
    test_text = PY_TEST.format(module=args.module) if args.lang == "python" else JS_TEST.replace("{module}", args.module)
    test_name = f"test_{args.module}.py" if args.lang == "python" else f"{args.module}.test.js"

    files = {
        kata_dir / "kata.json": json.dumps(
            {
                "id": kid,
                "slug": args.slug,
                "title": args.title,
                "lang": args.lang,
                "module": args.module,
                "level": args.level,
                "category": args.category,
                "prompt": args.prompt,
            },
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        kata_dir / f"{args.module}{ext}": module_text,
        kata_dir / ".original" / f"{args.module}{ext}": module_text,
        kata_dir / test_name: test_text,
        kata_dir / "README.md": README.format(
            id=kid,
            title=args.title,
            lang=args.lang,
            emoji=lib.CATEGORY_EMOJI[args.category],
            category=args.category,
            stars=lib.LEVEL_STARS[args.level],
            prompt=args.prompt,
            module=args.module,
            ext=ext,
            folder=folder,
        ),
        solution_dir / f"{args.module}{ext}": module_text,
    }
    for path, text in files.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8", newline="\n")

    print(f"Created katas/{folder}/ and solutions/{folder}/")
    print()
    print("Next steps:")
    print(f"  1. Write the buggy code in katas/{folder}/{args.module}{ext} and copy it to katas/{folder}/.original/")
    print(f"  2. Write the tests in katas/{folder}/{test_name} (they must FAIL on the buggy code)")
    print(f"  3. Write the fix in solutions/{folder}/{args.module}{ext} (the tests must PASS)")
    print("  4. Fill in the README (replace every TODO(kata))")
    print(f"  5. python tools/verify_katas.py {kid} --strict && python tools/build_index.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
