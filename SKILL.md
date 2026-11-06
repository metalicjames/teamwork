---
name: teamwork
license: MIT
description: >-
  Coordinates a collaborative multi-agent team for large software engineering
  projects, multi-file refactoring, systems simulations, document reviews, and
  mathematical proofs. Conducts a Phase 1 scoping interview (defining objectives
  and verifiable invariants with objective verification and integrity modes) and
  executes Phase 2 autonomous multi-agent orchestration with Sentinel, Project
  Orchestrator, Explorer, Worker, Critic, Challenger, Auditor, and Victory
  Auditor roles. Use when the user invokes /teamwork or requests a team of
  autonomous agents to deliver a complex project.
---

# Teamwork Multi-Agent Orchestration (`/teamwork`)

Teamwork coordinates a collaborative team of specialized, fresh-context subagents to deliver large software engineering projects, multi-file migrations, systems simulations, rigorous document critiques, and mathematical proofs.

Instead of overloading a single conversation context or allowing an implementer agent to self-certify incomplete work, Teamwork splits every run into two strict phases:

1. **Phase 1: Task Scoping & Specification (Scoping Interview)** — Clarifies scope, defines observable requirements (*what, not how*), establishes independent programmatic or rubric-based verification, maps shortcut restrictions to an **Integrity Mode** (`development`, `demo`, `benchmark`), sets the project working directory, and produces a reviewable prompt artifact (`prompt_draft.md`) requiring explicit user approval.
2. **Phase 2: Autonomous Execution (Structured Handoffs & Adversarial Gates)** — Once approved, **Project Sentinel** records `ORIGINAL_REQUEST.md`, runs pre-flight dependency checks, routes to the specialized **Orchestrator** for the chosen execution path, coordinates parallel **Explorers** and **Workers** with exclusive file ownership and per-agent scratch isolation, enforces independent verification gates (**Critic**, **Challenger**, **Auditor**) at every milestone, and blocks final completion on an end-to-end **Victory Auditor** (`VICTORY CONFIRMED`).

---

## Cross-Harness Delegation & Tool Mapping

Teamwork is harness-agnostic. Map each abstract action below to the native tools available in your current agent harness (see [references/harness-delegation.md](references/harness-delegation.md) for full details):

| Abstract Operation | Native / Tool Harness | Claude Code / Cowork | Codex / ChatGPT Work | Cursor / omp / Other Harnesses |
| :--- | :--- | :--- | :--- | :--- |
| **Spawn Fresh Subagent** | `invoke_subagent` (with `TypeName`, `Role`, `Prompt`) | `Agent` (`Task`) tool | `spawn_agent` (`fork_context: false` or `fork_turns: "none"`) | Native `task` / subagent tool (clean context) |
| **Define Custom Subagent** | `define_subagent` (or `agents/*.md`) | `./skills/` or `agents/*.md` | General-purpose subagent reads `agents/*.md` | Load `agents/*.md` or pass persona file path in prompt |
| **Message / Wake Subagent** | `send_message` | Resume/dispatch new `Agent` with artifact state | `send_message` / `wait` | Pass updated artifact state to fresh subagent |
| **Structured User Question** | `ask_question` | `AskUserQuestion` (or plain chat) | Structured question tool (or plain chat) | Structured question tool or plain-text question |
| **Periodic Progress Check** | `schedule` (`CronExpression`) | Check between milestone dispatches | Check between milestone dispatches | Check between milestone dispatches |

