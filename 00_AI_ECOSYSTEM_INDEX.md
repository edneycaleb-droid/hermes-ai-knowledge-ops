# AI Ecosystem Knowledge Index

This is the canonical, easy-to-find registry for AI tools, models, repositories, research feeds, architecture patterns, security decisions, and integration priorities used across Caleb's GitHub projects.

## Decision labels

- **ADOPT** — approved for repository-specific implementation after tests.
- **PILOT** — evaluate in a disposable branch, worktree, container, or VM.
- **WATCH** — monitor; do not add as a dependency yet.
- **REFERENCE** — extract design or research patterns only.
- **QUARANTINE** — never provide credentials or execute outside malware-analysis isolation.
- **REJECT** — unrelated, obsolete, redundant, or untrustworthy.

## Target architecture

```text
Hermes central supervisor
├── skill/capability router
├── ephemeral repository workers
├── Claude, Codex, and Kimi escalation models
├── local Ollama or llama.cpp workers
├── multimodal perception experts
├── MCP tools and Agent Skills
├── Playwright and authenticated-browser execution
├── deterministic test/security/critic gates
├── Git worktree isolation
└── durable evidence and decision registry
```

Standard lifecycle:

```text
Discover → verify source → classify → score → sandbox → implement → test → critique → repair → PR → monitor
```

## Tool and platform registry

| Resource | Best role | Decision |
|---|---|---|
| `mlhher/late-cli` | Ephemeral repository-agent harness, clean context, worktree isolation | PILOT / ADOPT |
| Open Interpreter | Local terminal and desktop execution | PILOT / ADOPT |
| ego-lite | Authenticated-browser execution alongside Playwright | PILOT |
| Playwright | Deterministic browser automation and validation | ADOPT |
| `HarleyCoops/KimiK3Manim` | Deterministic multi-agent supervisor, Pydantic artifacts, critic/repair loop, MCP and skills | REFERENCE |
| Pi Kimi providers | Modular Kimi worker access; independently validate authentication | PILOT |
| PapersGPT | Zotero-based academic evidence layer and MCP research source | PILOT |
| Boring Marketing | Paid Slack SEO/AI-visibility product; useful shared-memory and specialized-skill design | REFERENCE |
| Kimiflare | Cloudflare-hosted Kimi coding environment | WATCH |
| EvoLink Kimi K3 | Paid OpenAI-compatible fallback gateway | WATCH |
| `premAI-io` | Sovereign/private inference, confidential computing, local text-to-SQL patterns | WATCH / EXTRACT |
| `aws-neuron` | Future Inferentia/Trainium deployment backend | WATCH |

## Skill-based mixture-of-experts

`dinobby/Skill-MoE` is the primary architecture reference for dynamic task-to-expert routing:

```text
Task → infer capabilities → match expert profiles → recruit top-k workers → execute → aggregate → verify
```

Recommended routing factors:

```text
skill match × historical success × confidence × availability × trust level ÷ cost
```

Persist each worker's domain scores, success rate, latency, cost, failure classes, permissions, and security level. Never route solely by model reputation.

### Neural MoE references

| Resource | Use | Decision |
|---|---|---|
| `XueFuzhao/awesome-mixture-of-experts` | Current MoE research discovery feed | WATCH / INGEST |
| `davidmrau/mixture-of-experts` | Sparse top-k gating, dispatcher, and balancing reference | REFERENCE |
| `lucidrains/mixture-of-experts` | Historical implementation; newer ST-MoE work preferred | REFERENCE |
| `MoeOrganization` | Old Perl/Scala project unrelated to AI MoE | REJECT |

Track sparse routing, expert specialization/collapse, capacity factors, load balancing, expert parallelism, communication cost, routing stability, multimodal allocation, and auxiliary-loss-free balancing.

## Multimodal intelligence

| Resource | Role | Decision |
|---|---|---|
| `deepseek-ai/DeepSeek-VL2` | OCR, screenshot, chart, document, and grounding experiments | PILOT |
| `pliang279/awesome-multimodal-ml` | Multimodal taxonomy and research curriculum | INGEST / REFERENCE |

Visual models must return structured observations rather than directly controlling a machine:

