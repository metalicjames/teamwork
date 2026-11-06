# Operational Protocols & Artifact Schemas

Teamwork coordinates autonomous agents across isolated execution contexts through standardized handoffs, persistent workspace state, liveness monitoring, and anti-degradation protocols.

---

## 1. The 5-Component Handoff Protocol

Every subagent interaction, milestone completion, or task transfer must conclude with a self-contained handoff report written to `<agent_dir>/handoff.md`. The receiving agent must be able to resume immediately without querying the sender.

### Mandatory 5 Sections:
1. **Observation**: Concrete, empirical facts directly observed during execution. Quote exact file paths, line numbers, terminal commands, process exit codes, and verbatim test output.
2. **Logic Chain**: Step-by-step deductive reasoning linking observations to intermediate findings and final assessments.
3. **Caveats**: Uninvestigated edge cases, operating assumptions, alternative interpretations, or environmental constraints. (State *"No caveats"* if none exist).
4. **Conclusion**: Scoped, actionable determination supported directly by the logic chain (e.g. milestone gate readiness, architecture recommendation, or defect classification).
5. **Verification Method**: Step-by-step procedures to independently reproduce and verify the conclusion, including exact test command lines, inspected files, and invalidation criteria.

### Handoff Classifications:
| Classification | When Applied | Required Sections |
| :--- | :--- | :--- |
| **Hard Handoff** | Milestone or task successfully completed | All 5 sections fully populated. |
| **Soft Handoff** | Task transfer or context succession (e.g. 16-spawn limit reached) | All 5 sections + **Remaining Work** detailing concrete next actions. |
| **Partial Handoff** | Agent blocked or replaced mid-task | Populates available sections and explicitly details where and why execution stalled. |

---

## 2. 3-Step State Recovery Protocol

When an agent resumes from a context reset, wakes from sleep, or starts as a successor orchestrator, it must execute this 3-step recovery sequence before performing actions:

1. **Step 1 — Ingest `BRIEFING.md`**:
   Read `<working_dir>/BRIEFING.md` to re-establish identity, active execution path, milestone status, settled architectural decisions, and next immediate actions.
2. **Step 2 — Ingest Authoritative Requirements**:
   Read `<working_dir>/ORIGINAL_REQUEST.md` (unalterable user requirements and integrity constraints) and `<agent_dir>/DISPATCH.md` (current turn assignment).
3. **Step 3 — Reconcile Workspace State**:
   Inspect `<working_dir>/progress.md` (and `PROJECT_PLAN.md`, `GATE_STATUS.md`, `DEAD_ENDS.md` if present) to verify what files changed on disk and clean up orphaned background tasks via `manage_task`.

---

## 3. The 16-Spawn Self-Succession Protocol

To prevent context window degradation during extended projects, orchestrators enforce self-succession:

### Trigger Conditions (Both Required Concurrently):
1. **Spawn Threshold**: Cumulative subagent invocations by the active orchestrator reach **16** ($\text{spawn\_count} \ge 16$).
2. **Quiescence**: All active child subagents (Explorers, Workers, Gate Reviewers) have concluded and delivered their handoffs.

### 5-Step Succession Procedure:
1. **Generate Soft Handoff**: The current orchestrator compiles a soft handoff to `<agent_dir>/handoff.md` detailing current milestone progress, settled technical choices, and remaining work.
2. **Persist State**: Update `<working_dir>/BRIEFING.md` with the succession status:
   ```markdown
   ## Succession Status
   - Succession required: Yes
   - Spawn count: 16 / 16
   - Predecessor Conversation ID: <current_conv_id>
   - Successor Conversation ID: [TBD]
   ```
   and ensure `<working_dir>/progress.md` is current.
3. **Terminate Crons & Background Tasks**: Abort all running background timers and cron monitors using `manage_task(Action="kill")`.
4. **Spawn Successor with Parent Passthrough**: Launch a fresh orchestrator instance using the same persona. Pass the **original parent conversation ID** (the Sentinel or top-level caller) as the successor's parent—NOT the predecessor's conversation ID—preserving a shallow 2-tier tree.
5. **Cross-Track Notification**: If a parallel sub-orchestrator is active, notify it of the successor's conversation ID via `send_message`.

---

## 4. Liveness & Heartbeat Protocol

### Heartbeat Invariant:
Every active agent updates its `<agent_dir>/progress.md` after completing meaningful work, recording:
`Last visited: [UTC ISO-8601 timestamp]`
During long-running compilation or test commands, agents must touch `progress.md` at least once every 5 minutes.

### Monitoring Deadlines:
1. **Periodic Health Check**: The coordinating orchestrator evaluates child heartbeats every 10 minutes (via `schedule` cron or turn transitions).
2. **20-Minute Stale Deadline (Retry / Replace)**:
   If an agent's `Last visited` timestamp is older than 20 minutes with no output:
   - Issue a status query message and allow a 2-minute response window.
   - If still unresponsive, terminate the process via `manage_task` and spawn a replacement.
