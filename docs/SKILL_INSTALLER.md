# Governed Skill Installer

This repository uses the open-source [`skills`](https://github.com/vercel-labs/skills) CLI as its primary cross-agent skill installer.

## Selection

The reviewed installer is pinned to:

- npm package: `skills`
- package version: `1.5.20`
- upstream repository: `vercel-labs/skills`
- reviewed upstream commit: `e173b8c88f2581cfdaa1b6767c6519a08155790e`
- license: MIT
- minimum Node.js version: `22.20.0`

The pin prevents a future package release from silently changing installation behavior. Updating the pin requires a new source review, test update, and pull request.

## Why this installer

The CLI directly discovers `.agents/skills/`, supports local and remote sources, offers non-interactive installation, and targets Codex, Claude Code, Hermes Agent, and many other coding agents. It also supports listing, finding, updating, removing, initializing, and temporarily using skills.

The official Codex `$skill-installer` remains the preferred native fallback for Codex-only curated or GitHub-path installation. OpenSkills remains a valid reference implementation. They are not layered on top of the selected installer by default because overlapping installers can create duplicate or divergent copies.

## Install the canonical library

Run from the repository root.

### Windows PowerShell

```powershell
Set-ExecutionPolicy -Scope Process Bypass
.\tools\install-skill-library.ps1
```

### macOS or Linux

```bash
bash tools/install-skill-library.sh
```

The default operation:

1. checks for Node.js, `npx`, and Python 3;
2. requires Node.js `22.20.0` or newer;
3. runs `scripts/validate_skill_library.py`;
4. selects only skills in the `approved` lifecycle state;
5. uses `npx --yes skills@1.5.20`;
6. installs eligible skills globally for `codex`, `claude-code`, and `hermes-agent`;
7. copies files rather than creating fragile global symlinks;
8. lists the resulting installations;
9. instructs the operator to restart each agent.

If no skills are approved, the wrapper exits without installing anything. Review-state skills require an explicit override and are intended only for isolated CI or deliberate pre-merge testing.

Expected global destinations are:

- Codex: `~/.codex/skills/`
- Claude Code: `~/.claude/skills/`
- Hermes Agent: `~/.hermes/skills/`

## Install a specific approved skill

PowerShell:

```powershell
.\tools\install-skill-library.ps1 -Skill claude-codex-frenemy-bridge
```

Shell:

```bash
bash tools/install-skill-library.sh --skill claude-codex-frenemy-bridge
```

For isolated testing of a review-state skill:

```powershell
.\tools\install-skill-library.ps1 -AllowReview -Skill governed-skill-installer
```

```bash
bash tools/install-skill-library.sh --allow-review --skill governed-skill-installer
```

Do not use the review override as a permanent workstation default.

Install into project-local directories instead of global directories:

```powershell
.\tools\install-skill-library.ps1 -Scope Project
```

```bash
bash tools/install-skill-library.sh --project
```

Target a subset of agents:

```powershell
.\tools\install-skill-library.ps1 -Agent codex,claude-code
```

```bash
bash tools/install-skill-library.sh --agent codex --agent claude-code
```

## Direct CLI usage

List the skills discoverable in this checkout without installing:

```bash
npx --yes skills@1.5.20 add . --list
```

Direct CLI installation bypasses the repository lifecycle selector. Use it only after independently confirming that the registry state is `approved`.

```bash
python scripts/select_installable_skills.py --state approved --skill claude-codex-frenemy-bridge
npx --yes skills@1.5.20 add . --skill claude-codex-frenemy-bridge --agent codex --global --copy --yes
```

Use a skill temporarily without installing it only after the same eligibility check:

```bash
python scripts/select_installable_skills.py --state approved --skill claude-codex-frenemy-bridge
npx --yes skills@1.5.20 use . --skill claude-codex-frenemy-bridge
```

## Verification

Run the static and installation gates:

```bash
python scripts/validate_skill_library.py
python -m unittest tests.test_skill_library tests.test_skill_installer -v
```

The CI smoke test explicitly permits the two review-state skills, installs them into an isolated temporary home directory, and verifies that each target agent receives a `SKILL.md` copy. That override is visible in the workflow and cannot silently affect normal installation.

Runtime installation on an operator workstation is confirmed only when the installer exits successfully and the expected skill files exist. Restart the target agent before claiming the skill is active.

## Updates

Do not run an unpinned `npx skills` or `npx skills@latest` command in managed automation.

To update:

1. identify the desired release and its full upstream commit SHA;
2. inspect the release diff, package metadata, supported-agent paths, install behavior, and dependency changes;
3. update both wrappers and `governance/skill_installers.json`;
4. update static tests;
5. run the isolated installation smoke test;
6. submit the change for review.

`skills update` is useful for ordinary user-managed installations, but this repository's governed distribution remains version-pinned and review-gated.

## Rollback

Remove a skill with the same pinned CLI:

```bash
npx --yes skills@1.5.20 remove claude-codex-frenemy-bridge --agent codex --agent claude-code --agent hermes-agent --global --yes
```

Rollback must remove only the named skills. Do not delete an agent's entire skill directory or overwrite unrelated configuration.

## Security boundary

- No credentials are accepted or written by the wrapper.
- The local library must validate before installation.
- Normal installation permits only `approved` skills.
- Review-state installation requires an explicit visible override.
- Installation does not approve write-capable tools or agent actions.
- Remote skills must first pass the repository's discovery, provenance, security, compatibility, registration, and review process.
- No installer or installed skill may self-promote into an approved lifecycle state.
- Installation success is not evidence that a skill's downstream runtime integration works; those smoke tests remain skill-specific.
