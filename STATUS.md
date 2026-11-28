# Project status

Hermes AI Knowledge Ops is an active, read-only knowledge-operations repository.

## Current scope

- Track first-party official Hermes Agent sources, releases, capabilities, tools, skills, and MCP-related material.
- Preserve canonical URLs, retrieval time, upstream revision, and content digests.
- Treat every discovered artifact as untrusted research input.
- Never install, import, execute, activate, or grant credentials to discovered code automatically.

## Validation

Run `python scripts/check_repository_quality.py`. The Agent platform quality workflow runs the same deterministic check on pull requests and pushes to main. A passing score covers the repository controls examined by the script.
