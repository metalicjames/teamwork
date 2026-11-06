# Teamwork Reference Examples & Workflow Guides

Welcome to the Teamwork reference examples. This directory contains practical walkthroughs and guides demonstrating how autonomous multi-agent teams plan, implement, review, and verify complex technical objectives across diverse domains.

---

## Directory Navigation
- **[Software Engineering Walkthrough](software-engineering-walkthrough.md)**: A complete, end-to-end trace of a distributed key-value storage engine implementation under the **Project Pattern**, detailing Phase 0 survey, dual-track testing, adversarial verification gates, oscillation recovery, and victory audit.
- **[Operational Protocols](../references/operational-protocols.md)**: Specifications for the 5-component handoff, 3-step state recovery, 16-spawn self-succession, and heartbeat monitoring.
- **[Orchestration Patterns](../references/orchestration-patterns.md)**: Complete guide to the 5 canonical execution patterns and routing rules.
- **[Verification Gates](../references/verification-gates.md)**: Deep dive into the Critic, Challenger, Auditor, and Victory Auditor verification gates.

---

## Orchestration Patterns At A Glance

Teamwork supports five specialized execution patterns:

| Execution Pattern | Target Orchestrator | Primary Use Case | Key Differentiators |
| :--- | :--- | :--- | :--- |
| **1. Project Pattern** | `teamwork-orchestrator` | Multi-file software engineering, greenfield systems, migrations | Phase 0 survey (3 scouts; Completeness > Consensus); Dual-track architecture (Implementation + E2E Testing); 6-step canonical loop; 16-spawn succession. |
| **2. SWE Light** | `teamwork-swe-light` | Compact, single-unit bug fixes or localized refactors | 4 Hard Rules: Direct dispatch (no pre-work); Sequential refinement; Verbatim `<original_task>` propagation; Independent test verification. |
| **3. Document Review** | `teamwork-doc-orchestrator` | RFCs, technical papers, architectural specifications | Segment triage; Random Sample Aggregation (RSA) review trees; Synthesis Group Orchestration; Verbatim citation verification. |
| **4. Math / Proof** | `teamwork-proof-orchestrator` | Formal theorem proving, mathematical derivations | 5-Phase outer loop (Exploration, Decomposition, Subproblem Solving, Verification, Revision); Layer tournament tree delegation. |
| **5. Swarm (Colosseum)** | `teamwork-colosseum` | Open conjectures, large parameter searches | High-scale tournament waves converging on `BLACKBOARD.md` ground truth. |

---

## Standard Multi-Agent Lifecycle Progression

Every Teamwork project progresses through five disciplined stages:

```
[Phase 1: Intake & Scoping]
           │
           ▼
[Routing & Pre-Flight Checks] ──► Select 1 of 5 Orchestration Patterns
           │
           ▼
[Phase 0: Survey Stage]      ──► 3 Parallel Scouts (Completeness > Consensus)
           │
           ▼
[Dual-Track Execution]       ──► Implementation Track (Milestones M1..Mn)
           │                     E2E Testing Track (4-Tier Suite: 11N + max(5, N/2))
           ▼
[Milestone Verification]     ──► Gate 1 (Critic) ──► Gate 2 (Challenger) ──► Gate 3 (Auditor)
           │                     Composite Gate Pass = Strict Logical AND
           ▼
[Final Acceptance & Victory] ──► Phase 1: 100% E2E Pass ──► Phase 2: Victory Audit
```

---

## Workspace Directory Conventions

Agents operate with strict workspace isolation:

```
project_root/
├── src/ / pkg/                      # Production source code
├── tests/                           # Unit and E2E test suites
└── .agents/teamwork/                # METADATA ONLY (source/tests strictly prohibited here)
    ├── sentinel/                    # Sentinel BRIEFING.md, ORIGINAL_REQUEST.md
    ├── orchestrator/                # Orchestrator BRIEFING.md, progress.md, PROJECT_PLAN.md
    ├── worker_1/                    # Worker 1 private workspace (DISPATCH.md, handoff.md)
    └── auditor_1/                   # Auditor private workspace
```

### Core Invariants:
1. **Exclusive Directory Ownership**: Each subagent writes only to its assigned `.agents/teamwork/<agent_id>/` directory.
2. **Metadata-Only Rule**: Never place production code or tests in `.agents/teamwork/`.
3. **Taboo Names**: Never name any file `AGENTS.md` or `GEMINI.md`.
