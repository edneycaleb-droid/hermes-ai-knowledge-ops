# Hermes Skill Library

This repository is the canonical, review-gated library for reusable ChatGPT, Claude,
Codex, Hermes, and compatible agent workflows owned by `edneycaleb-droid`.

## Canonical layout

- Skills: `.agents/skills/<skill-name>/SKILL.md`
- Registry: `governance/skill_library.json`
- Installer selection: `governance/skill_installers.json`
- Library validator: `scripts/validate_skill_library.py`
- Distribution wrappers: `tools/install-skill-library.ps1` and `tools/install-skill-library.sh`
- Tests: `tests/test_skill_library.py` and `tests/test_skill_installer.py`
- CI: `.github/workflows/skill-library.yml` and `.github/workflows/skill-installer.yml`

A skill file is not considered part of the library until it is registered. Registration
does not make it approved: lifecycle state remains independently review-gated.

## Default lifecycle

Use this workflow after substantial implementation work:

```text
implement → verify → skillize → register → review → install → runtime verify
```

1. **Implement** the requested capability on a dedicated branch.
2. **Verify** it with tests, static gates, and runtime evidence where available.
3. **Skillize** the reusable procedure, decisions, guardrails, rollback, and evidence rules.
4. **Register** the skill with version, state, capabilities, and negative contracts.
5. **Review** the code and skill together. A skill cannot approve or promote itself.
6. **Install** only registered, eligible skills with the pinned governed installer.
7. **Runtime verify** after the target agent reloads and correctly discovers the skill.

## Required skill contract

Every skill must include:

- lowercase hyphenated `name`;
- clear `description` with trigger conditions;
- semantic `metadata.version`;
- `metadata.profile`;
- `## Contract` with input, output, done condition, and non-goals;
- `## Trigger conditions`;
- bounded `## Retry and stop` behavior;
- evidence and status-reporting rules appropriate to the capability;
- explicit negative contracts in the registry.

A skill may bundle scripts, references, templates, schemas, or fixtures beneath its own
directory when required. Executable material requires focused tests and a documented
security boundary.

## Lifecycle states

- `draft`: incomplete or not yet internally coherent;
- `review`: structurally complete and awaiting evidence or human review;
- `approved`: reviewed and eligible for governed reuse and installation;
- `deprecated`: still available for compatibility but should not be selected by default;
- `retired`: preserved for provenance and rollback history but not used.

Only a human-reviewed change may promote a skill to `approved`.

## Safety rules

- Never commit passwords, tokens, cookies, API keys, private keys, or live credentials.
- Never use a floating upstream branch as executable installation truth.
- Never auto-approve write-capable tools, relays, or delegated edits.
- Never permit a skill, installer, or agent to promote itself.
- Never claim runtime verification when only static checks ran.
- Never install a discovered remote skill before provenance, security, compatibility,
  registration, and review gates pass.
- Never delete an agent's entire skill directory during rollback.
- Keep retries bounded and preserve a stop condition for missing evidence or ambiguity.

## Installer policy

The selected cross-agent installer is pinned in `governance/skill_installers.json`.
Managed wrappers must use the exact reviewed package version rather than `latest`.
They validate the library first and use copy mode by default for global installation.

The installer may distribute approved skills; it cannot change their registry state,
security policy, permissions, or runtime approval boundaries. Installation success only
proves that expected files were written. Agent discovery and correct skill invocation
require a restart and skill-specific runtime evidence.

## Versioning

Increment versions using semantic versioning:

- patch: wording, examples, or non-behavioral corrections;
- minor: backward-compatible workflow or capability additions;
- major: changed authority, safety boundary, required inputs, outputs, or behavior.

Registry and frontmatter versions must match exactly.

## Validation

Run:

```bash
python scripts/validate_skill_library.py
python -m unittest tests.test_skill_library tests.test_skill_installer -v
```

The validator rejects missing files, duplicate names or paths, invalid semantic versions,
unregistered states, missing required sections, empty capabilities, and empty negative
contracts. The installer smoke test writes registered skills only into isolated temporary
agent homes and verifies exact `SKILL.md` copies.

## Reuse and installation

The library is the persistent source of truth. ChatGPT itself does not gain a mutable
private internal skill store from this repository; instead, connected agents and future
sessions retrieve or install these version-controlled skills from the repository.

Install the approved library with:

```powershell
.\tools\install-skill-library.ps1
```

or:

```bash
bash tools/install-skill-library.sh
```

After installation, restart the target agent and verify it discovers the requested skill
before reporting `RUNTIME_VERIFIED`.

## Removing a skill

Do not immediately delete an approved skill. Mark it `deprecated`, name the replacement,
and provide a migration path. Remove only the named installed skill from target agents;
do not delete an entire agent skill directory. Delete the canonical source only after
dependents have migrated and the registry records retirement.
