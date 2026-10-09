#!/usr/bin/env python3
"""Grade every kata and write progress files (used by the 'Grade my fork' workflow).

    python tools/progress.py [--out DIR]

Writes PROGRESS.md, progress.json and badge.json (a shields.io endpoint badge) into DIR.
The exit code is always 0 so your fork's CI stays green while you work through the katas.
"""
from __future__ import annotations

import argparse
import datetime
import json
import os
import sys
from pathlib import Path

import kata_lib as lib


def badge_color(solved: int, total: int) -> str:
    if total == 0 or solved == 0:
        return "lightgrey"
    if solved == total:
        return "brightgreen"
    if solved * 2 < total:
        return "orange"
    return "yellowgreen"


def main(argv=None) -> int:
    lib.setup_stdout()
    parser = argparse.ArgumentParser(description="Write progress files for this fork.")
    parser.add_argument("--out", default=".progress", help="output directory (default: .progress)")
    args = parser.parse_args(argv)

    katas = lib.load_katas()
    results = {}
    for kata in katas:
        results[kata.folder] = lib.run_tests(kata.dir, kata).status

    total = len(katas)
    solved = sum(1 for status in results.values() if status == "pass")
    skipped = sum(1 for status in results.values() if status == "skip")
    now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    repo = os.environ.get("GITHUB_REPOSITORY", "")
    server = os.environ.get("GITHUB_SERVER_URL", "https://github.com")
    run_id = os.environ.get("GITHUB_RUN_ID", "")
    run_url = f"{server}/{repo}/actions/runs/{run_id}" if repo and run_id else ""

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    icon = {"pass": "✅", "fail": "⬜", "skip": "⏭️"}
    rows = []
    for kata in katas:
        rows.append(
            f"| {kata.id} | [{kata.slug}](katas/{kata.folder}/) | {kata.lang} | "
            f"{lib.LEVEL_STARS[kata.level]} | {icon[results[kata.folder]]} |"
        )
    footer = f"_Updated {now}_" + (f" · [workflow run]({run_url})" if run_url else "")
    markdown = "\n".join(
        [
            "# My would-you-merge progress",
            "",
            f"**{solved} / {total}** bugs caught and fixed" + (f" ({skipped} skipped: runtime missing)" if skipped else ""),
            "",
            "| # | Kata | Language | Level | Status |",
            "|---|------|----------|-------|--------|",
            *rows,
            "",
            footer,
            "",
        ]
    )
    (out / "PROGRESS.md").write_text(markdown, encoding="utf-8", newline="\n")

    payload = {
        "solved": solved,
        "total": total,
        "skipped": skipped,
        "katas": results,
        "generated_at": now,
        "repo": repo,
        "sha": os.environ.get("GITHUB_SHA", ""),
        "run_url": run_url,
    }
    (out / "progress.json").write_text(json.dumps(payload, indent=2), encoding="utf-8", newline="\n")

    badge = {
        "schemaVersion": 1,
        "label": "bugs caught",
        "message": f"{solved}/{total}",
        "color": badge_color(solved, total),
    }
    (out / "badge.json").write_text(json.dumps(badge), encoding="utf-8", newline="\n")

    github_output = os.environ.get("GITHUB_OUTPUT")
    if github_output:
        with open(github_output, "a", encoding="utf-8") as handle:
            handle.write(f"score={solved}/{total}\n")

    print(f"Fixed {solved}/{total} katas ({skipped} skipped). Files written to {out}/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
