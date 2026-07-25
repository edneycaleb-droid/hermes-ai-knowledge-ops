---
name: agent-disagreement-resolver
description: Resolve conflicting agent recommendations by comparing evidence, assumptions, failure costs, and falsifiable predictions without forcing artificial consensus.
metadata:
  version: "1.0.0"
  profile: "review"
  novel_capability: "evidence-weighted multi-agent disagreement resolution"
---

# Agent Disagreement Resolver

## Contract

**Input:** competing recommendations, supporting evidence, task constraints, and decision consequences.

**Output:** disagreement map, shared facts, divergent assumptions, evidence quality, falsification tests, and a decision or explicit unresolved state.

**Done:** the selected action is justified by evidence and risk, or the disagreement is narrowed to a concrete experiment or human decision.

**Non-goals:** majority voting, averaging incompatible answers, rewarding confidence, or allowing an agent to review its own unverifiable claim.

## Workflow

1. Rewrite each recommendation as a falsifiable proposal.
2. Separate shared facts from assumptions, preferences, predictions, and unknowns.
3. Score evidence by authority, freshness, directness, reproducibility, and independence.
4. Identify whether disagreement is factual, causal, value-based, scope-based, or risk-tolerance-based.
5. Ask each proposal for its strongest failure mode and the observation that would disprove it.
6. Prefer reversible experiments when evidence is insufficient.
7. Apply asymmetric-loss analysis: estimate harm from choosing each option when it is wrong.
8. Decide only when one option dominates on evidence and risk; otherwise return `UNRESOLVED` with the smallest decisive test.

## Independence

Use a fresh reviewer or deterministic check for material decisions. Same-family or shared-context reviews must be labeled as non-independent.

## Retry and stop

`max_rounds: 2`. No endless debate. Stop when no new evidence or discriminating test is produced.

## Output

Return `shared_facts`, `assumption_matrix`, `evidence_scores`, `failure_modes`, `decision`, `confidence_bounds`, and `next_test`.
