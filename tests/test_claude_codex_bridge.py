from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
INSTALLER = ROOT / "tools" / "install-frenemy.ps1"
DOC = ROOT / "docs" / "CLAUDE_CODEX_BRIDGE.md"


class ClaudeCodexBridgeTests(unittest.TestCase):
    def test_installer_pins_full_commit_sha(self) -> None:
        text = INSTALLER.read_text(encoding="utf-8")
        match = re.search(r'\$PinnedCommit\s*=\s*"([0-9a-f]{40})"', text)
        self.assertIsNotNone(match)
        self.assertEqual(
            match.group(1),
            "dd460e61c2ff932d019266c8701290274ed2b495",
        )

    def test_installer_verifies_required_commands_and_checkout(self) -> None:
        text = INSTALLER.read_text(encoding="utf-8")
        for command in ("git", "node", "claude", "codex"):
            self.assertIn(f"Assert-Command {command}", text)
        self.assertIn("git -C $InstallRoot rev-parse HEAD", text)
        self.assertIn("Pinned commit verification failed", text)

    def test_write_tool_is_not_auto_approved(self) -> None:
        installer = INSTALLER.read_text(encoding="utf-8")
        documentation = DOC.read_text(encoding="utf-8")
        self.assertNotIn("[mcp_servers.claude.tools.ask_claude_write]", installer)
        self.assertIn("Never auto-approve `ask_claude_write` globally", documentation)

    def test_policy_forbids_recursive_delegation_and_secrets(self) -> None:
        text = DOC.read_text(encoding="utf-8")
        self.assertIn("Do not permit recursive Claude → Codex → Claude", text)
        self.assertIn("Never store Claude, Anthropic, OpenAI, or GitHub credentials", text)


if __name__ == "__main__":
    unittest.main()
