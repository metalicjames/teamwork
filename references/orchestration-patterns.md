# Phase 2: Orchestration Patterns & Multi-Agent Workflows

Following user approval of the Phase 1 task specification, the **Project Sentinel** records `<working_dir>/ORIGINAL_REQUEST.md`, conducts pre-flight environment checks, and routes autonomous execution to one of five specialized multi-agent orchestration patterns.

---

## 1. Routing Decision Table & Boundary Constraints

| Execution Pattern | Target Orchestrator | When to Route Here | Key Architectural Characteristics |
| :--- | :--- | :--- | :--- |
| **1. Project Pattern (General Distributed SWE)** | `teamwork-orchestrator` ([../agents/teamwork-orchestrator.md](../agents/teamwork-orchestrator.md)) | *Default* for multi-file software engineering, framework migrations, systems simulations, and greenfield systems. | Phase 0 survey (3 parallel scouts; completeness > consensus); Dual-track architecture (Implementation + E2E Testing); 6-step canonical loop; Oscillation & Regression guards; 16-spawn self-succession. |
| **2. SWE Light (Sequential Refinement)** | `teamwork-swe-light` ([../agents/teamwork-swe-light.md](../agents/teamwork-swe-light.md)) | Localized, single-unit modification (bug fix, targeted refactor) with **explicit** user prompt signal. | 4 Hard Rules: No pre-work; Sequential refinement; Verbatim task propagation inside `<original_task>` tags; Independent diff test verification. |
| **3. Document Review (RSA Trees & Synthesis)** | `teamwork-doc-orchestrator` ([../agents/teamwork-doc-orchestrator.md](../agents/teamwork-doc-orchestrator.md)) | Technical papers, RFCs, architecture specifications, and design critiques. | Segment triage; Random Sample Aggregation (RSA) review trees; Synthesis Group Orchestration; Verbatim citation verification. |
| **4. Math / Proof (5-Phase Outer Loop)** | `teamwork-proof-orchestrator` ([../agents/teamwork-proof-orchestrator.md](../agents/teamwork-proof-orchestrator.md)) | Formal theorem proving, mathematical derivations, and rigorous bound verification. | 5-Phase outer loop (Exploration, Decomposition, Subproblem Solving, Verification, Revision); Layer tournament tree delegation (`teamwork_layer`). |
| **5. Large-Team Swarm (`colosseum`)** | `teamwork-colosseum` ([../agents/teamwork-colosseum.md](../agents/teamwork-colosseum.md)) | High-scale tournament searches for hard conjectures, combinatorial bounds, or large parameter spaces with explicit user opt-in. | Blackboard architecture (`BLACKBOARD.md`); Competing waves of parallel solvers and adversarial falsers converging on certified ground truth. |

### Routing Boundary Edge Cases
1. **Unsignaled Single-File Modifications**: If a task appears compact but the user did not explicitly include an opt-in signal (e.g. *"keep it small"*, *"run as one contained change"*), the Sentinel **MUST route to the Project Pattern**. Orchestrators are strictly prohibited from self-sizing tasks into SWE Light.
2. **Mathematical Inquiries Embedded in Documents**: If a mathematical problem is presented as part of reviewing or verifying an academic paper or RFC, route to **Document Review**, utilizing specialized proof review lenses.
3. **Document Review Without Target Documents**: If a user requests a review team but provides no source document, RFC, or manuscript to evaluate, route to the **Project Pattern** to research and draft the necessary material first.

---

## 2. Pattern 1: The Project Pattern (General Distributed SWE)

The Project Pattern coordinates complex, multi-file software engineering across parallel work tracks and adversarial verification gates:

