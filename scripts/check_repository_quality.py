#!/usr/bin/env python3
"""Deterministic, network-free ten-control repository quality validator."""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
QUALITY_WORKFLOW = ".github/workflows/agent-platform.yml"
CONTROLS = {
    "readme_status": ["README.md", "STATUS.md"],
    "contributing": ["CONTRIBUTING.md"],
    "security_private_reporting": ["SECURITY.md"],
    "codeowners": [".github/CODEOWNERS"],
    "issue_forms": [".github/ISSUE_TEMPLATE/bug.yml", ".github/ISSUE_TEMPLATE/research.yml", ".github/ISSUE_TEMPLATE/config.yml"],
    "pull_request_template": [".github/pull_request_template.md"],
    "dependency_policy": [".github/dependabot.yml"],
    "deterministic_fallback": ["scripts/check_repository_quality.py"],
    "safe_workflow": [QUALITY_WORKFLOW],
    "clean_tracking": [".github/ISSUE_TEMPLATE/config.yml"],
}

failures = []
for control, paths in CONTROLS.items():
    missing = [path for path in paths if not (ROOT / path).is_file()]
    if missing:
        failures.append(f"{control}: missing {', '.join(missing)}")

def text(path):
    return (ROOT / path).read_text(encoding="utf-8")

if not failures:
    security = text("SECURITY.md").lower()
    workflow = text(QUALITY_WORKFLOW)
    steps = re.split(r"(?m)^      - ", workflow)
    validator = next((step for step in steps if re.search(
        r"(?m)^        run: python3? scripts/check_repository_quality\.py[ \t]*$", step)), "")
    checkout = next((step for step in steps if step.startswith("uses: actions/checkout@")), "")
    sources = text("sources/official.yml")
    owners = text(".github/CODEOWNERS")
    intake = text(".github/ISSUE_TEMPLATE/config.yml")
    checks = [
        ("security_private_reporting", "security/advisories/new" in security and "public issue" in security),
        ("valid_codeowners", "@edneycaleb-droid" in owners),
        ("private_issue_routing", "blank_issues_enabled: false" in intake and "security/advisories/new" in intake),
        ("read_only_permissions", re.search(r"(?m)^permissions:\n  contents: read[ \t]*\n(?=\n|[^ \t])", workflow) is not None),
        ("immutable_checkout", re.search(r"^uses: actions/checkout@[0-9a-f]{40}(?:[ \t]|$)", checkout) is not None),
        ("credentials_disabled", re.search(r"(?m)^          persist-credentials: false[ \t]*$", checkout) is not None),
        ("bounded_runtime", re.search(r"(?m)^        timeout-minutes: 5[ \t]*$", validator) is not None),
        ("offline_validator_executed", bool(validator)),
        ("source_execution_blocked", "execute_discovered_code: false" in sources),
        ("source_install_blocked", "install_discovered_code: false" in sources),
    ]
    failures.extend(name for name, passed in checks if not passed)

if failures:
    print("REPOSITORY_QUALITY_SCORE=FAIL")
    for failure in failures:
        print(f"- {failure}")
    sys.exit(1)

print("REPOSITORY_QUALITY_SCORE=10/10")
print("controls=" + ",".join(CONTROLS))
