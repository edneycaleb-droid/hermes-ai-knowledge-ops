# Unified Capability Forge

The Unified Capability Forge converts broad GitHub discovery into a minimal, governed set of capabilities that can be safely evaluated, adapted, and promoted.

## Why this exists

The reviewed ecosystem contains excellent ideas, but installing every repository would create duplicate triggers, contradictory methodologies, uncontrolled context growth, licensing ambiguity, hidden network dependencies, and unsafe execution paths. The Forge preserves useful ideas without importing unsafe defaults.

## Operating model

```text
Discover broadly
    -> normalize source and license
    -> compute Capability DNA
    -> identify duplicates and conflicts
    -> extract safe design patterns
    -> generate disabled adapter or draft skill
    -> run static and behavioral checks
    -> execute only in a disposable simulation twin
    -> collect proof receipts
    -> independent review
    -> human promotion
    -> project-local enablement
```

## Canonical control planes

- **Ferro Gateway** routes model inference. OpenRouter stays disabled unless explicitly approved.
- **callmux** routes MCP tools and external capabilities.
- **Loopy** defines finite iteration, budgets, and stopping behavior.
- **Repo Task Proof Loop** preserves coding evidence and independent verification.
- **AI2 Tango** provides cached, reproducible research steps.
- **OpenViking** indexes agent and project context.
- **PrivateGPT** owns citation-backed document and structured-data RAG.
- **Ar9av Obsidian Wiki** owns canonical human-readable knowledge.
- **Third Brain governance contracts** control provenance and semantic promotion.
- **Minions and Oh My Hermes** supervise bounded Hermes work.

No component may silently replace another component's canonical data.

## Quarantine salvage rules

A quarantined source may still contribute:

1. An algorithmic idea rewritten from first principles.
2. A schema or checklist with attribution.
3. A non-executing metadata adapter.
4. A test fixture or synthetic benchmark.
5. A safety control derived from a discovered failure mode.

It may not contribute:

- executable dependencies,
- lifecycle scripts,
- credentials,
- auto-install commands,
- wallet or brokerage access,
- CAPTCHA or anti-detection bypasses,
- unrestricted background loops,
- silent skill mutation,
- self-promotion,
- external writes without approval.

## Promotion contract

A capability advances through:

`discovered -> screened -> quarantined -> sandboxed -> verified -> candidate -> approved -> enabled`

Any state can transition to `retired` or `blocked`. Promotion requires:

- immutable source revision,
- license decision,
- Capability DNA record,
- negative capability contract,
- least-privilege permissions,
- network allowlist,
- simulation evidence,
- deterministic tests where feasible,
- rollback plan,
- fresh independent review,
- human approval.

## Ten new system ideas

The canonical definitions live in `governance/unified_capability_forge.json`.

1. **Capability DNA Hash** — behavioral deduplication beyond repository names.
2. **Safety Budget Market** — agents trade scope for privilege inside hard limits.
3. **Skill Greenhouse** — synthetic incubation before promotion.
4. **Negative Capability Registry** — explicit forbidden behaviors used during routing.
5. **Simulation Twin** — shadow execution with predicted side effects.
6. **Evidence Half-Life** — authority decays as evidence becomes stale.
7. **Agent Immune System** — failures become detectors and regression tests.
8. **Context Branch Predictor** — load only likely-needed context and measure misses.
9. **Reversibility Score** — stricter review for low-rollback actions.
10. **Human Attention Allocator** — rank approvals by decision leverage and avoided harm.

## New skill pack

Ten project-local skills are stored under `.agents/skills/`. They are intentionally distinct from the reviewed repositories and are designed to connect the existing stack rather than duplicate it.

## Trading boundary

Trading repositories and financial skills are research inputs only in this repository. They cannot place orders, read private keys, access wallets, alter live Freqtrade configuration, or bypass the Risk Governor. Any future execution adapter must be implemented in the trading repository through a separate reviewed pull request and paper-trading gate.
