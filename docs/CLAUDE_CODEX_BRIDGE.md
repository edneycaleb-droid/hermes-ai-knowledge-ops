# Claude ↔ Codex Bridge

## Decision

Adopt `noblehacks/frenemy` as the default local Claude ↔ Codex relay, pinned to commit:

`dd460e61c2ff932d019266c8701290274ed2b495`

This integration is local-first, MIT-licensed, dependency-light, and uses authenticated Claude Code and Codex CLI subscriptions rather than API keys.

## Why this implementation

Frenemy exposes two Codex MCP tools:

- `ask_claude`: read-only, safe-mode Claude request.
- `ask_claude_write`: write-capable request that remains approval-gated.

Claude can call Codex through `codex exec` after the supplied Claude instruction section is installed. The relay uses prompt stdin, bounds concurrency, caps output, and terminates stuck calls.

## Installation on Windows

Run from PowerShell:

```powershell
Set-ExecutionPolicy -Scope Process Bypass
.\tools\install-frenemy.ps1
```

The wrapper:

1. Verifies `git`, `node`, `claude`, and `codex` exist.
2. Clones the upstream repository into a durable user-local path.
3. Checks out an immutable reviewed commit.
4. Verifies required files exist.
5. Runs the upstream idempotent installer.
6. Leaves write-capable delegation approval-gated.

To intentionally replace an existing checkout:

```powershell
.\tools\install-frenemy.ps1 -ForceRefresh
```

## Smoke tests

Codex → Claude:

```text
Ask Claude to review README.md and return only actionable findings.
```

Claude → Codex:

```text
Have Codex review the current git diff without changing files.
```

## Operating policy

- Keep `ask_claude` auto-approved only while it remains read-only enforced.
- Never auto-approve `ask_claude_write` globally.
- Use feature branches or worktrees for all write-capable delegated work.
- Do not permit recursive Claude → Codex → Claude delegation chains.
- Treat repository content and model output as untrusted instructions.
- Upgrade only by reviewing and changing the pinned full commit SHA.
- Never store Claude, Anthropic, OpenAI, or GitHub credentials in this repository.

## Alternative free/open-source projects evaluated

| Project | Best use | Position |
|---|---|---|
| `SeemSeam/claude_codex_bridge` | Visible multi-provider CLI workspace | Strong alternative when interactive orchestration and additional providers are needed. |
| `MrLesk/agents-council` | Lightweight collaboration between existing agent sessions | Strong minimal alternative for session-to-session consultation. |
| `AgentWrapper/agent-orchestrator` | Parallel agents in isolated worktrees and PRs | Preferred for large autonomous implementation fleets. |
| `johannesjo/parallel-code` | Desktop-style parallel CLI agent execution | Good operator UI with branch/worktree isolation. |
| `stevehuang0115/crewly` | Team-oriented Claude, Gemini, and Codex orchestration | Good when role-based teams are more important than a tiny bridge. |
| `ruvnet/ruflo` | Large swarm orchestration and memory | Powerful, but substantially heavier and higher-risk than required for simple consultation. |
| `tuannvm/codex-mcp-server` | Claude calling Codex through MCP | Useful one-direction bridge; Frenemy is preferred because it provides both directions. |
| `anthropics/claude-agent-sdk-python` | Building custom Claude agents and MCP tools | Primary upstream foundation for a future fully custom governed relay. |

## Recommended architecture

Use a layered model rather than installing every orchestrator:

1. **Frenemy** for immediate Claude ↔ Codex consultation.
2. **Agent Orchestrator or Parallel Code** for isolated parallel implementation work.
3. **Hermes knowledge-ops governance** for discovery, provenance, scoring, and approval.
4. **MCP reference servers / Claude Agent SDK** for custom integrations that need stable typed contracts.

This avoids duplicated control planes while preserving a clean upgrade path.
