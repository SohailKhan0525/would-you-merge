#!/usr/bin/env python3
"""Run kata tests, see your scoreboard, or reset a kata.

    python tools/check.py              scoreboard for every kata
    python tools/check.py 07           run kata 07 and show what failed
    python tools/check.py 7 12 chunk   run several (by number or part of the name)
    python tools/check.py --reset 07   put the original buggy file back
    python tools/check.py --list       list the katas without running them

Needs Python 3.10+. JavaScript katas also need Node.js 20+.
"""
from __future__ import annotations

import argparse
import shutil
import sys

import kata_lib as lib


def label(kata: lib.Kata) -> str:
    emoji = lib.CATEGORY_EMOJI.get(kata.category, "")
    return f"{kata.id}  {kata.slug:<26} {kata.lang:<11} {emoji} {kata.category:<13} {lib.LEVEL_STARS[kata.level]}"


def main(argv=None) -> int:
    lib.setup_stdout()
    parser = argparse.ArgumentParser(description="Check your would-you-merge katas.")
    parser.add_argument("katas", nargs="*", help="kata number or part of its name (default: all)")
    parser.add_argument("--list", action="store_true", help="list katas and exit")
    parser.add_argument("--reset", action="store_true", help="restore the original file of the given kata(s)")
    args = parser.parse_args(argv)

    katas = lib.load_katas()
    if not katas:
        print("No katas found. Run this from the repository root.")
        return 2

    if args.list:
        for kata in katas:
            print(label(kata))
        return 0

    if args.reset:
        if not args.katas:
            print("Name the kata(s) to reset, e.g.  python tools/check.py --reset 07")
            return 2
        for kata in lib.select(katas, args.katas):
            shutil.copyfile(kata.original_file, kata.dir / kata.module_file)
            print(f"restored katas/{kata.folder}/{kata.module_file}")
        return 0

    chosen = lib.select(katas, args.katas) if args.katas else katas
    detailed = bool(args.katas)
    solved = failed = skipped = 0
    for kata in chosen:
        result = lib.run_tests(kata.dir, kata)
        if result.status == "pass":
            solved += 1
            print(f"✅ {label(kata)}")
        elif result.status == "skip":
            skipped += 1
            print(f"⏭️  {label(kata)}   ({result.detail})")
        else:
            failed += 1
            print(f"❌ {label(kata)}")
            if detailed:
                body = result.output or result.detail
                print()
                print(lib.tail(lib.friendly(body), 40))
                print()
                print(f"   edit: katas/{kata.folder}/{kata.module_file}   (don't touch the test)")
                print(f"   read: katas/{kata.folder}/README.md")
                print()

    total = len(chosen)
    print()
    suffix = f", {skipped} skipped" if skipped else ""
    print(f"Fixed {solved}/{total}{suffix}.")
    if solved == total and total == len(katas):
        print("🎉 Every bug caught. Share your score: see 'Share your score' in the README.")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
