import copy
import hashlib
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import json
import os
import subprocess
import sys
import tempfile
import threading
import unittest

from tools import check_local_hermes as check


TAG = "demo:7b"
PIN = "a" * 64


class LocalEndpointTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        class Handler(BaseHTTPRequestHandler):
            def dispatch(self):
                size = int(self.headers.get("Content-Length", 0))
                payload = json.loads(self.rfile.read(size)) if size else None
                self.server.calls.append((self.command, self.path, payload, self.headers.get("Authorization")))
                value = self.server.responses[self.path]
                if callable(value):
                    value = value(self.server.calls)
                status, raw = value if isinstance(value, tuple) else (200, json.dumps(value).encode())
                self.send_response(status)
                if status == 307:
                    self.send_header("Location", "/redirect-target")
                self.send_header("Content-Length", str(len(raw)))
                self.end_headers()
                self.wfile.write(raw)

            do_GET = do_POST = dispatch

            def log_message(self, *_args):
                pass

        cls.server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        cls.port = cls.server.server_port
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join()

    def setUp(self):
        self.server.calls = []
        self.tag = {"name": TAG, "model": TAG, "digest": PIN, "details": {"format": "gguf", "family": "demo"}}
        self.answer = {"model": TAG, "choices": [{"finish_reason": "stop", "message":
                       {"role": "assistant", "content": check.CANARY}}]}
        self.server.responses = {"/api/status": {"cloud": {"disabled": True}}, "/api/tags": {"models": [self.tag]},
                                 "/v1/models": {"data": [{"id": TAG}]}, "/v1/chat/completions": self.answer}

    def verify(self, **kwargs):
        return check.verify_route(self.port, TAG, **kwargs)

    def test_inventory_default_uses_reads_only_and_no_credentials(self):
        config, digest = self.verify()
        self.assertEqual(digest, PIN)
        self.assertEqual(config["model"], {"default": TAG, "base_url": f"http://127.0.0.1:{self.port}/v1",
                                            "provider": "custom"})
        self.assertEqual(config["fallback_providers"], [])
        self.assertEqual([c[1] for c in self.server.calls], ["/api/status", "/api/tags", "/v1/models", "/api/tags"])
        self.assertTrue(all(c[0] == "GET" and c[3] is None for c in self.server.calls))

    def test_opt_in_sends_one_fixed_message_no_tools_and_no_auth(self):
        self.verify(expected=PIN, smoke="chat")
        posts = [c for c in self.server.calls if c[0] == "POST"]
        self.assertEqual(len(posts), 1)
        _, path, payload, auth = posts[0]
        self.assertEqual(path, "/v1/chat/completions")
        self.assertEqual(payload["messages"], [{"role": "user", "content": f"Reply with exactly {check.CANARY}."}])
        self.assertNotIn("tools", payload)
        self.assertIsNone(auth)

    def test_unknown_or_enabled_cloud_holds_before_inspection_or_inference(self):
        for status in ({}, {"cloud": None}, {"cloud": {"disabled": False}}, {"cloud": {"disabled": "true"}}):
            with self.subTest(status=status):
                self.server.calls.clear()
                self.server.responses["/api/status"] = status
                with self.assertRaises(check.Held):
                    self.verify(smoke="chat")
                self.assertEqual([c[1] for c in self.server.calls], ["/api/status"])

    def test_remote_aliases_and_missing_or_changed_pins_do_not_dispatch(self):
        for prop in ({"remote_host": "https://example.invalid"}, {"remote_model": "hosted"},
                     {"digest": None}, {"digest": "b" * 64}, {"details": {}}, {"model": "different"}):
            with self.subTest(prop=prop):
                self.server.responses["/api/tags"] = {"models": [{**self.tag, **prop}]}
                with self.assertRaises(check.Held):
                    self.verify(expected=PIN, smoke="chat")
        self.assertFalse(any(c[0] == "POST" for c in self.server.calls))

    def test_requires_an_unambiguous_id_on_both_apis(self):
        for endpoint, field, row in [("/api/tags", "models", self.tag), ("/v1/models", "data", {"id": TAG})]:
            saved = self.server.responses[endpoint]
            for rows in ([], [row, row], None, ["bad row"]):
                self.server.responses[endpoint] = {field: rows}
                with self.subTest(endpoint=endpoint, rows=rows), self.assertRaises(check.Held):
                    self.verify(smoke="chat")
            self.server.responses[endpoint] = saved
        self.assertFalse(any(c[0] == "POST" for c in self.server.calls))

    def test_rechecks_manifest_even_after_a_successful_canary(self):
        def inventory(calls):
            digest = PIN if len([c for c in calls if c[1] == "/api/tags"]) == 1 else "b" * 64
            return {"models": [{**self.tag, "digest": digest}]}
        self.server.responses["/api/tags"] = inventory
        with self.assertRaisesRegex(check.Held, "changed during"):
            self.verify(smoke="chat")
        self.assertEqual(sum(c[0] == "POST" for c in self.server.calls), 1)

    def test_rejects_wrong_model_tool_calls_and_unfinished_or_wrong_replies(self):
        cases = [("model", "another"), ("finish_reason", "length"), ("role", "tool"),
                 ("content", "different reply"), ("tool_calls", [{"id": "fixture"}])]
        for key, value in cases:
            answer = copy.deepcopy(self.answer)
            target = answer if key == "model" else answer["choices"][0]
            if key not in ("model", "finish_reason"):
                target = target["message"]
            target[key] = value
            self.server.responses["/v1/chat/completions"] = answer
            with self.subTest(key=key), self.assertRaises(check.Held):
                self.verify(smoke="chat")
        self.assertEqual(sum(c[0] == "POST" for c in self.server.calls), len(cases))

    def test_tool_canary_requires_a_single_correct_structured_call_and_never_executes_it(self):
        call = {"type": "function", "function": {"name": "report_local_marker",
                                                "arguments": json.dumps({"marker": check.CANARY})}}
        answer = {"model": TAG, "choices": [{"finish_reason": "tool_calls",
                  "message": {"role": "assistant", "tool_calls": [call]}}]}
        self.server.responses["/v1/chat/completions"] = answer
        self.verify(smoke="tool")
        posts = [c for c in self.server.calls if c[0] == "POST"]
        self.assertEqual(len(posts), 1)
        self.assertEqual([t["function"]["name"] for t in posts[0][2]["tools"]], ["report_local_marker"])
        for calls in ([], [call, call], [{"type": "function", "function": {"name": "other"}}],
                      [{"type": "function", "function": {"name": "report_local_marker", "arguments": "not-json"}}],
                      [{"type": "function", "function": {"name": "report_local_marker", "arguments": "{}"}}]):
            answer["choices"][0]["message"]["tool_calls"] = calls
            with self.subTest(calls=calls), self.assertRaises(check.Held):
                self.verify(smoke="tool")
        self.assertEqual(sum(c[0] == "POST" for c in self.server.calls), 6)

    def test_redirects_errors_and_invalid_replies_stop_without_retry(self):
        for status, body in [(307, b""), (429, b"private"), (500, b"private"), (200, b"broken"), (200, b"[]")]:
            self.server.responses["/v1/chat/completions"] = (status, body)
            self.server.calls.clear()
            with self.assertRaises(check.Held) as error:
                self.verify(smoke="chat")
            self.assertNotIn("private", str(error.exception))
            self.assertEqual([c[1] for c in self.server.calls if c[0] == "POST"], ["/v1/chat/completions"])

    def test_cli_repeat_preserves_config_and_holds_preserve_old_bytes(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "candidate.yaml"
            argv = [sys.executable, str(Path(check.__file__)), "--port", str(self.port), "--model", TAG,
                    "--write-config", str(path)]
            env = {**os.environ, "HTTP_PROXY": "http://127.0.0.1:1", "NO_PROXY": ""}
            first = subprocess.run(argv, env=env, check=True, capture_output=True)
            self.assertEqual(json.loads(first.stdout)["config_sha256"], hashlib.sha256(path.read_bytes()).hexdigest())
            stat = path.stat()
            self.assertEqual(subprocess.run(argv, env=env, check=True, capture_output=True).stdout, first.stdout)
            self.assertEqual(path.stat().st_mtime_ns, stat.st_mtime_ns)
            path.write_bytes(b"existing profile")
            held = subprocess.run(argv, env=env, capture_output=True)
            self.assertEqual((held.returncode, json.loads(held.stderr)["status"], held.stdout), (1, "held", b""))
            self.assertEqual(path.read_bytes(), b"existing profile")
            self.server.responses["/api/status"] = {}
            other = Path(tmp) / "other.yaml"
            held = subprocess.run(argv[:-1] + [str(other)], env=env, capture_output=True)
            self.assertEqual(held.returncode, 1)
            self.assertFalse(other.exists())
