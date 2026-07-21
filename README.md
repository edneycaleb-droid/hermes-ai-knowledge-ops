# Hermes AI Knowledge Ops

A read-only research repository for tracking official Hermes Agent knowledge: source inventory, skills, tools, MCP documentation, releases, profiles, cron, plugins, and the learning loop.

## Safety boundary

This repository catalogs and analyzes discovered code and documentation. It does **not** automatically execute, install, import, or enable discovered code. All updates must retain provenance and pass security review.

## Layout

- `sources/official.yml` — allowlisted first-party sources
- `catalog/` — normalized skills, tools, MCP, plugins, profiles, cron, and learning-loop records
- `releases/` — release snapshots and change notes
- `provenance/` — source receipts and integrity metadata
- `security/` — screening policy and findings
- `.github/workflows/research-update.yml` — scheduled read-only inventory checks

## Operating principles

1. Prefer official upstream sources.
2. Record retrieval time, canonical URL, revision, and content digest.
3. Deduplicate by canonical identity and digest.
4. Never execute or install discovered code automatically.
5. Submit material changes through reviewable pull requests.