> **Subagent Persona Resolution**: All Teamwork subagent personas are defined in `agents/<persona-name>.md` (relative to this skill directory or the plugin root `../../agents/<persona-name>.md`).
> - If your harness registers named subagents from `agents/`, invoke the subagent by its frontmatter `name` (for example, `teamwork-sentinel`, `teamwork-interviewer`, `teamwork-orchestrator`, `teamwork-swe-light`, `teamwork-doc-orchestrator`, `teamwork-proof-orchestrator`, `teamwork-colosseum`, `teamwork-explorer`, `teamwork-worker`, `teamwork-critic`, `teamwork-challenger`, `teamwork-auditor`, `teamwork-victory-auditor`, `teamwork-dependency-auditor`).
> - If your harness does not register named subagents, either register them dynamically at runtime (e.g., via `define_subagent`) or spawn a general-purpose fresh-context subagent and instruct it to read `agents/<persona-name>.md` as its system persona before starting its task.
> - If your harness cannot nest subagents (subagents spawning subagents), the primary agent acts as both **Sentinel** and **Orchestrator**, dispatching **Explorers**, **Workers**, **Critics**, **Challengers**, **Auditors**, and the **Victory Auditor** directly as flat depth-1 subagents while preserving all artifact handoffs and fresh-context boundaries.

---

## Execution Paths & Routing Table

Teamwork automatically selects the team architecture, verification depth, and orchestrator role based on the work described in the approved prompt (see [references/orchestration-patterns.md](references/orchestration-patterns.md)):

| Execution Path | Orchestrator Persona | Best For | Trigger / Opt-in Signal | Pre-Flight Dependency Audit? | Final Victory Audit |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **1. Project Pattern (General Distributed SWE)** | `teamwork-orchestrator` ([agents/teamwork-orchestrator.md](agents/teamwork-orchestrator.md)) | Multi-file SWE, large-scale refactoring, systems simulation, and greenfield development. | *Default* (automatically selected for multi-component or multi-file tasks). | Yes (`teamwork-dependency-auditor`) | `teamwork-victory-auditor` |
| **2. SWE Light (Sequential Refinement)** | `teamwork-swe-light` ([agents/teamwork-swe-light.md](agents/teamwork-swe-light.md)) | One self-contained change — a localized bug fix, small feature, or contained refactor (4 Hard Rules). | Explicit prompt signal (e.g., *"keep it small"*, *"keep it focused"*, *"run as one contained change"*). | Yes (`teamwork-dependency-auditor`) | `teamwork-victory-auditor` |
| **3. Document Review (`document_review`)** | `teamwork-doc-orchestrator` ([agents/teamwork-doc-orchestrator.md](agents/teamwork-doc-orchestrator.md)) | Multi-angle critique, RSA review trees, and synthesis of papers, RFCs, and design docs. | Review requests (e.g., *"review this paper"*, *"critique this design doc"*). | No | `teamwork-victory-auditor` (Document Review mode) |
| **4. Math / Proof (`proof`)** | `teamwork-proof-orchestrator` ([agents/teamwork-proof-orchestrator.md](agents/teamwork-proof-orchestrator.md)) | Mathematical problem solving, 5-phase lemma derivations, and theorem proving. | Math prompts (e.g., *"prove theorem X"*, *"derive and verify mathematical bounds"*). | Optional (if CAS/Lean/Python needed) | Built-in pipeline proof verifier + `teamwork-victory-auditor` |
| **5. Math / Proof — Large Team (`colosseum`)** | `teamwork-colosseum` ([agents/teamwork-colosseum.md](agents/teamwork-colosseum.md)) | High-scale tournament networks for hard conjectures, counterexample search, and combinatorial optimization. | Explicit scale signal (e.g., *"Use a very large team of agents"*). | Optional (if compute tools needed) | `teamwork-victory-auditor` (Proof/Colosseum mode) |

---

## Integrity Modes

Teamwork enforces one of three internal integrity modes to align verification strictness with project requirements. During the Phase 1 interview, ask the user which shortcuts should be off-limits (without exposing internal mode names in the question) and map their answer to the corresponding mode in the prompt artifact:

