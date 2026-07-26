---
name: ai-ecosystem-curator
description: Evaluate AI tools, repositories, models, MCP servers, agent frameworks, research feeds, and infrastructure; preserve useful findings; classify adoption risk; and keep decisions easy to find across repositories. Use whenever the user shares AI-related URLs, asks whether a component belongs in the ecosystem, requests cross-repository implementation, or wants prior AI research organized for future agents.
metadata:
  short-description: Curate, verify, classify, and preserve AI ecosystem decisions
---

# AI Ecosystem Curator

## Purpose
Evaluate AI tools, repositories, models, MCP servers, agent frameworks, research feeds, and infrastructure; preserve the useful findings; and route each candidate into the correct adoption path without polluting production systems.

## When to use
Use this skill whenever the user shares one or more AI-related URLs, asks whether a tool belongs in the ecosystem, requests cross-repository implementation, or wants prior research organized for future agents.

## Operating principles
1. Verify current facts from authoritative sources before making time-sensitive claims.
2. Prefer official repositories, official documentation, primary papers, and reproducible evidence.
3. Treat curated lists as discovery feeds, not trust anchors.
4. Prefer local-first, open-source, auditable, and provider-agnostic components.
5. Separate architecture worth copying from software worth installing.
6. Never install unverified executables, browser agents, proxy clients, or credential-handling tools outside a disposable sandbox.
7. Preserve one canonical knowledge source and link other repositories to it.
8. Keep findings easy to locate using root-level `00_` index files.

## Decision vocabulary
Classify every candidate as exactly one primary decision:

- **ADOPT** — ready for controlled integration.
- **PILOT** — promising, but requires benchmarked trial.
- **WATCH** — strategically useful later or dependent on future scale.
- **REFERENCE** — architecture, research, or educational value only.
- **QUARANTINE** — potentially useful but high-risk or insufficiently verified.
- **REJECT** — unrelated, obsolete, misleading, redundant, or unacceptable risk.

## Evaluation rubric
Score each candidate across:

- Practical capability: 25%
- Security and isolation: 20%
- Maintenance health: 15%
- Local-first compatibility: 15%
- Integration compatibility: 10%
- Cost efficiency: 10%
- Documentation quality: 5%

Automatic adoption requires:

- Total score at least 85/100
- Security score at least 80/100
- No critical red flags
- Approved license
- Sandbox tests passed
- No superior existing component

## Mandatory review gates

### 1. Identity
Resolve the official owner, repository, homepage, package, paper, and release channel. Flag brand impersonation and unofficial forks.

### 2. Maintenance
Check archived status, recent commits, releases, issue activity, contributor depth, dependency health, and reproducible builds.

### 3. Security
Inspect install scripts, post-install hooks, network destinations, telemetry, secret handling, browser/session access, shell permissions, filesystem scope, update mechanism, signing, checksums, and CVEs.

### 4. Cost and lock-in
Classify as free open source, open core, free tier, paid API, paid subscription, or unclear. Identify provider lock-in and hidden infrastructure requirements.

### 5. Sandbox validation
Use a disposable VM, container, worktree, Windows Sandbox, or isolated user profile. Never expose real credentials, production repositories, personal browser sessions, DoD data, or financial secrets during evaluation.

### 6. Architectural fit
Determine whether the candidate replaces, complements, duplicates, or conflicts with existing components.

## Preferred ecosystem architecture

```text
Persistent supervisor
├── skill-based router
├── ephemeral repository workers
├── multimodal perception experts
├── browser/desktop execution workers
├── research and evidence workers
├── security critic
├── test verifier
└── durable decision journal
```

### Routing pattern
Infer required capabilities, select only the relevant experts, execute them in isolation, aggregate structured outputs, verify, then promote or reject the result.

### Ephemeral worker output
Every worker should return:

```json
{
  "status": "success|failed|partial",
  "changes": [],
  "commands_run": [],
  "tests": [],
  "remaining_risks": [],
  "artifacts": [],
  "recommended_next_action": ""
}
```

## Learned component roles

- **Late CLI** — repository-level ephemeral worker harness; strong architecture candidate.
- **Open Interpreter** — desktop and terminal execution layer.
- **ego-lite plus Playwright** — authenticated browser execution, with Playwright retained as deterministic foundation.
- **KimiK3Manim** — six-agent deterministic supervisor and repair-loop reference.
- **Skill-MoE** — dynamic capability-based agent routing reference.
- **DeepSeek-VL2** — multimodal perception pilot for screenshots, OCR, documents, charts, and grounding.
- **PapersGPT** — research evidence and Zotero knowledge layer.
- **Artificial-Intelligence-Universe** — discovery feed only; never auto-install listed tools.
- **awesome-mixture-of-experts** — permanent MoE research feed.
- **awesome-multimodal-ml** — multimodal taxonomy and curriculum feed.
- **PremAI** — private and sovereign inference architecture; evaluate specific components such as PremSQL.
- **AWS Neuron** — future Inferentia/Trainium backend, not a current local dependency.
- **Boring Marketing** — commercial marketing architecture reference, not a core local-first component.
- **china-lawyer-analyst** — modular domain-routing and verification architecture reference only.
- **legacy neural MoE repositories** — educational references for gating, dispatch, and balancing, not default production foundations.
- **unofficial Kimi-ai-K3/kimi-k3** — quarantine; do not install, authenticate, or provide credentials.

## Multimodal operating pattern

```text
Artifact
├── screenshot expert
├── OCR expert
├── document expert
├── chart expert
├── audio expert
└── video-frame expert
      ↓
Strict observation schema
      ↓
Skill router
      ↓
Operational agents
      ↓
Critic and verifier
```

Never let a visual model directly control a machine without a policy and verification layer.

## Knowledge preservation standard

Canonical source:

`edneycaleb-droid/hermes-ai-knowledge-ops/00_AI_ECOSYSTEM_INDEX.md`

Portable skill:

`.chatgpt/skills/ai-ecosystem-curator/SKILL.md`

Every repository should contain a prominent root-level `00_AI_ECOSYSTEM_INDEX.md` pointing to the canonical registry and a copy or pointer to this skill.

## Response format for future evaluations
For each candidate, provide:

1. What it is
2. Best role in the ecosystem
3. Key strengths
4. Key risks and limitations
5. Integration recommendation
6. Decision classification
7. Direct-use, architecture, and trust ratings when useful
8. Exact next action

For batches, end with a ranked decision table and a combined architecture showing how the useful pieces fit together.

## Installation and change policy

- Documentation and pointers may be added directly when requested.
- Code changes should use isolated branches or worktrees and pass tests before merge.
- High-risk tools remain quarantined until independent verification succeeds.
- Do not overwrite established project behavior merely because a new tool is interesting.
- Prefer reversible, minimal, auditable changes.

## Success criteria
The skill is being used correctly when:

- findings remain easy to find;
- the canonical registry is current;
- risky tools are not accidentally trusted;
- architecture and executable adoption are clearly separated;
- duplicate tools are avoided;
- workers return structured evidence;
- integrations are tested, reversible, and documented.
