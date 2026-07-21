# Project status

Hermes AI Knowledge Ops is an active, read-only knowledge-operations repository.

## Current scope

- Track first-party official Hermes Agent sources, releases, capabilities, tools, skills, and MCP-related material.
- Preserve canonical URLs, retrieval time, upstream revision, and content digests.
- Treat every discovered artifact as untrusted research input.
- Never install, import, execute, activate, or grant credentials to discovered code automatically.

## Validation

Run `python scripts/check_repository_quality.py`. The scheduled workflow runs the same deterministic, network-free validation. A passing score proves repository controls only; it does not prove upstream availability or runtime safety.
