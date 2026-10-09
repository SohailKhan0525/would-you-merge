"""Shared helpers for the would-you-merge tooling. Standard library only (Python 3.10+)."""
from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Sequence

ROOT = Path(__file__).resolve().parent.parent
KATAS_DIR = ROOT / "katas"
SOLUTIONS_DIR = ROOT / "solutions"

EXT = {"python": ".py", "javascript": ".js"}
LEVEL_STARS = {1: "★☆☆", 2: "★★☆", 3: "★★★"}
CATEGORY_EMOJI = {
    "hallucination": "👻",
    "boundaries": "📏",
    "security": "🔐",
    "async": "⏳",
    "data": "🧮",
    "errors": "🙈",
    "logic": "🧠",
    "performance": "🐌",
}
FOLDER_RE = re.compile(r"^(\d{2})-([a-z0-9]+(?:-[a-z0-9]+)*)$")
MIN_NODE_MAJOR = 20


def setup_stdout() -> None:
    """Make emoji output safe on consoles that default to a legacy encoding."""
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[attr-defined]
        except (AttributeError, ValueError):
            pass


@dataclass
class Kata:
    id: str
    slug: str
    title: str
    lang: str
    module: str
    level: int
    category: str
    prompt: str
    dir: Path

    @property
    def folder(self) -> str:
        return f"{self.id}-{self.slug}"

    @property
    def module_file(self) -> str:
        return self.module + EXT[self.lang]

    @property
    def test_file(self) -> str:
        if self.lang == "python":
            return f"test_{self.module}.py"
        return f"{self.module}.test.js"

    @property
    def original_file(self) -> Path:
        return self.dir / ".original" / self.module_file

    @property
    def solution_file(self) -> Path:
        return SOLUTIONS_DIR / self.folder / self.module_file


def load_katas(root: Optional[Path] = None) -> List[Kata]:
    katas_dir = (root or ROOT) / "katas"
    katas: List[Kata] = []
    if not katas_dir.is_dir():
        return katas
    for folder in sorted(p for p in katas_dir.iterdir() if p.is_dir()):
        meta_path = folder / "kata.json"
        if not meta_path.is_file():
            continue
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
        katas.append(
            Kata(
                id=str(meta["id"]),
                slug=str(meta["slug"]),
                title=str(meta["title"]),
                lang=str(meta["lang"]),
                module=str(meta["module"]),
                level=int(meta["level"]),
                category=str(meta["category"]),
                prompt=str(meta["prompt"]),
                dir=folder,
            )
        )
    return katas


def select(katas: Sequence[Kata], selectors: Sequence[str]) -> List[Kata]:
    """Pick katas by number ('7', '07') or by part of the slug/title ('chunk')."""
    chosen: List[Kata] = []
    for selector in selectors:
        text = selector.strip().lower()
        if text.isdigit():
            matches = [k for k in katas if int(k.id) == int(text)]
        else:
            matches = [k for k in katas if text in k.slug or text in k.title.lower()]
        if not matches:
            raise SystemExit(f"No kata matches {selector!r}. Try: python tools/check.py --list")
        for match in matches:
            if match not in chosen:
                chosen.append(match)
    return chosen


def runtime_problem(lang: str) -> Optional[str]:
    """Return a human-readable reason this language can't run here, or None."""
    if lang == "python":
        return None
    node = shutil.which("node")
    if not node:
        return "Node.js not found (install Node 20+ to play the JavaScript katas)"
    try:
        out = subprocess.run([node, "--version"], capture_output=True, text=True, timeout=15).stdout.strip()
        major = int(out.lstrip("v").split(".")[0])
    except (OSError, ValueError, subprocess.SubprocessError):
        return "could not determine the Node.js version"
    if major < MIN_NODE_MAJOR:
        return f"Node {out} is too old (need {MIN_NODE_MAJOR}+)"
    return None


@dataclass
class Result:
    status: str  # "pass" | "fail" | "skip"
    output: str = ""
    detail: str = ""

    @property
    def passed(self) -> bool:
        return self.status == "pass"


def run_tests(workdir: Path, kata: Kata, timeout: int = 60) -> Result:
    """Run a kata's tests inside `workdir` (a kata folder or a copy of one)."""
    problem = runtime_problem(kata.lang)
    if problem:
        return Result("skip", "", problem)
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["NODE_NO_WARNINGS"] = "1"
    if kata.lang == "python":
        cmd = [sys.executable, "-m", "unittest", "-q", Path(kata.test_file).stem]
    else:
        cmd = [shutil.which("node") or "node", "--test", "--test-reporter=spec", kata.test_file]
    try:
        proc = subprocess.run(
            cmd, cwd=str(workdir), env=env, capture_output=True, text=True, timeout=timeout
        )
    except subprocess.TimeoutExpired:
        return Result("fail", "", f"timed out after {timeout}s")
    except OSError as exc:
        return Result("skip", "", f"could not start the test runner: {exc}")
    output = (proc.stdout or "") + (proc.stderr or "")
    return Result("pass" if proc.returncode == 0 else "fail", output)


def tail(text: str, lines: int = 40) -> str:
    parts = text.strip().splitlines()
    if len(parts) <= lines:
        return "\n".join(parts)
    return "\n".join(["..."] + parts[-lines:])


_NOISE = re.compile(r"node:|startSubtestAfterBootstrap|^\s*(generatedMessage|code|operator|diff):|^ℹ ")


def friendly(text: str) -> str:
    """Drop test-runner internals (stack frames, summary counters) so beginners see the useful part."""
    kept = [line for line in text.splitlines() if not _NOISE.search(line)]
    return "\n".join(kept)
