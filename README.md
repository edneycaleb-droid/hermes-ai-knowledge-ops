# Hermes AI Knowledge Ops

Autonomous, review-gated discovery and integration intelligence for Hermes Agent skills, tools, MCP servers, plugins, profiles, cron, and learning-loop capabilities.

This repository runs an autonomous **eleven-agent** knowledge-operations loop that
discovers GitHub projects, classifies skills/tools/MCP servers, deduplicates forks,
records provenance, performs static security screening, extracts integration metadata,
checks compatibility, learns from bounded reviewer feedback, scores ten quality
controls, makes a decision, and generates disabled implementation adapters plus
reviewable pull requests.

## Safety boundary

The discovery loop never installs dependencies from discovered repositories, never
executes discovered code or containers, never follows instructions embedded in
untrusted content, and never merges its own proposals. Critical static findings are
blocked. Every generated adapter is `disabled_pending_review`.

## Agents

1. Discovery
2. Deduplication
3. Classification
4. Provenance
5. Security
6. Extraction
7. Compatibility
8. Bounded learning
9. Ten-control quality scoring
10. Decision
11. Proposal and disabled adapter generation

## Continuous operation

`.github/workflows/autonomous-research.yml` runs at minutes 7 and 37 of every hour.
It scans GitHub with read-only API calls, runs all tests and gates, and opens or refreshes
a pull request containing `generated/` proposals. It does not push to `main`.

Run locally:

```bash
python -m pip install -e .
python -m knowledge_ops
python scripts/run_all_checks.py
python -m knowledge_ops.service
```

Service endpoints:

- `GET /health`
- `GET /ready`
- `GET /metrics`
- `GET /catalog`
- `POST /run` with `Authorization: Bearer $KNOWLEDGE_OPS_RUN_TOKEN`

## dlt verified-source ingestion

GitHub has an official dlt verified source. The optional pipeline loads seed-repository
events incrementally into DuckDB:

```bash
python -m pip install -r requirements-dlt.txt
dlt --non-interactive --yes --disable-telemetry init github duckdb
python pipelines/github_verified_pipeline.py
```

Real credentials belong in `.dlt/secrets.toml` or environment variables; that file is
gitignored. The scheduled dlt workflow stores the DuckDB file as a short-lived Actions
artifact rather than committing database state.

## CreateOS

`createos.json`, `Dockerfile`, and `CREATEOS.md` define a production VCS deployment on
Python 3.12, port 3000, with health/readiness probes and security scanning enabled.
CreateOS auto-deploys on push after the repository is connected.

## Quality target

`scripts/quality_gate.py` requires all ten platform controls to pass. The score is a
verifiable repository gate, not a claim that unknown third-party software is perfect.

## Unified Capability Forge

The Forge consolidates the full reviewed agent, skill, MCP, memory, research, design,
marketing, browser, finance, and trading ecosystem into one governed registry rather
than bulk-installing conflicting projects.

- Registry: `governance/unified_capability_forge.json`
- Architecture: `docs/UNIFIED_CAPABILITY_FORGE.md`
- Validator: `scripts/validate_unified_capability_forge.py`
- New project-local skills: `.agents/skills/`
- Focused tests: `tests/test_unified_capability_forge.py`
- CI: `.github/workflows/unified-capability-forge.yml`

The registry preserves useful ideas from quarantined sources as non-executing patterns,
tests, schemas, or simulation fixtures. It does not install upstream dependencies,
connect wallets, place trades, bypass access controls, silently mutate shared skills,
or permit self-promotion.

The new skill pack adds ten original capabilities:

1. Constraint Drift Radar
2. Counterfactual Sandbox Designer
3. Capability Compression Cartographer
4. Provenance Entropy Auditor
5. Failure Pattern Immunizer
6. Reversible Automation Designer
7. Interface Contract Miner
8. Agent Disagreement Resolver
9. Cross-Project Opportunity Radar
10. Shadow Work Eliminator

Run the focused gate with:

```bash
python scripts/validate_unified_capability_forge.py
python -m unittest tests.test_unified_capability_forge -v
```

## Claude ↔ Codex bridge

A governed integration for `noblehacks/frenemy` lets Codex consult Claude and lets
Claude delegate to Codex without copying prompts between sessions or adding API keys.
The installer pins a reviewed full upstream commit SHA and keeps write-capable Claude
delegation approval-gated.