| Integrity Mode | Purpose | Permitted Practices | Operational Boundaries / Disallowed Shortcuts | Auditor Enforcement |
| :--- | :--- | :--- | :--- | :--- |
| **`development`** *(Default)* | Rapid iteration | Code reuse, third-party libraries, and pre-built frameworks permitted. | Fabricating outputs, returning facade/stub implementations, or mocking/faking test passes. | Flags fabricated outputs, hardcoded/mocked test passes, and unimplemented stubs. |
| **`demo`** | Reproducible presentation | Standard libraries and general utilities permitted; core logic must be genuinely implemented. | All `development` prohibitions **plus**: copying core logic from open source, delegating core work to external tools/binaries, and reading test source/oracles to reverse-engineer expected behavior. | Audits imports, subprocess calls, and git/file access to ensure core logic is original and test oracles were not reverse-engineered. |
| **`benchmark`** | Thorough evaluation | Fully independent, from-scratch implementation using the language standard library only. | All `demo` prohibitions **plus**: using any third-party libraries or external frameworks for implementation. | Maximum strictness: rejects any non-stdlib dependency, any external delegation, any oracle peeking, and validates ground-truth execution outputs with binary veto. |

---

## Phase 1: Task Scoping & Specification (Scoping Interview)

Before spawning the execution team, align with the user on **what** to build and **how it will be independently verified**. Read [references/interview-protocol.md](references/interview-protocol.md) for full details and edge cases.

### Core Principle: Define Objectives and Observable Invariants, Not Internal Mechanics
Do not prescribe internal class hierarchies, file splits, or implementation algorithms in the prompt artifact unless the user explicitly requires them. Over-constraining *how* prevents Explorers and Workers from adapting to real codebase constraints; under-specifying *verification* allows agents to self-certify incomplete work.

### The 9-Step Scoping Protocol

1. **Step 1 — Intake & Triage**:
   - Inspect the user's initial `/teamwork` request and any referenced files in the workspace. Support `[skip-interview]` parameter to bypass directly to Phase 2; log unrecognized bracket parameters as ignored.
   - Identify what is already clear vs. what is missing across: (a) Scope & Purpose, (b) Execution Path opt-ins, (c) Operational Boundaries / Integrity Mode, (d) Verification & Acceptance Criteria, and (e) Working Directory.
   - **Respect user focus**: Minimize user roundtrips by batching all necessary inquiries into a single focused questionnaire (or at most two in highly multifaceted domains). Use `ask_question` when choices are discrete, or clear numbered questions in chat.
2. **Step 2 — Scope, Purpose & Execution Path Opt-ins**:
   - Clarify deliverable purpose: `showcase` / `demo`, `production`, `eval` / `benchmark`, or `exploration` / `research`.
   - Capture explicit opt-ins (e.g. *"keep it small and focused"* or *"Use a very large team of agents"*) in the opening sentence of the prompt artifact.
3. **Step 3 — Shortcut Restrictions & Integrity Mode Mapping**:
   - Elicit user constraints on open-source copying, external CLI delegation, oracle peeking, and third-party libraries.
   - Map to `development`, `demo`, or `benchmark`.
4. **Step 4 — Requirements (`R1`, `R2`, ...)**:
   - Draft modular requirement blocks describing observable behavior, inputs/outputs, invariants, and constraints — **what** the deliverable must do, not how to code it.
5. **Step 5 — Independent Verification & Dual-Track Testing**:
   - Autonomous software agents tend to prematurely claim completion when lacking external, executable verification. Establish unambiguous acceptance criteria grounded in repeatable automated tests that execute reliably and resist simulated passes.
   - For General Path SWE projects, require the **Dual-Track Testing Architecture**, where an independent test suite satisfies the minimum tier formula:
     $$\text{Total Minimum Tests} \ge 11N + \max\left(5, \left\lfloor \frac{N}{2} \right\rfloor\right)$$
6. **Step 6 — Acceptance Criteria**:
   - Convert verification checks into checkable `- [ ]` items grouped by category under `## Acceptance Criteria`.
7. **Step 7 — Infrastructure Constraints (Conditional)**:
   - Specify controlled API/filesystem boundaries only when dealing with sandbox or external job constraints.
