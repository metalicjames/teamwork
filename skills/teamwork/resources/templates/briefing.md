# BRIEFING — [UTC ISO-8601 Timestamp]

## Mission
[One-line summary of current high-level objective and milestone]

## 🔒 My Identity
- Archetype: [sentinel | orchestrator | explorer | worker | critic | challenger | auditor | test_writer]
- Role: [Specific functional role title, e.g., Primary Storage Engine Worker]
- Working Directory: [.agents/teamwork/<agent_id>/]
- Original Parent: [Conversation ID of Sentinel or top-level invoker]
- Active Milestone: [Milestone ID, e.g., M1, M2]
- Platform Harness: [Subagent-Native | Claude Code | OpenAI Codex / Custom GPT]

## 🔒 Key Constraints
- Mode: [development | demo | benchmark]
- Execution Boundaries: [Read-only investigation vs armed implementation]
- Taboo Files: Never create AGENTS.md or GEMINI.md anywhere in the workspace.
- Workspace Hygiene: No production code or tests in .agents/teamwork/ (metadata only).
- Integrity Rules: Zero placeholder stubs, zero fabricated passes, standard library only if benchmark mode.

## Current Parent & Coordination
- Parent Conversation ID: [Immediate parent conversation ID]
- Last Updated: [UTC ISO-8601 Timestamp]
- Communication Channel: [send_message for status notifications; file artifacts for content]

## Team Roster & Topology
| Agent Role | Conversation ID | Working Directory | Harness Mode | Assigned Focus |
| :--- | :--- | :--- | :--- | :--- |
| **Sentinel** | `[Conv ID]` | `.agents/teamwork/sentinel/` | Native / Host | Top-level monitor & victory audit |
| **Orchestrator** | `[Conv ID]` | `.agents/teamwork/orchestrator/` | Subagent | Milestone decomposition & dispatch |
| **Worker 1** | `[Conv ID]` | `.agents/teamwork/worker_1/` | Subagent | Component A implementation |
| **Critic** | `[Conv ID]` | `.agents/teamwork/critic_1/` | Subagent | Gate 1 code & architecture review |
| **Challenger** | `[Conv ID]` | `.agents/teamwork/challenger_1/` | Subagent | Gate 2 adversarial stress probing |
| **Auditor** | `[Conv ID]` | `.agents/teamwork/auditor_1/` | Subagent | Gate 3 forensic integrity verification |
| **Test Writer**| `[Conv ID]` | `.agents/teamwork/test_writer_1/`| Subagent | E2E opaque-box testing track |

## Active Timers & Background Schedules
- Heartbeat Schedule: `CronExpression: "*/8 * * * *"` (Task ID: `[task_id]`)
- Liveness Check: Evaluated every 10 minutes by Orchestrator.
- Stale Deadline: 20 minutes unresponsive triggers agent replacement.
- Active Background Tasks:
  - Task ID: `[task_id]` | Command: `[build / test command]` | Status: `[running]`

## Succession Status (16-Spawn Protocol)
- Succession Required: `[No | Yes]`
- Cumulative Spawn Count: `[N / 16]`
- Predecessor Conversation ID: `[Predecessor ID or None]`
- Successor Conversation ID: `[TBD or Successor ID]`
- Succession Invariant: Upon 16 spawns, emit soft handoff, terminate crons, and spawn successor passing Original Parent ID.

## Task Summary
- **Primary Deliverable**: [Clear summary of what is being constructed or reviewed]
- **Acceptance Criteria**: [Checklist of verifiable requirements from ORIGINAL_REQUEST.md]
- **Interface Contracts**: [Pointer to contract definitions in PROJECT_PLAN.md]

## Settled Technical Decisions
- [Decisions locked in by Phase 0 survey or prior milestones that MUST NOT be re-litigated by subsequent agents]
- Decision 1: [e.g., Storage format established as append-only binary log with 64-bit offsets]
- Decision 2: [e.g., Serialization protocol standardized on JSON-RPC over Unix domain sockets]

## 3-Step State Recovery Checkpoint
When resuming after context reset or process restart:
1. **Step 1 — Ingest BRIEFING.md**: Re-read this file to recover identity, settled decisions, and succession counters.
2. **Step 2 — Ingest Authoritative Requirements**: Read `ORIGINAL_REQUEST.md` and `DISPATCH.md`.
3. **Step 3 — Reconcile Workspace State**: Read `progress.md`, `GATE_STATUS.md`, `DEAD_ENDS.md`, and clean dead tasks with `manage_task`.

## Artifact Index
| File Path | Purpose | Owning Agent | Status |
| :--- | :--- | :--- | :--- |
| `ORIGINAL_REQUEST.md` | Authoritative requirements & integrity tier | Sentinel / User | Locked |
| `PROJECT_PLAN.md` | Architecture, feature inventory & milestones | Orchestrator | Active |
| `progress.md` | Checklist & heartbeat timestamp | Active Agent | Updated continuously |
| `handoff.md` | 5-component self-contained handoff | Active Agent | Completed on yield |
| `GATE_STATUS.md` | Milestone gate check ledger | Orchestrator | Evaluated per iteration |
| `DEAD_ENDS.md` | Oscillation guard & refuted architectures | Orchestrator | Active |
| `TEST_INFRA.md` | 4-tier E2E testing specification | Test Orchestrator | Active |
| `TEST_READY.md` | E2E test suite readiness certification | Test Orchestrator | Published prior to acceptance |
