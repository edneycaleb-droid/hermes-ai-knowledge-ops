from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "governance" / "skill_library.json"


def select(requested: list[str], allowed_states: set[str]) -> list[str]:
    data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    entries = {entry["name"]: entry for entry in data["skills"]}

    names = list(entries) if requested == ["*"] else requested
    selected: list[str] = []
    errors: list[str] = []

    for name in names:
        entry = entries.get(name)
        if entry is None:
            errors.append(f"unknown registered skill: {name}")
            continue
        state = entry["state"]
        if state not in allowed_states:
            errors.append(
                f"skill {name!r} is in lifecycle state {state!r}; "
                f"allowed states: {', '.join(sorted(allowed_states))}"
            )
            continue
        selected.append(name)

    if errors:
        raise ValueError("; ".join(errors))
    return selected


def main() -> int:
    parser = argparse.ArgumentParser(description="Select registered skills eligible for installation.")
    parser.add_argument("--skill", action="append", dest="skills", default=[])
    parser.add_argument("--state", action="append", dest="states", default=[])
    args = parser.parse_args()

    requested = args.skills or ["*"]
    allowed_states = set(args.states or ["approved"])

    try:
        selected = select(requested, allowed_states)
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    for name in selected:
        print(name)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
