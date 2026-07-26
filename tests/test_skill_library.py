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

    def test_frenemy_skill_is_registered(self) -> None:
        data = json.loads(REGISTRY.read_text(encoding="utf-8"))
        entries = {entry["name"]: entry for entry in data["skills"]}
        skill = entries["claude-codex-frenemy-bridge"]
        self.assertEqual("review", skill["state"])
        self.assertEqual("1.0.0", skill["version"])
        self.assertIn("no automatic approval of write-capable delegation", skill["negative_contracts"])
        self.assertTrue((ROOT / skill["path"]).is_file())

    def test_library_policy_documents_implementation_to_skillization(self) -> None:
        policy = (ROOT / "docs" / "SKILL_LIBRARY.md").read_text(encoding="utf-8")
        self.assertIn("implement → verify → skillize → register", policy)
        self.assertIn("Never commit passwords, tokens, cookies, API keys", policy)
        self.assertIn("Never auto-approve write-capable tools", policy)


if __name__ == "__main__":
    unittest.main()
