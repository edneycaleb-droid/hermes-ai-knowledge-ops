---
name: provenance-entropy-auditor
description: Measure how knowledge loses authority through stale evidence, citation distance, repeated summarization, source disagreement, and unverified transformations.
metadata:
  version: "1.0.0"
  profile: "analysis"
  novel_capability: "evidence half-life and provenance entropy scoring"
---

# Provenance Entropy Auditor

## Contract

**Input:** claims, source graph, timestamps, transformations, and domain volatility.

**Output:** claim-level authority scores, evidence half-life, entropy causes, expired claims, and prioritized re-verification tasks.

**Done:** every material claim is classified as current, decaying, stale, disputed, or unsupported with traceable reasoning.

**Non-goals:** treating citation count as truth, deleting old evidence, inventing source dates, or refreshing low-value facts indiscriminately.

## Workflow

1. Trace each claim to the nearest primary or authoritative source.
2. Count transformation hops: extraction, paraphrase, synthesis, translation, aggregation, and model-generated inference.
3. Assign domain volatility: static, slow, moderate, fast, or real-time.
4. Calculate an evidence half-life from volatility, source authority, observation date, and known update cadence.
5. Increase entropy for missing locators, circular citations, mediated summaries, unresolved disagreement, or transformations without receipts.
6. Decrease entropy for independent confirmation, deterministic reproduction, signed artifacts, and fresh direct checks.
7. Produce the smallest verification queue ordered by consequence multiplied by uncertainty.
8. Preserve superseded claims with validity intervals rather than erasing history.

## Decision labels

- `CURRENT`: direct evidence remains within its authority window.
- `DECAYING`: usable with an as-of qualification.
- `STALE`: must not support a present-tense claim.
- `DISPUTED`: authoritative sources conflict.
- `UNSUPPORTED`: no adequate evidence chain.

## Retry and stop

`max_attempts: 2`. Stop when source identity or dates cannot be established.

## Output

Return `claim_scores`, `half_lives`, `entropy_drivers`, `expired_claims`, `verification_queue`, and `allowed_wording`.
