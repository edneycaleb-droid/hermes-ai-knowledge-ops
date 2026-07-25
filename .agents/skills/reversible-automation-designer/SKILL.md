---
name: reversible-automation-designer
description: Design automations with dry-run behavior, rollback, kill switches, idempotency, blast-radius limits, and compensation before enabling side effects.
metadata:
  version: "1.0.0"
  profile: "high-risk"
  novel_capability: "reversibility-first automation design"
---

# Reversible Automation Designer

## Contract

**Input:** intended automation, trigger, side effects, data stores, permissions, and failure tolerance.

**Output:** reversible architecture, dry-run contract, idempotency keys, compensation steps, kill switch, blast-radius limits, and reversibility score.

**Done:** every side effect is prevented, recorded, reversed, or explicitly classified as irreversible before enablement.

**Non-goals:** enabling the automation, disguising irreversible actions as compensatable, or accepting backups that have not been restored in a test.

## Workflow

1. Enumerate triggers, reads, writes, external notifications, spending, deployments, and deletions.
2. Classify each action as naturally reversible, compensatable, restorable, or irreversible.
3. Add preview mode that produces the exact proposed changes without performing them.
4. Define idempotency keys and duplicate-event handling.
5. Limit batch size, concurrency, affected accounts, paths, hosts, and maximum spend.
6. Add a tested kill switch independent of the primary scheduler.
7. Design compensation in reverse dependency order and record partial rollback states.
8. Test recovery from interruption after every material step.
9. Calculate a reversibility score from restoration coverage, external effects, evidence, and time-to-recover.
10. Route low-scoring designs to stricter human approval.

## Mandatory controls

- Default disabled.
- Least privilege.
- Audit receipt per run.
- No secret values in logs.
- No live trading, payment, publication, or credential mutation without explicit approval.

## Retry and stop

`max_attempts: 2`. Stop if any consequential action lacks a viable rollback or accepted irreversible-action policy.

## Output

Return `action_inventory`, `dry_run_contract`, `idempotency_plan`, `kill_switch`, `rollback_graph`, `blast_radius`, `reversibility_score`, and `approval_required`.
