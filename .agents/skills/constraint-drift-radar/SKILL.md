---
name: constraint-drift-radar
description: Detect contradictions, silent requirement changes, and policy drift across prompts, plans, docs, code, tests, issues, and agent memory before implementation or release.
metadata:
  version: "1.0.0"
  profile: "review"
  novel_capability: "cross-artifact temporal constraint reconciliation"
---

# Constraint Drift Radar

## Contract

**Input:** task scope, authoritative sources, candidate artifacts, and relevant timestamps.

**Output:** a drift ledger with canonical constraints, conflicting statements, likely supersessions, unresolved ambiguity, affected files, and safe next actions.

**Done:** every material conflict has provenance and is either resolved by authority/recency rules or marked for human decision.

**Non-goals:** silently choosing business intent, rewriting policy, treating newer text as automatically authoritative, or broadening scope.

## Workflow

1. Identify the authority hierarchy for this task: runtime evidence, current policy, accepted specification, tests, implementation, historical notes.
2. Extract falsifiable constraints into normalized records: subject, rule, polarity, scope, source, date, confidence.
3. Compare records for direct contradiction, scope mismatch, stale values, renamed concepts, and implicit behavior changes.
4. Build a temporal chain showing when each constraint appeared and what it replaced.
5. Resolve only when authority and scope are unambiguous. Otherwise return `DECISION_REQUIRED` with the smallest discriminating question.
6. Produce an impact map listing code, tests, docs, automation, memory, and external integrations affected by each drift.
7. Recommend the smallest coherent patch set; do not edit unless separately authorized.

## Evidence rules

- Quote only short exact fragments and preserve source paths or URLs.
- Runtime evidence can disprove documentation, but one transient failure does not redefine policy.
- A passing test proves only its asserted scope.
- Historical memory never overrides current explicit instruction.

## Retry and stop

`max_attempts: 2`. Retry only after changing source coverage or normalization. Stop on repeated ambiguity or missing authority.

## Output

Return `status`, `canonical_constraints`, `drift_events`, `unresolved_conflicts`, `impact_map`, `evidence`, and `next_action`.
