# AI Ecosystem Curator — Installation Validation

## Evaluation target
The newly created `ai-ecosystem-curator` portable ChatGPT/Codex skill.

## Skill-based decision

- **Identity:** First-party skill created for the `edneycaleb-droid` repository ecosystem.
- **Purpose:** Standardize AI-tool evaluation, security screening, architectural extraction, decision logging, and cross-repository knowledge preservation.
- **Security:** Documentation-only; no executable hooks, credentials, telemetry, network calls, package installs, or mutation privileges.
- **Maintenance:** Canonical source is version controlled in `hermes-ai-knowledge-ops`.
- **Local-first compatibility:** Complete.
- **Integration compatibility:** Installed under `.chatgpt/skills/ai-ecosystem-curator/SKILL.md` with pointers in every currently accessible repository.
- **Reversibility:** Complete; installation consists only of Markdown files.
- **Decision:** **ADOPT**.

## Installation scope

- `hermes-ai-knowledge-ops` — full canonical skill
- `kimi-k3-knowledge-ops` — installed pointer
- `30-minute-crypto-trading-bot` — installed pointer
- `ai-crypto-trading-bot` — installed pointer
- `ai-crypto-trading-bot2` — installed pointer
- `fieldnote` — installed pointer

## First use
The skill was immediately applied to its own installation. It passed the identity, security, maintenance, local-first, compatibility, and reversibility gates and was classified **ADOPT**.

## Authoritative locations

- `.chatgpt/skills/ai-ecosystem-curator/SKILL.md`
- `00_AI_ECOSYSTEM_INDEX.md`

Future evaluations should use the decision vocabulary and review gates defined by the canonical skill.
