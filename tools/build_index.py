#!/usr/bin/env python3
"""Regenerate the kata table in README.md (the block between the KATAS markers).

    python tools/build_index.py            rewrite README.md if the table is out of date
    python tools/build_index.py --check    exit 1 if README.md is out of date (used by CI)
"""
from __future__ import annotations

import argparse
import sys

import kata_lib as lib

START = "<!-- KATAS:START -->"
END = "<!-- KATAS:END -->"


def render(katas) -> str:
    python = sum(1 for k in katas if k.lang == "python")
    javascript = sum(1 for k in katas if k.lang == "javascript")
    lines = [
        f"_{len(katas)} katas · {python} Python · {javascript} JavaScript_",
        "",
        "| # | Kata | Language | Bug class | Level |",
        "|---|------|----------|-----------|-------|",
    ]
    for k in katas:
        title = k.title.replace("|", "\\|")
        emoji = lib.CATEGORY_EMOJI.get(k.category, "")
        lines.append(
            f"| {k.id} | [{title}](katas/{k.folder}/) | {k.lang} | {emoji} {k.category} | {lib.LEVEL_STARS[k.level]} |"
        )
    return "\n".join(lines)


def replace_block(text: str, body: str) -> str:
    start = text.find(START)
    end = text.find(END)
    if start == -1 or end == -1 or end < start:
        raise SystemExit(f"README.md must contain {START} ... {END}")
    return text[: start + len(START)] + "\n" + body + "\n" + text[end:]


def main(argv=None) -> int:
    lib.setup_stdout()
    parser = argparse.ArgumentParser(description="Rebuild the README kata table.")
    parser.add_argument("--check", action="store_true", help="fail if README.md is out of date")
    args = parser.parse_args(argv)

    readme = lib.ROOT / "README.md"
    current = readme.read_text(encoding="utf-8")
    updated = replace_block(current, render(lib.load_katas()))
    if updated == current:
        print("README.md kata table is up to date.")
        return 0
    if args.check:
        print("README.md kata table is out of date. Run: python tools/build_index.py")
        return 1
    readme.write_text(updated, encoding="utf-8", newline="\n")
    print("README.md kata table updated.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
