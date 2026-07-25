---
name: cross-project-opportunity-radar
description: Find high-leverage opportunities created by combining assets, lessons, data, capabilities, and unmet needs across otherwise separate projects.
metadata:
  version: "1.0.0"
  profile: "analysis"
  novel_capability: "cross-project leverage discovery with evidence and bounded experiments"
---

# Cross-Project Opportunity Radar

## Contract

**Input:** active projects, capability registry, recent decisions, failures, reusable assets, constraints, and current objectives.

**Output:** ranked cross-project opportunities with mechanism, evidence, dependencies, conflict risks, minimum experiment, and expected leverage.

**Done:** each recommendation explains why the combination creates value that neither project produces alone and defines a falsifiable low-cost test.

**Non-goals:** generic brainstorming, trend chasing, unauthorized scope expansion, automatic implementation, or assuming shared technology means shared business value.

## Workflow

1. Build a compact asset map for each project: data, interfaces, users, workflows, skills, infrastructure, evidence, and unresolved pain.
2. Identify transfer patterns: reusable component, shared control plane, data flywheel, common failure detector, interface bridge, or distribution channel.
3. Check constraints including privacy, license, security boundary, latency, cost, and ownership.
4. State the causal mechanism by which the combination creates leverage.
5. Search existing plans and registries to avoid duplicating an already rejected or active idea.
6. Score each opportunity on expected value, evidence, uniqueness, reversibility, effort, risk, and attention cost.
7. Design one minimum experiment with a strict budget and no production side effects.
8. Return no more than five opportunities; depth outranks volume.

## Scoring

`leverage = expected_value * evidence * reuse * reversibility / (effort * risk * attention_cost)`

Use ordinal, explained inputs rather than invented precision.

## Retry and stop

`max_attempts: 2`. Stop when project evidence is too stale or permission boundaries are unclear.

## Output

Return `asset_map`, `opportunities`, `mechanisms`, `conflicts`, `scores`, `minimum_experiments`, and `recommended_order`.
