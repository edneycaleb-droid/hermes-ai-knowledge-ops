from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "governance" / "unified_capability_forge.json"
SKILL_ROOT = ROOT / ".agents" / "skills"
EXPECTED_NEW_SKILLS = {
    "constraint-drift-radar",
    "counterfactual-sandbox-designer",
    "capability-compression-cartographer",
    "provenance-entropy-auditor",
    "failure-pattern-immunizer",
    "reversible-automation-designer",
    "interface-contract-miner",
    "agent-disagreement-resolver",
    "cross-project-opportunity-radar",
    "shadow-work-eliminator",
}
ALLOWED_DISPOSITIONS = {
    "adopt",
    "adapt",
    "archive",
    "blocked",
    "conditional",
    "discover",
    "fallback",
    "future-hardware",
    "quarantine",
    "reference",
    "reject",
    "sandbox",
}
UNSAFE_DEFAULTS = (
    "never stop",
    "do not ask permission",
    "auto_execute: true",
    "auto_install: true",
    "activation_requires_human_approval: false",
)
REQUIRED_SKILL_SECTIONS = ("# ", "## Contract", "## Workflow", "## Retry and stop", "## Output")


def _frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        return {}
    try:
        block = text.split("---\n", 2)[1]
    except IndexError:
        return {}
    result: dict[str, str] = {}
    for line in block.splitlines():
        if not line or line.startswith(" ") or ":" not in line:
            continue
        key, value = line.split(":", 1)
        result[key.strip()] = value.strip().strip('"')
    return result


def validate() -> list[str]:
    errors: list[str] = []
    if not REGISTRY.is_file():
        return [f"missing registry: {REGISTRY}"]

    try:
        data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [f"invalid registry JSON: {exc}"]

    if data.get("schema_version") != 1:
        errors.append("registry schema_version must be 1")

    invariants = data.get("hard_invariants") or []
    for phrase in ("No capability can promote itself", "OpenRouter remains disabled", "Every loop is bounded"):
        if not any(phrase in item for item in invariants):
            errors.append(f"missing hard invariant containing: {phrase}")

    sources = data.get("sources") or []
    repos = [item.get("repo") for item in sources]
    duplicates = sorted({repo for repo in repos if repo and repos.count(repo) > 1})
    if duplicates:
        errors.append(f"duplicate source repositories: {duplicates}")
    if len(sources) < 60:
        errors.append(f"expected at least 60 reviewed sources, found {len(sources)}")
    for index, item in enumerate(sources):
        repo = item.get("repo")
        disposition = item.get("disposition")
        if not isinstance(repo, str) or not re.fullmatch(r"[^/\s]+/[^/\s]+|callmux", repo):
            errors.append(f"sources[{index}] has invalid repo: {repo!r}")
        if disposition not in ALLOWED_DISPOSITIONS:
            errors.append(f"sources[{index}] has invalid disposition: {disposition!r}")

    blocked = {item["repo"] for item in sources if item.get("disposition") in {"blocked", "reject"}}
    for required in {"BaggaT236/AI-Trading-Skills", "luyu0279/BrainyAI"}:
        if required not in blocked:
            errors.append(f"required blocked source missing: {required}")

    ideas = data.get("new_ideas") or []
    if len(ideas) != 10:
        errors.append(f"expected exactly 10 new ideas, found {len(ideas)}")
    idea_ids = [item.get("id") for item in ideas]
    if len(set(idea_ids)) != len(idea_ids):
        errors.append("new idea ids must be unique")

    actual_skills = {path.parent.name for path in SKILL_ROOT.glob("*/SKILL.md")}
    missing = EXPECTED_NEW_SKILLS - actual_skills
    if missing:
        errors.append(f"missing new skills: {sorted(missing)}")

    for skill_name in sorted(EXPECTED_NEW_SKILLS):
        path = SKILL_ROOT / skill_name / "SKILL.md"
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        metadata = _frontmatter(text)
        if metadata.get("name") != skill_name:
            errors.append(f"{path}: frontmatter name mismatch")
        if not metadata.get("description"):
            errors.append(f"{path}: missing description")
        for section in REQUIRED_SKILL_SECTIONS:
            if section not in text:
                errors.append(f"{path}: missing section {section!r}")
        lowered = text.lower()
        for unsafe in UNSAFE_DEFAULTS:
            if unsafe in lowered:
                errors.append(f"{path}: unsafe default phrase {unsafe!r}")
        if "max_attempts" not in text and "max_rounds" not in text:
            errors.append(f"{path}: missing finite retry or round limit")
        if "Non-goals" not in text and "Non-goals" not in text:
            errors.append(f"{path}: missing explicit non-goals")

    return errors


def main() -> int:
    errors = validate()
    if errors:
        print("Unified Capability Forge validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Unified Capability Forge validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