```
User <───> [Sentinel] (permanent coordination & liveness monitor)
               │
               ▼
   [Project Orchestrator] ─── self-succeeds at 16 spawns ───► [Successor Orchestrator]
               │
               ├── Phase 0: Survey Stage (3 parallel Explorers / Spec Miners; Completeness > Consensus)
               │
               ├── Dual-Track Architecture:
               │   ├── Implementation Track (Milestones M1..Mn)
               │   │   └── Sub-Orchestrator per Milestone
               │   │         └── Canonical Iteration Loop (Assess → Explore → Implement →
               │   │                                       Review/Challenge → Audit → Gate)
               │   │               ├── Oscillation Guard (2 failures → DEAD_ENDS.md)
               │   │               └── Regression Guard (redesign on regression)
               │   │
               │   └── E2E Testing Track (Parallel, Opaque-Box, Requirements-Derived)
               │         └── Dedicated Test Orchestrator / Test Writers
               │               ├── Test infrastructure & 4-tier suite (11N + max(5, N/2))
               │               └── Publishes TEST_READY.md when complete
               │
               └── Final Milestone Execution:
                     ├── Phase 1: Poll TEST_READY.md → 100% E2E test pass (Tiers 1-4)
                     └── Phase 2: Adversarial coverage hardening (Tier 5 stress testing)
```

### Stage 1: Phase 0 Survey
1. Spawn 3 read-only **Explorers** (`teamwork-explorer`) in parallel to examine authoritative requirements, existing codebase topology, interfaces, and toolchains.
2. The Orchestrator aggregates survey findings into `PROJECT_PLAN.md` adhering to the rule of **Completeness > Consensus**: unique observations substantiated with `path/to/file:line` citations are retained rather than discarded by majority vote.

### Stage 2: Dual-Track Decomposition
The Orchestrator partitions work into two concurrent tracks:
1. **Implementation Track**: Decomposed into sequential milestones (`M1..Mn`) in `PROJECT_PLAN.md`.
2. **E2E Testing Track**: Dispatched immediately in parallel under an independent testing sub-orchestrator or `teamwork-test-writer` subagents. Tests treat the implementation as an opaque black box, derived exclusively from `ORIGINAL_REQUEST.md` and `PROJECT_PLAN.md`.

### Stage 3: The 6-Step Canonical Iteration Loop (Per Milestone)
Each milestone executes this disciplined 6-step loop:
- **Step a (Assess)**: Evaluate milestone targets, dependency contracts, and previous iteration findings.
- **Step b (Explore)**: Target worker investigates assigned files and formulates a surgical diff plan.
- **Step c (Implement)**: `teamwork-worker` authors production code and unit tests within its **exclusive file ownership boundary**, verifying local compilation and unit tests before handoff.
- **Step d (Review & Challenge)**: Independent fresh-context subagents evaluate candidate changes:
  - `teamwork-critic`: Inspects correctness, style, interface conformance, and error handling (`APPROVE` / `REJECT`).
  - `teamwork-challenger`: Authors adversarial probes (boundary inputs, race conditions, resource limits) with the **empirical reproduction guarantee** (`SURVIVED` / `BROKEN`).
- **Step e (Forensic Audit)**: `teamwork-auditor` verifies compliance with active `Integrity mode` and independently executes tests to confirm genuine execution (`PASS` / `INTEGRITY VIOLATION`).
- **Step f (Gate Evaluation & Compilation)**: Orchestrator records outcomes in `<working_dir>/GATE_STATUS.md`. Gate pass requires a **strict logical AND**:
  $$\text{Gate Pass} = \text{Build/Test Pass} \land (\text{Critic} == \text{APPROVE}) \land (\text{Challenger} == \text{SURVIVED}) \land (\text{Auditor} == \text{PASS})$$

### Stage 4: Anti-Degradation Guards
- **Oscillation Guard**: If the same test failure or compilation defect recurs across **2 consecutive iterations**, the orchestrator blocks further attempts with that approach. The failed strategy is recorded in `<working_dir>/DEAD_ENDS.md`, and the team must adopt a fundamentally distinct technical architecture.
- **Regression Guard**: Any regression in previously passing test suites halts forward milestone progress until resolved.

### Stage 5: Final Milestone Two-Phase Verification
- **Phase 1**: Polls for `<working_dir>/TEST_READY.md`. Sequentially executes E2E test tiers 1 through 4 until 100% pass rate is achieved.
- **Phase 2**: Adversarial stress hardening with `teamwork-challenger` to verify system resilience under edge conditions.

### Stage 6: 16-Spawn Self-Succession Protocol
To prevent context window saturation over extended projects:
- **Trigger**: Cumulative subagent dispatches reach **16** ($\text{spawn\_count} \ge 16$) AND all active child subagents have completed.
- **Soft Handoff**: Current orchestrator writes a structured soft handoff report to `handoff.md`, updates `BRIEFING.md § Succession Status`, terminates active background crons via `manage_task`, and launches a fresh successor orchestrator passing the **original parent conversation ID** (Sentinel) to maintain shallow hierarchy.

