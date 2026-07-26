# Skills Index

This is the canonical skill registry for the repositories owned by `edneycaleb-droid`.

## Official installer

Use OpenAI's official `skill-installer` from `openai/skills`.

- Source: `https://github.com/openai/skills/tree/main/skills/.system/skill-installer`
- Type: Codex system skill
- Default target: `$CODEX_HOME/skills` (normally `~/.codex/skills`)
- Supported sources: OpenAI curated skills or a GitHub repository path
- Safety behavior: validates relative paths, requires `SKILL.md`, prevents overwrite of an existing destination, and uses safe ZIP extraction or sparse Git checkout.

Example installation command from a Codex environment:

```bash
$skill-installer install https://github.com/edneycaleb-droid/hermes-ai-knowledge-ops/tree/main/.chatgpt/skills/ai-ecosystem-curator
```

Equivalent helper-script command when the official system skill scripts are available:

```bash
python "$CODEX_HOME/skills/.system/skill-installer/scripts/install-skill-from-github.py" \
  --repo edneycaleb-droid/hermes-ai-knowledge-ops \
  --path .chatgpt/skills/ai-ecosystem-curator
```

Restart Codex after installing a new personal skill.

## Installed repository skills

### AI Ecosystem Curator

- Canonical ChatGPT/Agent Skill: `.chatgpt/skills/ai-ecosystem-curator/SKILL.md`
- Repository Codex copy: `.codex/skills/ai-ecosystem-curator/SKILL.md`
- Canonical knowledge registry: `00_AI_ECOSYSTEM_INDEX.md`
- Decision: **ADOPT**
- Use for evaluating, screening, classifying, integrating, and documenting AI tools, models, repositories, MCP servers, research feeds, and agent frameworks.

## Installation policy

1. Prefer official or verified sources.
2. Inspect every `SKILL.md`, script, reference, executable, and dependency before installation.
3. Preserve the upstream license and attribution.
4. Do not install skills that request secrets, unrestricted shell access, browser sessions, production credentials, or destructive writes without a sandbox review.
5. Install to an isolated destination first and validate the trigger description, required files, and behavior.
6. Record the source repository, path, commit or blob SHA, license, installation date, and decision in this index.
7. Keep one canonical skill copy and use controlled synchronization to prevent silent drift.

## ChatGPT account note

ChatGPT workspace Skills are installed through **Plugins → Skills** when the account and workspace support Personal Skills. Repository and Codex skill files do not automatically become installed ChatGPT workspace Skills; they remain portable Agent Skills until uploaded or installed through the supported ChatGPT interface.
