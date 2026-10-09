#!/usr/bin/env python3
"""Maintainer check: every kata must FAIL on its original code and PASS with its reference solution.

    python tools/verify_katas.py                 verify every kata
    python tools/verify_katas.py 07 chunk        verify specific katas
    python tools/verify_katas.py --strict        also require katas/*/<module> == .original/<module>
    python tools/verify_katas.py --require-all   treat a missing runtime (e.g. no Node) as an error

CI runs this with --strict --require-all on the upstream repo.
"""
from __future__ import annotations

import argparse
import shutil
import sys
import tempfile
from pathlib import Path
from typing import List

import kata_lib as lib

TODO_MARK = "TODO(kata)"


def run_with(kata: lib.Kata, overlay: Path) -> lib.Result:
    """Run the kata's tests in a throw-away copy with `overlay` as the module under test."""
    with tempfile.TemporaryDirectory() as tmp:
        work = Path(tmp) / "kata"
        shutil.copytree(kata.dir, work, ignore=shutil.ignore_patterns(".original", "__pycache__", "node_modules"))
        shutil.copyfile(overlay, work / kata.module_file)
        return lib.run_tests(work, kata)


def check_kata(kata: lib.Kata, strict: bool, require_all: bool, warnings: List[str]) -> List[str]:
    errors: List[str] = []

    match = lib.FOLDER_RE.match(kata.dir.name)
    if not match:
        errors.append("folder name must look like '07-some-slug'")
    elif match.group(1) != kata.id or match.group(2) != kata.slug:
        errors.append("folder name must be '<id>-<slug>' exactly as written in kata.json")
    if kata.lang not in lib.EXT:
        errors.append(f"lang must be one of {sorted(lib.EXT)}")
        return errors
    if kata.level not in lib.LEVEL_STARS:
        errors.append("level must be 1, 2 or 3")
    if kata.category not in lib.CATEGORY_EMOJI:
        errors.append(f"category must be one of {sorted(lib.CATEGORY_EMOJI)}")
    if not kata.prompt.strip() or not kata.title.strip():
        errors.append("title and prompt must not be empty")

    required = {
        "README.md": kata.dir / "README.md",
        kata.module_file: kata.dir / kata.module_file,
        kata.test_file: kata.dir / kata.test_file,
        f".original/{kata.module_file}": kata.original_file,
        f"solutions/{kata.folder}/{kata.module_file}": kata.solution_file,
    }
    for name, path in required.items():
        if not path.is_file():
            errors.append(f"missing file: {name}")
    if errors:
        return errors

    for name, path in required.items():
        if TODO_MARK in path.read_text(encoding="utf-8"):
            errors.append(f"{name} still contains {TODO_MARK}")
    first_line = (kata.dir / "README.md").read_text(encoding="utf-8").splitlines()[0]
    if not first_line.startswith(f"# {kata.id} · "):
        errors.append(f"README.md must start with '# {kata.id} · <title>'")
    if errors:
        return errors

    if strict and kata.original_file.read_bytes() != (kata.dir / kata.module_file).read_bytes():
        errors.append(f"{kata.module_file} differs from .original/{kata.module_file}: don't commit a solved kata")

    buggy = run_with(kata, kata.original_file)
    if buggy.status == "skip":
        (errors if require_all else warnings).append(f"skipped: {buggy.detail}")
        return errors
    if buggy.passed:
        errors.append("tests PASS on the original code: a kata needs at least one failing test")
    elif "SyntaxError" in buggy.output:
        errors.append("the original code has a SyntaxError (it should fail on a *test*, not on parsing)")

    fixed = run_with(kata, kata.solution_file)
    if not fixed.passed:
        errors.append("tests FAIL with the reference solution:\n" + lib.tail(fixed.output or fixed.detail, 25))
    return errors


def main(argv=None) -> int:
    lib.setup_stdout()
    parser = argparse.ArgumentParser(description="Verify katas.")
    parser.add_argument("katas", nargs="*", help="kata number or part of its name (default: all)")
    parser.add_argument("--strict", action="store_true", help="require the working file to equal .original")
    parser.add_argument("--require-all", action="store_true", help="fail if a language runtime is missing")
    args = parser.parse_args(argv)

    katas = lib.load_katas()
    if not katas:
        print("No katas found.")
        return 1

    problems = 0
    ids = [k.id for k in katas]
    for dup in sorted({i for i in ids if ids.count(i) > 1}):
        print(f"❌ duplicate kata id: {dup}")
        problems += 1

    chosen = lib.select(katas, args.katas) if args.katas else katas
    warnings: List[str] = []
    for kata in chosen:
        errors = check_kata(kata, args.strict, args.require_all, warnings)
        if errors:
            problems += 1
            print(f"❌ {kata.folder}")
            for message in errors:
                print("   - " + message.replace("\n", "\n     "))
        else:
            print(f"✅ {kata.folder}")
    for warning in warnings:
        print(f"⚠️  {warning}")

    print()
    if problems:
        print(f"{problems} problem(s) found.")
        return 1
    print(f"All {len(chosen)} kata(s) verified: each fails on the original code and passes with its solution.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
