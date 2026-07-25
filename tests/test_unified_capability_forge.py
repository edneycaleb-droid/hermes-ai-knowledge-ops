from __future__ import annotations

import importlib.util
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class UnifiedCapabilityForgeTests(unittest.TestCase):
    def setUp(self) -> None:
        self.registry_path = ROOT / "governance" / "unified_capability_forge.json"
        self.registry = json.loads(self.registry_path.read_text(encoding="utf-8"))

    def test_registry_contains_reviewed_ecosystem_and_ten_new_ideas(self) -> None:
        self.assertGreaterEqual(len(self.registry["sources"]), 60)
        self.assertEqual(len(self.registry["new_ideas"]), 10)
        self.assertEqual(len({item["repo"] for item in self.registry["sources"]}), len(self.registry["sources"]))

    def test_execution_and_trading_boundaries_are_explicit(self) -> None:
        invariants = "\n".join(self.registry["hard_invariants"])
        self.assertIn("No capability can promote itself", invariants)
        self.assertIn("No trading capability can place orders", invariants)
        self.assertIn("OpenRouter remains disabled", invariants)
        self.assertIn("Every loop is bounded", invariants)

    def test_required_sources_have_fail_closed_dispositions(self) -> None:
        dispositions = {item["repo"]: item["disposition"] for item in self.registry["sources"]}
        self.assertEqual(dispositions["BaggaT236/AI-Trading-Skills"], "blocked")
        self.assertEqual(dispositions["luyu0279/BrainyAI"], "reject")
        self.assertEqual(dispositions["moss-site/moss-trade-bot-skills"], "quarantine")
        self.assertEqual(dispositions["browser-act/skills"], "quarantine")

    def test_validator_passes_repository_state(self) -> None:
        path = ROOT / "scripts" / "validate_unified_capability_forge.py"
        spec = importlib.util.spec_from_file_location("validate_unified_capability_forge", path)
        module = importlib.util.module_from_spec(spec)
        assert spec.loader
        spec.loader.exec_module(module)
        self.assertEqual(module.validate(), [])

    def test_exactly_ten_new_skill_packages_exist(self) -> None:
        expected = {
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
        actual = {path.parent.name for path in (ROOT / ".agents" / "skills").glob("*/SKILL.md")}
        self.assertTrue(expected.issubset(actual))


if __name__ == "__main__":
    unittest.main()
