#!/usr/bin/env python3
"""Rotate the "Kata of the week" block in README.md.

    python tools/featured.py                 pick this week's kata and update README.md
    python tools/featured.py --date 2026-10-12   pretend today is that date (for testing)
    python tools/featured.py --dry-run       print the block without writing

The pick is deterministic (ISO year + week number), so re-running it in the same week is a no-op.
"""
from __future__ import annotations

import argparse
import datetime
import sys

import kata_lib as lib

START = "<!-- FEATURED:START -->"
END = "<!-- FEATURED:END -->"


def pick(katas, day: datetime.date):
    iso = day.isocalendar()
    return katas[(iso[0] * 53 + iso[1]) % len(katas)]


def render(kata: lib.Kata) -> str:
    emoji = lib.CATEGORY_EMOJI.get(kata.category, "")
    return "\n".join(
        [
            f"### 🎯 Kata of the week: [{kata.id} · {kata.title}](katas/{kata.folder}/)",
            "",
            f"`{kata.lang}` · {emoji} `{kata.category}` · level {lib.LEVEL_STARS[kata.level]}",
            "",
            f'> 🤖 **The prompt:** "{kata.prompt}"',
            "",
            f"**Would you merge it?** [Open the kata →](katas/{kata.folder}/)",
        ]
    )


def main(argv=None) -> int:
    lib.setup_stdout()
    parser = argparse.ArgumentParser(description="Update the featured kata in README.md.")
    parser.add_argument("--date", help="YYYY-MM-DD (default: today, UTC)")
    parser.add_argument("--dry-run", action="store_true", help="print the block, don't write")
    args = parser.parse_args(argv)

    katas = lib.load_katas()
    if not katas:
        print("No katas found.")
        return 1
    if args.date:
        day = datetime.date.fromisoformat(args.date)
    else:
        day = datetime.datetime.now(datetime.timezone.utc).date()

    block = render(pick(katas, day))
    if args.dry_run:
        print(block)
        return 0

    readme = lib.ROOT / "README.md"
    text = readme.read_text(encoding="utf-8")
    start = text.find(START)
    end = text.find(END)
    if start == -1 or end == -1 or end < start:
        print(f"README.md must contain {START} ... {END}")
        return 1
    updated = text[: start + len(START)] + "\n" + block + "\n" + text[end:]
    if updated == text:
        print("Featured kata unchanged.")
        return 0
    readme.write_text(updated, encoding="utf-8", newline="\n")
    print(f"Featured kata is now {pick(katas, day).folder}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
