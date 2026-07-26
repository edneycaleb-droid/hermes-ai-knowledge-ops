from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INSTALLERS = ROOT / "governance" / "skill_installers.json"
POWERSHELL = ROOT / "tools" / "install-skill-library.ps1"
SHELL = ROOT / "tools" / "install-skill-library.sh"
SKILL = ROOT / ".agents" / "skills" / "governed-skill-installer" / "SKILL.md"
WORKFLOW = ROOT / ".github" / "workflows" / "skill-installer.yml"


class GovernedSkillInstallerTests(unittest.TestCase):
    def test_selected_installer_is_fully_pinned(self) -> None:
        data = json.loads(INSTALLERS.read_text(encoding="utf-8"))
        selected = data["selected_installer"]
        self.assertEqual("vercel-labs/skills", selected["repository"])
        self.assertRegex(selected["version"], r"^\d+\.\d+\.\d+$")
        self.assertRegex(selected["reviewed_commit"], r"^[0-9a-f]{40}$")
        self.assertEqual("MIT", selected["license"])
        self.assertNotEqual("latest", selected["version"])

    def test_wrappers_pin_the_same_package_and_commit(self) -> None:
        data = json.loads(INSTALLERS.read_text(encoding="utf-8"))
        selected = data["selected_installer"]
        expected_package = f'{selected["npm_package"]}@{selected["version"]}'
        for path in (POWERSHELL, SHELL):
            text = path.read_text(encoding="utf-8")
            self.assertIn(expected_package, text)
            self.assertIn(selected["reviewed_commit"], text)
            self.assertNotRegex(text, r"skills@latest|npx\s+skills\s")
            self.assertIn("validate_skill_library.py", text)
            self.assertIn("--copy", text)
            for agent in ("codex", "claude-code", "hermes-agent"):
                self.assertIn(agent, text)

    def test_installer_skill_has_required_governance_sections(self) -> None:
        text = SKILL.read_text(encoding="utf-8")
        for heading in (
            "## Contract",
            "## Trigger conditions",
            "## Security rules",
            "## Evidence and reporting",
            "## Retry and stop",
        ):
            self.assertIn(heading, text)
        self.assertIn("skills@1.5.20", text)
        self.assertIn("Do not claim the user's workstation was modified", text)
        self.assertNotRegex(text, re.compile(r"(?i)(api[_ -]?key|token)\s*[:=]\s*['\"][A-Za-z0-9_-]{16,}"))

    def test_ci_performs_isolated_installation_smoke_test(self) -> None:
        text = WORKFLOW.read_text(encoding="utf-8")
        self.assertIn("node-version: 22.20.0", text)
        self.assertIn("install-skill-library.sh", text)
        self.assertIn("$RUNNER_TEMP/skill-home", text)
        for path in (
            ".codex/skills/governed-skill-installer/SKILL.md",
            ".claude/skills/governed-skill-installer/SKILL.md",
            ".hermes/skills/governed-skill-installer/SKILL.md",
        ):
            self.assertIn(path, text)


if __name__ == "__main__":
    unittest.main()
