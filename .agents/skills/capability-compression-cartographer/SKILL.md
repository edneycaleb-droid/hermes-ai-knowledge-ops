---
name: capability-compression-cartographer
description: Map overlapping agents, skills, tools, MCP servers, and workflows into the smallest coherent capability set without losing required behavior.
metadata:
  version: "1.0.0"
  profile: "analysis"
  novel_capability: "behavior-level capability compression"
---

# Capability Compression Cartographer

## Contract

**Input:** capability manifests, skill descriptions, tool schemas, usage traces, and project requirements.

**Output:** a behavior map, duplicate clusters, canonical owners, retained differentiators, deprecation candidates, and migration plan.

**Done:** every required behavior has exactly one canonical owner or an explicit justified exception.

**Non-goals:** choosing by popularity alone, deleting unique safety controls, merging incompatible trust boundaries, or installing replacements.

## Workflow

1. Normalize each capability into triggers, inputs, outputs, permissions, dependencies, side effects, state, and failure behavior.
2. Compute a Capability DNA record and compare exact, near, and partial overlaps.
3. Cluster by observable behavior rather than repository name or marketing category.
4. Select a canonical owner using authority, maintenance, evidence, license, context cost, reversibility, and operational fit.
5. Preserve unique ideas as adapters, tests, policies, or optional profiles instead of duplicate global skills.
6. Identify trigger collisions and contradictory instructions.
7. Produce a migration sequence with compatibility shims, rollback, and a measurable context-reduction estimate.

## Selection rules

- Official or primary sources outrank repackaged catalogs.
- Native platform support outranks compatibility wrappers when functionality is equivalent.
- A safer capability may outrank a richer but less governable one.
- Domain-specific capabilities remain project-local.

## Retry and stop

`max_attempts: 2`. Stop if manifests are too incomplete to compare; return required evidence rather than guessing.

## Output

Return `capability_dna`, `clusters`, `canonical_map`, `retained_differentiators`, `deprecations`, `migration_plan`, and `estimated_context_savings`.
