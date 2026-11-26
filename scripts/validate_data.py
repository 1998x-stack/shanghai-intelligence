#!/usr/bin/env python3
"""Fail closed for malformed published intelligence and incomplete vendored Skill files."""
from __future__ import annotations
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from build_site import TOPICS, DISTRICTS, SOURCES, REPORTS, load_events  # noqa: E402


def verify_snapshot() -> None:
    manifest = json.loads((ROOT / "config/olah-snapshot-manifest.json").read_text(encoding="utf-8"))
    prefix = ROOT / ".pi/skills/Olah-style-posts"
    expected = {x["path"]: x["sha"] for x in manifest["files"]}
    actual_paths = {str(p.relative_to(prefix)).replace("\\", "/") for p in prefix.rglob("*") if p.is_file()}
    if actual_paths != set(expected):
        missing = sorted(set(expected) - actual_paths)
        extra = sorted(actual_paths - set(expected))
        raise ValueError(f"Olah snapshot paths mismatch: missing={missing}, extra={extra}")
    for relative, wanted in expected.items():
        payload = (prefix / relative).read_bytes()
        got = hashlib.sha1(b"blob " + str(len(payload)).encode() + b"\0" + payload).hexdigest()
        if got != wanted:
            raise ValueError(f"Olah snapshot SHA mismatch: {relative}: {got} != {wanted}")
    skill = ROOT / ".pi/skills/olah-style-paper-posts/SKILL.md"
    if not skill.is_file():
        raise ValueError("Pi skill entry is missing")
    for relative in expected:
        if relative.startswith("skills/olah-style-paper-posts/"):
            path = ROOT / ".pi/skills/olah-style-paper-posts" / relative.removeprefix("skills/olah-style-paper-posts/")
            if not path.is_file():
                raise ValueError(f"Missing native Pi skill file: {path}")
    print(f"Verified Olah mirror: {len(expected)} exact upstream blobs")


def main() -> None:
    assert len(TOPICS) == 7, "Expected seven editorial topics"
    assert len(DISTRICTS) == 16, "Expected Shanghai's 16 districts"
    assert len({x["id"] for x in TOPICS}) == len(TOPICS), "Duplicate topic IDs"
    assert len({x["id"] for x in DISTRICTS}) == len(DISTRICTS), "Duplicate district IDs"
    assert all(x["type"] in ("official", "discovery") for x in SOURCES)
    assert isinstance(REPORTS, list)
    verified = load_events()
    verify_snapshot()
    print(f"Data validation passed: {len(verified)} publicly verified events")


if __name__ == "__main__":
    main()