8. **Step 8 — Project Working Directory**:
   - Existing codebase: use existing directory (do not ask). New project: ask, defaulting to `~/teamwork_projects/<project_name>`.
9. **Step 9 — Assemble, Validate & Request Approval**:
   - Write `prompt_draft.md` using the standard schema and present the **full text** directly to the user in chat.
   - Present anticipated path: *"Anticipating execution via the multi-milestone general engineering path; please indicate if you would prefer a single lightweight change."*
   - **STOP and wait for explicit user approval** before starting Phase 2.

---

## Phase 2: Autonomous Execution (Sentinel & Orchestrator Protocol)

Once the user explicitly approves the prompt artifact, transition immediately to **PROJECT SENTINEL** mode. Read [references/orchestration-patterns.md](references/orchestration-patterns.md), [references/verification-gates.md](references/verification-gates.md), and [references/operational-protocols.md](references/operational-protocols.md).

### Core Sentinel Responsibilities

As **Sentinel** ([agents/teamwork-sentinel.md](agents/teamwork-sentinel.md)), you are the permanent top-level project custodian. You **MUST NOT** write production code, debug implementation details, or make low-level technical decisions yourself — keep your context ultra-light to supervise the entire project lifecycle.

#### Responsibility 1: Baseline Ingestion & Request Persistence
1. Ensure the target `Working directory` exists (e.g., `mkdir -p <working_dir>/.teamwork/scratch`).
2. Write the approved prompt artifact **verbatim** to `<working_dir>/ORIGINAL_REQUEST.md` (immutable ground truth).
3. Initialize `<working_dir>/BRIEFING.md` to track active execution path, subagent IDs, current milestone, and state invariants.

#### Responsibility 2: Autonomous Health & Progress Monitoring
1. Schedule a non-intrusive periodic monitor via `schedule` (or turn transitions) to scan `<working_dir>/PROGRESS.md` and track liveness heartbeats (`Last visited: [timestamp]`).
2. Provide concise, factual progress summaries to the user without dumping raw logs into chat.

#### Responsibility 3: Environment Auditing & Execution Path Routing
1. Select execution path from the **Execution Paths & Routing Table**.
2. **Pre-Flight Dependency Audit (Blocking)**:
   - For General SWE, SWE Light, or Math runs requiring local toolchains, spawn **`teamwork-dependency-auditor`** ([agents/teamwork-dependency-auditor.md](agents/teamwork-dependency-auditor.md)).
   - On `READY`: Spawn the designated path Orchestrator.
   - On `MISSING`: Provide exact installation commands to the user and halt without installing packages.
   - On `OUTAGE`: Report infrastructure failure and halt.
3. **Spawn the Orchestrator**:
   - Dispatch the appropriate orchestrator persona (`teamwork-orchestrator`, `teamwork-swe-light`, `teamwork-doc-orchestrator`, `teamwork-proof-orchestrator`, or `teamwork-colosseum`).

#### Responsibility 4: Decoupled Victory Auditing & Binary Gate Verification
1. Treat all completion claims by the implementation team as uncertified hypotheses until independently verified in a fresh execution context.
2. Dispatch `teamwork-victory-auditor` ([agents/teamwork-victory-auditor.md](agents/teamwork-victory-auditor.md)) with clean context.
3. Enforce the blocking verdict:
   - **`VICTORY CONFIRMED`**: Every requirement `R1..Rn` and every acceptance criterion `- [ ]` in `ORIGINAL_REQUEST.md` has been independently executed and verified against real command output, with zero integrity violations. Present the final summary and deliverables to the user.
   - **`VICTORY REJECTED`**: Forward the full audit report back to the Orchestrator to resume remediation.

---

## Orchestrator & Team Operating Rules (All Paths)

