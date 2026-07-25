---
name: interface-contract-miner
description: Recover implicit API, CLI, data, timing, and human-workflow contracts from code, tests, logs, examples, and production evidence before refactors or integrations.
metadata:
  version: "1.0.0"
  profile: "engineering"
  novel_capability: "implicit contract recovery from heterogeneous evidence"
---

# Interface Contract Miner

## Contract

**Input:** target interface and available code, tests, schemas, documentation, traces, logs, examples, and consumers.

**Output:** explicit contract model, confidence per clause, observed exceptions, compatibility tests, and migration hazards.

**Done:** externally observable behavior is separated from implementation detail and backed by evidence.

**Non-goals:** treating undocumented quirks as permanent without impact analysis, inventing guarantees, or changing the interface.

## Workflow

1. Identify producers, consumers, owners, and trust boundaries.
2. Extract syntax contracts: fields, types, commands, exit codes, status codes, headers, filenames, and protocols.
3. Extract semantic contracts: ordering, units, defaults, idempotency, pagination, retries, timeouts, null behavior, and error meaning.
4. Extract temporal contracts: event cadence, freshness, sequence, concurrency, locking, and eventual-consistency assumptions.
5. Compare documentation, tests, and observed traces; record disagreements rather than averaging them.
6. Mark each clause `specified`, `tested`, `observed`, `inferred`, or `disputed`.
7. Generate compatibility tests for high-impact clauses and negative tests for forbidden behavior.
8. Produce migration hazards and a versioning recommendation.

## Evidence priority

Explicit accepted specification outranks examples. Fresh production evidence can reveal undocumented behavior but does not automatically make that behavior desirable.

## Retry and stop

`max_attempts: 2`. Stop when consumer evidence is missing for a claimed compatibility guarantee.

## Output

Return `contract`, `clause_confidence`, `exceptions`, `compatibility_tests`, `migration_hazards`, and `versioning_recommendation`.
