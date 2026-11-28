"""Prepare Hermes model settings from an existing loopback Ollama installation."""

import argparse
import hashlib
import http.client
import json
import os
from pathlib import Path
import re
import sys
import tempfile


MAX_BYTES = 2 * 1024 * 1024
DIGEST = re.compile(r"[0-9a-f]{64}")
MODEL = re.compile(r"[A-Za-z0-9][A-Za-z0-9._:/-]{0,254}")
HOST = "127.0.0.1"
CANARY = "HERMES_LOCAL_OK"


class Held(ValueError):
    """The available evidence does not establish a usable local route."""


def request(port, path, payload=None):
    connection = http.client.HTTPConnection(HOST, port, timeout=45 if payload else 5)
    try:
        data = json.dumps(payload).encode() if payload is not None else None
        connection.request("POST" if data else "GET", path, body=data,
                           headers={"Content-Type": "application/json"} if data else {})
        response = connection.getresponse()
        if response.status != 200:
            raise Held(f"{path} returned HTTP {response.status}")
        raw = response.read(MAX_BYTES + 1)
        if len(raw) > MAX_BYTES:
            raise Held(f"{path} exceeded the response size limit")
        obj = json.loads(raw)
        if not isinstance(obj, dict):
            raise Held(f"{path} did not return an object")
        return obj
    except (OSError, http.client.HTTPException, UnicodeError, json.JSONDecodeError) as exc:
        raise Held(f"{path} unavailable ({type(exc).__name__})") from None
    finally:
        connection.close()


def models_in(obj, field):
    rows = obj.get(field)
    if not isinstance(rows, list) or not all(isinstance(row, dict) for row in rows):
        raise Held(f"invalid model inventory ({field})")
    return rows


def local_digest(port, name):
    rows = [row for row in models_in(request(port, "/api/tags"), "models")
            if name in (row.get("name"), row.get("model"))]
    if len(rows) != 1:
        raise Held("the selected tag is missing or ambiguous in Ollama")
    row = rows[0]
    if row.get("name") != name or row.get("model", name) != name:
        raise Held("the inventory disagrees about the model name")
    if row.get("remote_host") or row.get("remote_model"):
        raise Held("Ollama reports remote inference for this tag")
    digest = row.get("digest")
    if not isinstance(digest, str) or not DIGEST.fullmatch(digest.removeprefix("sha256:")):
        raise Held("Ollama did not supply a valid manifest digest")
    details = row.get("details")
    if not isinstance(details, dict) or not details.get("format") or not details.get("family"):
        raise Held("Ollama did not supply local model metadata")
    return digest.removeprefix("sha256:")


def verify_reply(port, name, mode):
    tool = "report_local_marker"
    payload = {"model": name, "stream": False, "temperature": 0, "max_tokens": 64,
               "messages": [{"role": "user", "content": f"Reply with exactly {CANARY}."}]}
    if mode == "tool":
        payload["messages"][0]["content"] = f"Call {tool} once with marker {CANARY}."
        payload["tools"] = [{"type": "function", "function": {
            "name": tool, "description": "Report the marker for this synthetic test.",
            "parameters": {"type": "object", "properties": {"marker": {"type": "string"}},
                           "required": ["marker"]}}}]
    answer = request(port, "/v1/chat/completions", payload)
    choices = answer.get("choices")
    choice = choices[0] if isinstance(choices, list) and len(choices) == 1 else None
    message = choice.get("message") if isinstance(choice, dict) else None
    if answer.get("model") != name or not isinstance(message, dict) or message.get("role") != "assistant":
        raise Held("the response did not identify the selected model and an assistant message")
    if mode == "tool":
        calls = message.get("tool_calls")
        call = calls[0] if isinstance(calls, list) and len(calls) == 1 else {}
        func = call.get("function") if isinstance(call, dict) and call.get("type") == "function" else None
        if choice.get("finish_reason") != "tool_calls" or not isinstance(func, dict) or func.get("name") != tool:
            raise Held("the model did not request the declared test function")
        try:
            arguments = json.loads(func.get("arguments", ""))
        except (TypeError, ValueError):
            raise Held("the model did not return valid tool arguments") from None
        if arguments != {"marker": CANARY}:
            raise Held("the tool call did not carry the expected marker")
    elif (choice.get("finish_reason") != "stop" or message.get("tool_calls") or message.get("function_call")
          or not isinstance(message.get("content"), str) or message["content"].strip() != CANARY):
        raise Held("the model did not return the fixed reply")


def verify_route(port, name, expected=None, smoke=None):
    if not 1 <= port <= 65535 or not MODEL.fullmatch(name):
        raise Held("specify a valid port and an exact Ollama model tag")
    if expected is not None and not DIGEST.fullmatch(expected):
        raise Held("the expected digest must be 64 lowercase hex digits")
    cloud = request(port, "/api/status").get("cloud")
    if not isinstance(cloud, dict) or cloud.get("disabled") is not True:
        raise Held("the server has not confirmed cloud inference is disabled")
    digest = local_digest(port, name)
    if expected is not None and expected != digest:
        raise Held("the installed manifest differs from the expected digest")
    available = models_in(request(port, "/v1/models"), "data")
    if sum(row.get("id") == name for row in available) != 1:
        raise Held("the exact model ID is missing or ambiguous on the Hermes API route")
    if smoke:
        verify_reply(port, name, smoke)
    if local_digest(port, name) != digest:
        raise Held("the manifest changed during verification")
    return {"model": {"provider": "custom", "base_url": f"http://{HOST}:{port}/v1", "default": name},
            "fallback_providers": []}, digest


def write_candidate(path, raw):
    """Publish one complete candidate atomically, without replacing an existing file."""
    tmp = tempfile.NamedTemporaryFile(dir=path.parent, delete=False)
    temp = Path(tmp.name)
    try:
        with tmp:
            tmp.write(raw)
        try:
            os.link(temp, path)
        except FileExistsError:
            if path.is_symlink() or not path.is_file() or path.stat().st_size != len(raw) or path.read_bytes() != raw:
                raise Held("a different file already exists at the candidate path") from None
    finally:
        temp.unlink(missing_ok=True)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", required=True, help="exact installed tag, including its version")
    parser.add_argument("--port", type=int, default=11434)
    parser.add_argument("--expect-digest", help="require this previously recorded manifest SHA-256")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--smoke", dest="smoke", action="store_const", const="chat",
                      help="send one fixed, tool-free chat request")
    mode.add_argument("--tool-smoke", dest="smoke", action="store_const", const="tool",
                      help="ask for one synthetic tool call and inspect it without executing it")
    parser.add_argument("--write-config", type=Path, help="create a separate candidate config.yaml")
    args = parser.parse_args(argv)
    try:
        config, digest = verify_route(args.port, args.model, args.expect_digest, args.smoke)
        raw = (json.dumps(config, indent=2) + "\n").encode()
        if args.write_config:
            write_candidate(args.write_config, raw)
    except (Held, OSError) as exc:
        reason = str(exc) if isinstance(exc, Held) else f"file operation failed ({type(exc).__name__})"
        print(json.dumps({"status": "held", "reason": reason}), file=sys.stderr)
        return 1
    print(json.dumps({"status": f"{args.smoke}_verified" if args.smoke else "inventory_verified",
                      "model_manifest_sha256": digest, "config_sha256": hashlib.sha256(raw).hexdigest(),
                      "config": config}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
