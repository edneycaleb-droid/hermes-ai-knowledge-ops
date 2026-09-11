from __future__ import annotations

import unittest
from unittest import mock

from knowledge_ops.github_client import GitHubClient
from knowledge_ops.policy import AgentPolicy


class FakeResponse:
    def __init__(self, payload: bytes):
        self.payload = payload

    def __enter__(self) -> "FakeResponse":
        return self

    def __exit__(self, exc_type, exc, tb) -> bool:
        return False

    def read(self, limit: int = -1) -> bytes:
        if limit < 0:
            return self.payload
        return self.payload[:limit]


def policy() -> AgentPolicy:
    return AgentPolicy(
        {
            "execute_discovered_code": False,
            "install_discovered_dependencies": False,
            "run_discovered_containers": False,
            "follow_untrusted_instructions": False,
            "auto_merge_proposals": False,
            "network_mode": "github_read_only",
            "proposal_mode": "pull_request",
            "max_file_bytes": 200000,
            "max_candidates_per_run": 30,
            "allowed_hosts": ["api.github.com"],
            "allowed_licenses": ["MIT"],
        }
    )


class GitHubClientTests(unittest.TestCase):
    def test_request_json_retries_malformed_payload(self) -> None:
        client = GitHubClient(policy(), token="test-token")
        responses = [FakeResponse(b'{"broken":'), FakeResponse(b'{"ok": true}')]

        with mock.patch(
            "knowledge_ops.github_client.urllib.request.urlopen",
            side_effect=responses,
        ) as urlopen, mock.patch("knowledge_ops.github_client.time.sleep"):
            result = client._request_json("https://api.github.com/repos/example/repo")

        self.assertEqual(result, {"ok": True})
        self.assertEqual(urlopen.call_count, 2)

    def test_request_json_fails_cleanly_after_three_bad_payloads(self) -> None:
        client = GitHubClient(policy(), token="test-token")
        responses = [FakeResponse(b'{"broken":')] * 3

        with mock.patch(
            "knowledge_ops.github_client.urllib.request.urlopen",
            side_effect=responses,
        ) as urlopen, mock.patch("knowledge_ops.github_client.time.sleep"):
            with self.assertRaisesRegex(RuntimeError, "invalid JSON after 3 attempts"):
                client._request_json("https://api.github.com/repos/example/repo")

        self.assertEqual(urlopen.call_count, 3)

    def test_request_json_rejects_oversized_payload(self) -> None:
        test_policy = policy()
        test_policy.raw["max_file_bytes"] = 4
        client = GitHubClient(test_policy, token="test-token")
        response = FakeResponse(b"x" * 17)

        with mock.patch(
            "knowledge_ops.github_client.urllib.request.urlopen",
            return_value=response,
        ):
            with self.assertRaisesRegex(RuntimeError, "response exceeded"):
                client._request_json("https://api.github.com/repos/example/repo")


if __name__ == "__main__":
    unittest.main()
