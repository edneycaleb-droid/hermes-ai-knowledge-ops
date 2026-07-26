# Hermes Skill Library

This repository is the canonical, version-controlled skill library for reusable ChatGPT, Claude, Codex, Hermes, and compatible agent workflows owned by `edneycaleb-droid`.

## Canonical locations

- Skill definitions: `.agents/skills/<skill-name>/SKILL.md`
- Machine-readable registry: `governance/skill_library.json`
- Validation: `scripts/validate_skill_library.py`
- Regression tests: `tests/test_skill_library.py`

A skill is not considered part of the library merely because a Markdown file exists. It must be registered, validated, reviewed, and associated with evidence.

## Standard lifecycle

1. **Draft** — the workflow is captured but may be incomplete.
2. **Review** — static validation passes and a pull request is open.
3. **Approved** — the skill has been reviewed and merged.
4. **Deprecated** — a replacement exists or the workflow is no longer preferred.
5. **Retired** — the skill must no longer be selected for new work.

Skills cannot promote themselves. Lifecycle changes require a reviewed repository change.

## Required skill contract

Every skill must include YAML frontmatter with:

- `name`
- `description`
- `metadata.version`
- `metadata.profile`

Every skill body must define:

- Contract: input, output, done condition, and non-goals
- Trigger conditions
- Bounded workflow
- Evidence rules
- Safety and negative contracts
- Tests or validation expectations
- Retry and stop conditions
- Rollback when the skill can change files, configuration, services, or external state

## Default implementation workflow

For substantial repository work:

1. Inspect the target repository, current branch, issue, and pull request state.
2. Establish authoritative requirements and immutable safety constraints.
3. Implement the smallest coherent change set on a dedicated branch.
4. Add or strengthen tests, documentation, rollback, and verification evidence.
5. Open or update a reviewable pull request.
6. After the implementation is complete, extract the reusable process into a new or updated skill.
7. Add the skill to `.agents/skills/` and register it in `governance/skill_library.json`.
8. Run the skill-library validator and focused tests.
9. Report exact paths, versions, commits, pull requests, evidence, and remaining runtime verification.

This "implement → verify → skillize → register" sequence is the repository default for reusable workflows.

## Governance rules

- Never commit passwords, tokens, cookies, API keys, private keys, or session material.
- Never treat a floating upstream branch as an executable source of truth; pin reviewed full commit SHAs.
- Never auto-approve write-capable tools or agents by default.
- Never claim a runtime integration works based only on static inspection.
- Never install or execute discovered third-party software during discovery.
- Never create recursive agent delegation without explicit depth and cycle controls.
- Prefer one canonical skill over several overlapping variants.
- Preserve source provenance and distinguish confirmed, statically verified, and runtime-pending claims.

## Adding a skill

Create:

```text
.agents/skills/<skill-name>/SKILL.md
```

Then add one registry entry containing at least:

- `name`
- `path`
- `version`
- `state`
- `profile`
- `capabilities`
- `negative_contracts`

Run:

```bash
python scripts/validate_skill_library.py
python -m unittest tests.test_skill_library -v
```

## Updating a skill

- Increment its semantic version when behavior or contract changes.
- Update the corresponding registry version in the same pull request.
- Preserve compatibility notes or migration steps when replacing prior behavior.
- Add regression coverage for every corrected failure or newly enforced constraint.

## Removing a skill

Do not immediately delete an approved skill. Mark it `deprecated`, name the replacement, and provide a migration path. Delete only after dependents have migrated and the registry records retirement.
