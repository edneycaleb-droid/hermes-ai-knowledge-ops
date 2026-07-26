from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts.validate_skill_library import ROOT, REGISTRY, validate


class SkillLibraryTests(unittest.TestCase):
    def test_registry_and_registered_skills_are_valid(self) -> None:
        self.assertEqual([], validate())

    def test_library_is_review_gated_and_safe_by_default(self) -> None:
        data = json.loads(REGISTRY.read_text(encoding="utf-8"))
        governance = data["governance"]
        self.assertTrue(governance["review_required"])
        self.assertTrue(governance["self_promotion_forbidden"])
        self.assertTrue(governance["credentials_forbidden"])
        self.assertTrue(governance["floating_upstream_refs_forbidden"])
        self.assertTrue(governance["write_capabilities_require_explicit_approval"])

    def test_core_reusable_skills_are_registered(self) -> None:
        data = json.loads(REGISTRY.read_text(encoding="utf-8"))
        entries = {entry["name"]: entry for entry in data["skills"]}

        frenemy = entries["claude-codex-frenemy-bridge"]
        self.assertEqual("review", frenemy["state"])
        self.assertEqual("1.0.0", frenemy["version"])
        self.assertIn("no automatic approval of write-capable delegation", frenemy["negative_contracts"])
        self.assertTrue((ROOT / frenemy["path"]).is_file())

        installer = entries["governed-skill-installer"]
        self.assertEqual("review", installer["state"])
        self.assertEqual("1.0.0", installer["version"])
        self.assertIn("no floating installer package version", installer["negative_contracts"])
        self.assertTrue((ROOT / installer["path"]).is_file())

    def test_library_policy_documents_full_lifecycle(self) -> None:
        policy = (ROOT / "docs" / "SKILL_LIBRARY.md").read_text(encoding="utf-8")
        self.assertIn("implement → verify → skillize → register", policy)
        self.assertIn("review → install → runtime verify", policy)
        self.assertIn("Never commit passwords, tokens, cookies, API keys", policy)
        self.assertIn("Never auto-approve write-capable tools", policy)
        self.assertIn("only `approved` skills", policy)


if __name__ == "__main__":
    unittest.main()
