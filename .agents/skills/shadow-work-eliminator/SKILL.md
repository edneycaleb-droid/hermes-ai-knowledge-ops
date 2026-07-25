---
name: shadow-work-eliminator
description: Detect repetitive hidden human effort in logs and workflows, then design bounded automation candidates that reduce toil without removing necessary judgment.
metadata:
  version: "1.0.0"
  profile: "analysis"
  novel_capability: "evidence-based human toil discovery and safe automation conversion"
---

# Shadow Work Eliminator

## Contract

**Input:** work logs, task histories, command history, tickets, calendars, recurring files, handoffs, and user-defined protected decisions.

**Output:** toil inventory, repetition evidence, judgment boundaries, automation candidates, minimum safe prototypes, and expected time recovered.

**Done:** each candidate is grounded in repeated behavior and preserves human judgment where consequences or ambiguity require it.

**Non-goals:** surveillance, automating rare tasks because they are annoying, replacing accountable decisions, or silently changing workflows.

## Workflow

1. Normalize activities without retaining secrets or unnecessary personal content.
2. Identify repeated sequences, duplicate data entry, waiting/rechecking, manual reconciliation, recurring formatting, and predictable handoffs.
3. Separate mechanical work from judgment, relationship, approval, and exception handling.
4. Quantify frequency, elapsed time, failure rate, context switching, and downstream impact using observed evidence.
5. Rank candidates by time recovered, error reduction, reversibility, implementation effort, and risk.
6. Design the smallest automation: reminder, template, prefill, validator, batch tool, draft queue, or full workflow.
7. Require preview mode, manual approval for external writes, audit receipts, and a kill switch.
8. Define adoption and abandonment metrics; retire automations that create more review work than they save.

## Privacy

Redact credentials, health information, financial account data, and private communications unless specifically required and authorized. Prefer aggregate patterns over raw content.

## Retry and stop

`max_attempts: 2`. Stop when evidence does not show meaningful repetition or the task depends primarily on human judgment.

## Output

Return `toil_inventory`, `evidence`, `judgment_boundaries`, `automation_candidates`, `minimum_prototypes`, `time_recovery_estimate`, and `retirement_metrics`.
