---
name: counterfactual-sandbox-designer
description: Design a reversible simulation that tests a risky automation or architecture against realistic counterfactuals before any production execution.
metadata:
  version: "1.0.0"
  profile: "high-risk"
  novel_capability: "counterfactual simulation planning with side-effect prediction"
---

# Counterfactual Sandbox Designer

## Contract

**Input:** proposed change, expected behavior, real interfaces, risk boundaries, and available historical or synthetic data.

**Output:** an isolated simulation plan, synthetic scenarios, predicted side effects, acceptance checks, and a promotion recommendation.

**Done:** the simulation can falsify the proposal without production credentials or irreversible writes.

**Non-goals:** executing against production, copying live secrets, claiming simulated success proves live safety, or weakening the real gate.

## Workflow

1. Enumerate every external effect: filesystem writes, network calls, messages, deployments, purchases, trades, credentials, and data mutation.
2. Replace each effect with a recording stub or disposable service.
3. Construct a simulation twin whose interfaces match production but whose outputs are deterministic and inspectable.
4. Generate at least five counterfactuals: expected success, stale input, partial outage, malicious input, and rollback after partial completion.
5. Add domain-specific extremes such as rate limits, duplicate events, clock skew, race conditions, low liquidity, or malformed schemas.
6. Define acceptance thresholds before running the twin.
7. Produce a side-effect ledger comparing intended, predicted, observed, and prohibited effects.
8. Recommend `PROMOTE`, `REVISE`, or `BLOCK`; promotion still requires separate human approval.

## Safety controls

- Use synthetic or redacted data.
- Bind services to loopback where possible.
- Deny unknown outbound hosts.
- Use zero-value or paper-only financial fixtures.
- Make cleanup idempotent and verify it.

## Retry and stop

`max_attempts: 3`. Every retry must change a hypothesis, fixture, or implementation. Stop on the same failure signature twice.

## Output

Return `twin_architecture`, `counterfactual_matrix`, `side_effect_ledger`, `evidence`, `residual_risk`, and `promotion_recommendation`.