Every Orchestrator and subagent in the team must obey these structural invariants (detailed in [references/orchestration-patterns.md](references/orchestration-patterns.md) and [references/verification-gates.md](references/verification-gates.md)):

1. **Structured Artifact Handoffs**:
   - `ORIGINAL_REQUEST.md`: Immutable user prompt, requirements, integrity mode, and acceptance criteria.
   - `PROJECT_PLAN.md`: Milestone roadmap, architecture contracts, workstream decomposition, and file-ownership assignments.
   - `PROGRESS.md`: Live status of every milestone, track, command output summary, and verification gate verdict.
   - `BRIEFING.md`: Concise working memory for clean successor handoffs (*"who am I, what is the current state, what is next"*).
2. **Exclusive File Ownership**:
   - When dispatching parallel `teamwork-worker` subagents in a milestone, assign an explicit, **disjoint list of owned files** to each worker. Two concurrent workers **MUST NEVER** edit the same file.
3. **Per-Agent Scratch Isolation**:
   - Every subagent receives its own scratch directory `<working_dir>/.teamwork/scratch/<agent_id>/` for temporary scripts, probe inputs, notes, and logs. Never litter the project root.
4. **The 16-Spawn Self-Succession Protocol**:
   - When cumulative subagent dispatches reach 16, persist all operational state into metadata files, write a self-contained soft handoff, terminate active crons, and spawn a fresh successor orchestrator with parent passthrough.
5. **Mandatory Adversarial Milestone Gates**:
   - No code milestone may be marked `COMPLETED` until it passes all three independent, fresh-context verification gates:
     1. **Critic (`teamwork-critic`)**: Reviews code correctness, completeness, interface conformance, and style (`APPROVE` / `REJECT`).
     2. **Challenger (`teamwork-challenger`)**: Authors and runs adversarial edge-case, boundary, failure-path, and stress tests (`SURVIVED` / `BROKEN`).
     3. **Auditor (`teamwork-auditor`)**: Enforces active `Integrity mode` and independently executes tests to confirm genuine execution with binary veto (`PASS` / `INTEGRITY VIOLATION`).

---

## Reference Manuals & Personas

- **Phase 1 Scoping Interview Guide**: [references/interview-protocol.md](references/interview-protocol.md)
- **Phase 2 Orchestration Patterns**: [references/orchestration-patterns.md](references/orchestration-patterns.md)
- **Adversarial Verification Gates & Testing Infrastructure**: [references/verification-gates.md](references/verification-gates.md)
- **Operational Protocols & Artifact Schemas**: [references/operational-protocols.md](references/operational-protocols.md)
- **Cross-Harness Subagent Delegation Guide**: [references/harness-delegation.md](references/harness-delegation.md)
- **Subagent Persona Definitions**:
  - [agents/teamwork-interviewer.md](agents/teamwork-interviewer.md)
  - [agents/teamwork-sentinel.md](agents/teamwork-sentinel.md)
  - [agents/teamwork-dependency-auditor.md](agents/teamwork-dependency-auditor.md)
  - [agents/teamwork-orchestrator.md](agents/teamwork-orchestrator.md)
  - [agents/teamwork-swe-light.md](agents/teamwork-swe-light.md)
  - [agents/teamwork-doc-orchestrator.md](agents/teamwork-doc-orchestrator.md)
  - [agents/teamwork-proof-orchestrator.md](agents/teamwork-proof-orchestrator.md)
  - [agents/teamwork-colosseum.md](agents/teamwork-colosseum.md)
  - [agents/teamwork-explorer.md](agents/teamwork-explorer.md)
  - [agents/teamwork-worker.md](agents/teamwork-worker.md)
  - [agents/teamwork-critic.md](agents/teamwork-critic.md)
  - [agents/teamwork-challenger.md](agents/teamwork-challenger.md)
  - [agents/teamwork-auditor.md](agents/teamwork-auditor.md)
  - [agents/teamwork-victory-auditor.md](agents/teamwork-victory-auditor.md)