---

## 3. Pattern 2: SWE Light (Sequential Refinement)

SWE Light executes compact, focused code modifications under **4 Hard Rules**:

1. **Rule 1 — Direct Dispatch (No Pre-Work)**:
   The orchestrator dispatches an implementer immediately. Spawning reconnaissance explorers, preliminary surveys, or multi-milestone roadmaps is strictly prohibited.
2. **Rule 2 — Sequential Refinement, Not Parallel Panels**:
   Iteration follows a strictly linear chain of refinement:
   $$\text{Implementer} \longrightarrow \text{Reviewer 1} \longrightarrow \text{Reviewer 2} \longrightarrow \dots \longrightarrow \text{Done}$$
   No competing parallel implementers or multi-member reviewer panels.
3. **Rule 3 — Propagate Task Verbatim Inside `<original_task>` Tags**:
   Every dispatched subagent receives the user's initial task unedited, wrapped inside `<original_task>` ... `</original_task>` XML tags in the dispatch prompt. Never truncate or paraphrase instructions.
4. **Rule 4 — Verify Independently Before Accepting Diff**:
   The orchestrator and reviewers independently execute the project test suite against candidate diffs before accepting any handoff.

---

## 4. Pattern 3: Document Review (RSA Trees & Synthesis)

Coordinates multi-angle critiques of technical papers, RFCs, and architecture proposals:

1. **Pre-flight Tooling Verification**: Confirm availability of required document extraction, rendering, and analysis tools (`teamwork-dependency-auditor`).
2. **Document Triage into Segments**: Partition large documents into logical sections, thematic modules, or page clusters.
3. **Random Sample Aggregation (RSA) Review Trees**:
   For each document segment, dispatch a group coordinator orchestrating an RSA review tree across orthogonal lenses:
   - *Architectural & Theoretical Soundness*
   - *Empirical & Methodological Rigor*
   - *Structural Clarity & Precision*
   - *Adversarial Counterexamples & Edge Cases*
4. **Synthesis Group Orchestration**:
   A dedicated Synthesis Orchestrator aggregates segment review trees, deduplicates overlapping observations, resolves contradictory assessments by verifying the primary text, and ranks findings (`Blocker`, `Major`, `Nit`).
5. **Document Victory Audit**:
   `teamwork-victory-auditor` confirms that every quoted text passage, line citation, table figure, and mathematical formula exists verbatim in the source document.

---

## 5. Pattern 4 & 5: Math / Proof & Colosseum Swarms

Coordinates formal theorem proving, lemma derivations, and high-scale conjecture tournaments:

### The 5-Phase Proof Outer Loop
1. **Phase 1 — Exploration**: Formulate candidate proof strategies; execute computational searches and counterexample sweeps in scratch space.
2. **Phase 2 — Decomposition**: Decompose winning strategy into a formal Lemma DAG in `PROJECT_PLAN.md` and compile master LaTeX skeleton (`proof.tex`).
3. **Phase 3 — Subproblem Solving**: Parallel solvers (`teamwork-worker`) draft independent derivations for individual lemmas.
4. **Phase 4 — Verification**: Pair each candidate lemma with an adversarial falser (`teamwork-challenger`) searching for counterexamples, followed by logical audit (`teamwork-auditor`).
5. **Phase 5 — Revision & Synthesis**: Resolve derivation gaps and assemble verified lemmas into the complete deliverable.

### Layer Tournament Tree Delegation (`teamwork_layer`)
Organize subproblem solvers as a hierarchical tournament tree:
- Leaf nodes explore diverse derivation techniques.
- Parent nodes pair candidate derivations with falsers and merge verified lemmas upward.

### Colosseum High-Scale Swarm
For open mathematical conjectures or large parameter spaces:
- Maintain `<working_dir>/BLACKBOARD.md` separating *Verified Facts*, *Active Hypotheses*, and *Refuted Dead Ends*.
- Dispatch concurrent tournament waves of solvers and falsers until convergence on certified ground truth.