Windows installation:

```powershell
Set-ExecutionPolicy -Scope Process Bypass
.\tools\install-frenemy.ps1
```

Architecture, operating policy, smoke tests, and evaluated free alternatives are in
`docs/CLAUDE_CODEX_BRIDGE.md`.

## Canonical skill library

This repository is also the authoritative, version-controlled library for reusable
ChatGPT, Claude, Codex, Hermes, and compatible agent workflows.

- Skill root: `.agents/skills/`
- Registry: `governance/skill_library.json`
- Policy: `docs/SKILL_LIBRARY.md`
- Validator: `scripts/validate_skill_library.py`
- Tests: `tests/test_skill_library.py`
- CI: `.github/workflows/skill-library.yml`

The default reusable-workflow lifecycle is:

```text
implement → verify → skillize → register → review → install → runtime verify
```

Run the focused skill-library gate with:

```bash
python scripts/validate_skill_library.py
python -m unittest tests.test_skill_library -v
```

Skills cannot promote themselves, store credentials, auto-approve write-capable tools,
or claim runtime success without evidence.

## Governed skill installer

The canonical library is distributed with the open-source `vercel-labs/skills` CLI,
pinned to `skills@1.5.20` and reviewed upstream commit
`e173b8c88f2581cfdaa1b6767c6519a08155790e`.

Windows:

```powershell
Set-ExecutionPolicy -Scope Process Bypass
.\tools\install-skill-library.ps1
```

macOS or Linux:

```bash
bash tools/install-skill-library.sh
```

By default, the wrappers validate the registry and copy only `approved` skills into the
global skill directories for Codex, Claude Code, and Hermes Agent. Review-state skills
require an explicit isolated-test override. The installer selection, alternatives,
update policy, CI smoke test, and rollback commands are in `docs/SKILL_INSTALLER.md`
and `governance/skill_installers.json`.

Run the focused installer gate with:

```bash
python scripts/validate_skill_library.py
python -m unittest tests.test_skill_library tests.test_skill_installer -v
```

## Prepare Hermes for an existing local Ollama model

The tutorial [Hermes Agent, but 100% uncensored](https://www.youtube.com/watch?v=6kadyV1GkcE&t=752s) tests inference before connecting an agent to messaging. This standalone check applies that sequence to an already installed local model. It uses Python's standard library and connects directly to Ollama on IPv4 loopback. It does not start a server, download weights, use account credentials or modify a running agent.

Use the exact installed tag shown by `ollama list`. For example, on a server that already has `qwen2.5:7b`:

```sh
python tools/check_local_hermes.py --model qwen2.5:7b --write-config local-candidate.yaml
python tools/check_local_hermes.py --model qwen2.5:7b --expect-digest YOUR_64_HEX_DIGEST --smoke
python tools/check_local_hermes.py --model qwen2.5:7b --expect-digest YOUR_64_HEX_DIGEST --tool-smoke
```

Replace the digest placeholder with `model_manifest_sha256` from the first result. The first command requires an explicit cloud-disabled status from the server and matching identities in the native and OpenAI-compatible inventories. It writes model settings in JSON, which Hermes accepts as YAML. A conflicting destination is preserved. Repeat checks accept the same bytes. The two optional probes each send one fixed request. The tool probe checks the proposed function name and arguments without executing any function. A failed or ambiguous response exits nonzero without retrying.

`inventory_verified` confirms the observed manifest and route. `chat_verified` and `tool_verified` distinguish the two sampled behaviors. The manifest digest identifies Ollama's local tag manifest. Recheck it after a model or server change. The candidate selects only the main conversation route and sets an empty fallback chain. Existing profiles, plugins, auxiliary services, messaging, tools and publication permissions have their own configuration. No part of the discovery service invokes this utility. Discard the candidate file to roll back.

Upstream references: [Hermes local Ollama configuration](https://github.com/NousResearch/hermes-agent/blob/774a456f7a181c3c61ba3e5a3d93d66b1505fa8e/website/docs/guides/local-ollama-setup.md) · [Ollama API types](https://github.com/ollama/ollama/blob/d227b7e210b569e9e01c6b4b0c40748e73dcd01a/api/types.go).