```json
{
  "screen_type": "unknown",
  "visible_text": [],
  "interactive_elements": [],
  "target_element": null,
  "confidence": 0.0,
  "recommended_action": null,
  "needs_human_review": true
}
```

A policy layer checks permissions, then a deterministic executor acts.

## Discovery feeds

- `frangelbarrera/Artificial-Intelligence-Universe`: broad candidate catalog; never trust catalog inclusion as validation.
- `XueFuzhao/awesome-mixture-of-experts`: MoE papers, models, systems, and libraries.
- `pliang279/awesome-multimodal-ml`: foundational multimodal research taxonomy.
- GitHub search/topics/trending, Hugging Face, arXiv, Papers with Code, npm, and PyPI.

Every candidate requires official-owner verification, maintenance review, license review, security inspection, cost classification, sandbox testing, redundancy analysis, and a rollback plan.

Suggested adoption gate:

```text
Overall score ≥ 85/100
Security score ≥ 80/100
No critical red flags
Approved license
Sandbox tests passed
No superior existing component
```

## Candidate schema

```json
{
  "name": "",
  "category": "",
  "source_catalog": "",
  "homepage": "",
  "repository": "",
  "official_owner_verified": false,
  "license": "unknown",
  "open_source": null,
  "local_first": null,
  "last_commit": null,
  "release_recency_days": null,
  "archived": null,
  "security_policy": null,
  "install_method": null,
  "requires_api_key": null,
  "paid_dependency": null,
  "risk_score": null,
  "capability_score": null,
  "recommendation": "pending-review"
}
```

## Mandatory security gates

1. Resolve the official owner, repository, documentation, and release channel.
2. Inspect commits, releases, issues, PRs, archived state, and dependency freshness.
3. Inspect install scripts, post-install hooks, telemetry, credential storage, network destinations, shell privileges, and filesystem scope.
4. Confirm license and commercial/hosting restrictions.
5. Classify cost and external dependencies.
6. Install only in disposable worktrees, containers, VMs, Windows Sandbox, or temporary profiles.
7. Compare against current components and reject redundant tools.
8. Require tests, evidence, rollback instructions, and a reviewed PR.

## Quarantine registry

### `Kimi-ai-K3/kimi-k3` — HIGH RISK

- Unofficial and not operated by Moonshot AI.
- Minimal organization and contributor history.
- Executable releases without sufficient transparent build provenance.
- Scarcity, referral, and free-lifetime marketing tactics.
- Unsupported claims about hundreds of browser agents and free proxy infrastructure.
- Never provide GitHub tokens, API keys, browser sessions, personal data, employer data, government data, or payment information.
- Do not execute outside a disposable malware-analysis VM.

Use official Moonshot/Kimi channels and reviewed providers instead.

## Reusable domain-skill pattern

`CSlawyer1985/china-lawyer-analyst` is not authoritative for U.S., Louisiana, military, or VA matters. Its reusable architecture is:

```text
classify domain → load relevant modules → create checklist → retrieve authoritative sources → validate citations/currentness → reflect/revise → structured result
```

Apply that design to CI repair, repository maintenance, security, networking, trading research, and documentation.

## Worker output contract

Every ephemeral worker must return structured signal rather than unbounded raw context:

```json
{
  "status": "success|failed|partial",
  "summary": "",
  "changes": [],
  "commands_run": [],
  "tests": [],
  "evidence": [],
  "remaining_risks": [],
  "artifacts": [],
  "rollback": "",
  "recommended_next_action": ""
}
```

## Priority order

1. Build the skill registry and historical performance database.
2. Implement Skill-MoE-style dynamic routing.
3. Use Late-style ephemeral workers and worktree isolation.
4. Enforce strict outputs, tests, critic loops, and rollback plans.
5. Build a multimodal observation router with a policy boundary.
6. Ingest research catalogs through independent verification gates.
7. Keep local-first execution; paid cloud gateways are controlled fallbacks.
8. Preserve AWS Neuron as an optional future scaling backend.

## Maintenance policy

Keep this file at the root as `00_AI_ECOSYSTEM_INDEX.md`. Add every evaluated model, tool, skill, MCP server, provider, or catalog here with its source, decision, rationale, security concerns, and intended integration. Functional changes should normally enter through pull requests rather than uncontrolled direct edits.