3. **20-Minute Hard Dispatch Deadline**:
   If an agent remains completely unresponsive for 20 minutes from initial dispatch, immediately kill and replace it, appending a log entry:
   `HANG: [role] unresponsive after 20 min, replaced.`

---

## 5. Fault Tolerance Escalation Ladder

When subagent tasks encounter errors or timeouts, coordinators escalate through these 5 tiers:

$$\text{Retry} \longrightarrow \text{Replace} \longrightarrow \text{Skip} \longrightarrow \text{Redistribute} \longrightarrow \text{Degrade}$$

1. **Retry**: Re-invoke the same agent instance with clarified inputs or error diagnostics (maximum 1 retry).
2. **Replace**: Terminate the failing instance via `manage_task` and spawn a fresh subagent with clean context.
3. **Skip**: For non-critical exploratory tasks (e.g. secondary documentation sweeps), omit the task.
   *(Auditor Exemption: `teamwork-auditor` and `teamwork-victory-auditor` can NEVER be skipped).*
4. **Redistribute**: Partition the failing task into smaller sub-units assigned to distinct workers.
5. **Degrade**: Report insurmountable blockers to the user and request manual environment intervention.

---

## 6. Workspace Conventions

1. **Exclusive Directory Ownership**:
   Agents own their assigned directory (`.agents/teamwork/<agent_id>/`). Agents write only to their own directory, though they may read other directories.
2. **Metadata-Only Rule**:
   The `.agents/teamwork/` directory is reserved strictly for operational metadata (`handoff.md`, `progress.md`, `DISPATCH.md`). Placing source code, test suites, or production data inside `.agents/teamwork/` is a **hard structural violation**.
3. **Taboo File Names**:
   Never create files named `AGENTS.md` or `GEMINI.md` anywhere in the repository, as host harnesses treat these as global system prompts.

---

## 7. Artifact Schemas & Templates

### 7.1 Authoritative Request (`<working_dir>/ORIGINAL_REQUEST.md`)
```markdown
[1-2 sentence project description, opening with any opt-in sentence or requested team]

Working directory: <path>
Integrity mode: [development | demo | benchmark]
[Optional: Operational Boundaries / Disallowed Shortcuts: The team shall refrain from: <forbidden items>]

[Optional: Reference material (paper URL, spec link, baseline files)]

## Requirements

### R1. [Primary deliverable]
[Observable behavior and interface contracts — what it does, not how to build it]

### R2. [Secondary requirement or constraint]
[Observable behavior and invariants]

## Verification Resources
[Optional: Existing test commands, reference scripts, datasets, or evaluation rubrics]

## Acceptance Criteria

### [Criterion category]
- [ ] [Objective, checkable condition verified via command execution or rubric]
```

### 7.2 Situational Awareness Memory (`<working_dir>/BRIEFING.md`)
```markdown
# BRIEFING — [timestamp]

## Mission
[One-line description of current objective]

## 🔒 My Identity
- Archetype: [sentinel | orchestrator | worker | critic | challenger | auditor]
- Roles: [role list]
- Working directory: [absolute path]
- Original parent: [caller conversation ID]
- Milestone: [milestone identifier]

## 🔒 Key Constraints
- [Non-negotiable constraints from request and dispatch]

## Current Parent
- Conversation ID: [parent ID]
- Updated: [timestamp]

## Succession Status
- Succession required: [No | Yes]
- Spawn count: [N / 16]
- Predecessor Conversation ID: [ID]
- Successor Conversation ID: [TBD]

## Task Summary
- **What to build**: [deliverable summary]
- **Success criteria**: [concrete criteria]
- **Interface contracts**: [path to PROJECT_PLAN.md]

## Settled Decisions
- [Decisions made that subsequent generations must not re-litigate]

## Artifact Index
- [path] — [purpose]
```

### 7.3 Milestone Gate Ledger (`<working_dir>/GATE_STATUS.md`)
```markdown
# Milestone Gate Status — Milestone [M]

| Gate | Assigned Agent | Status | Verdict Evidence & Findings |
| :--- | :--- | :---: | :--- |
| **Gate 1: Critic** | `teamwork-critic` | `[APPROVE | REJECT]` | [Summary of findings or clean approval] |
| **Gate 2: Challenger** | `teamwork-challenger` | `[SURVIVED | BROKEN]` | [Reproduction evidence or probes passed] |
| **Gate 3: Auditor** | `teamwork-auditor` | `[PASS | INTEGRITY VIOLATION]` | [Integrity check & live test counts] |

## Gate Determination
- **Status**: `[PASS | REMEDIATION_REQUIRED]`
- **Determination**: Strict logical AND of all three gates.
```

### 7.4 Oscillation Ledger (`<working_dir>/DEAD_ENDS.md`)
```markdown
# Dead Ends & Refuted Architectures

| Date / Iteration | Failed Strategy | Failure Signature | Root Cause & Mandated Alternative |
| :--- | :--- | :--- | :--- |
| [Timestamp] | [Description of approach] | [Exact error / test failure] | [Why it failed; alternate architecture mandated] |
```
