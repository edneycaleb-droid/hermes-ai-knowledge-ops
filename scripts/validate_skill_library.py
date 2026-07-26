from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "governance" / "skill_library.json"
SEMVER = re.compile(r"^\d+\.\d+\.\d+$")
NAME = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


class ValidationError(RuntimeError):
    pass


def _frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        raise ValidationError("skill must start with YAML frontmatter")
    end = text.find("\n---\n", 4)
    if end < 0:
        raise ValidationError("skill frontmatter is not terminated")

    values: dict[str, str] = {}
    metadata = False
    for raw in text[4:end].splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        indent = len(raw) - len(raw.lstrip())
        line = raw.strip()
        if line == "metadata:":
            metadata = True
            continue
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip().strip('"\'')
        if indent and metadata:
            values[f"metadata.{key}"] = value
        elif not indent:
            metadata = False
            values[key] = value
    return values


def validate() -> list[str]:
    errors: list[str] = []
    if not REGISTRY.exists():
        return [f"missing registry: {REGISTRY.relative_to(ROOT)}"]

    data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    root = ROOT / data.get("canonical_root", "")
    states = set(data.get("lifecycle_states", []))
    required = data.get("required_frontmatter", [])
    skills = data.get("skills", [])

    seen_names: set[str] = set()
    seen_paths: set[str] = set()

    for entry in skills:
        name = entry.get("name", "")
        path = entry.get("path", "")
        version = entry.get("version", "")
        state = entry.get("state", "")

        if not NAME.fullmatch(name):
            errors.append(f"invalid skill name: {name!r}")
        if name in seen_names:
            errors.append(f"duplicate skill name: {name}")
        seen_names.add(name)

        if path in seen_paths:
            errors.append(f"duplicate skill path: {path}")
        seen_paths.add(path)

        skill_path = ROOT / path
        try:
            skill_path.relative_to(root)
        except ValueError:
            errors.append(f"skill path outside canonical root: {path}")

        if not skill_path.is_file():
            errors.append(f"missing skill file: {path}")
            continue

        try:
            fm = _frontmatter(skill_path.read_text(encoding="utf-8"))
        except ValidationError as exc:
            errors.append(f"{path}: {exc}")
            continue

        for key in required:
            if not fm.get(key):
                errors.append(f"{path}: missing frontmatter {key}")

        if fm.get("name") != name:
            errors.append(f"{path}: registry name does not match frontmatter")
        if fm.get("metadata.version") != version:
            errors.append(f"{path}: registry version does not match frontmatter")
        if fm.get("metadata.profile") != entry.get("profile"):
            errors.append(f"{path}: registry profile does not match frontmatter")
        if not SEMVER.fullmatch(version):
            errors.append(f"{path}: invalid semantic version {version!r}")
        if state not in states:
            errors.append(f"{path}: invalid lifecycle state {state!r}")
        if not entry.get("capabilities"):
            errors.append(f"{path}: capabilities must not be empty")
        if not entry.get("negative_contracts"):
            errors.append(f"{path}: negative_contracts must not be empty")

        body = skill_path.read_text(encoding="utf-8").lower()
        for heading in ("## contract", "## trigger conditions", "## retry and stop"):
            if heading not in body:
                errors.append(f"{path}: missing required section {heading}")

    return errors


def main() -> int:
    errors = validate()
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("Skill library validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
