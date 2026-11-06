# Teamwork Framework Blueprint

## System Overview

Teamwork is an autonomous, harness-agnostic multi-agent orchestration framework designed for complex software engineering, large-scale systems simulation, rigorous technical document reviews, and formal mathematical proofs. Rather than overloading a single conversation context or permitting implementers to self-certify incomplete work, Teamwork organizes execution into two decoupled phases:

1. **Phase 1: Task Scoping & Specification (Scoping Interview)** — Clarifies project objectives (*what to build, not how to build it*), defines verifiable operational constraints, maps shortcut restrictions to an **Integrity Mode** (`development`, `demo`, or `benchmark`), establishes independent programmatic or rubric verification criteria, and outputs an approved specification (`ORIGINAL_REQUEST.md`).
2. **Phase 2: Autonomous Multi-Agent Execution** — A permanent custodian (**Sentinel**) runs pre-flight dependency audits, activates the specialized path **Orchestrator**, dispatches parallel **Explorers** and **Workers** under exclusive file ownership and per-agent scratch isolation, enforces mandatory adversarial milestone gates (**Critic**, **Challenger**, **Auditor**), and requires final validation by an independent **Victory Auditor** (`VICTORY CONFIRMED`).

---

## Architecture & Execution Paths

Teamwork routes incoming tasks into one of five specialized execution patterns based on deliverable scope, complexity, and domain:

| Execution Pattern | Target Orchestrator | Primary Use Case | Key Architectural Attributes |
| :--- | :--- | :--- | :--- |
| **1. Project Pattern** | `teamwork-orchestrator` | Multi-file SWE, greenfield systems, migrations, systems simulations | Phase 0 discovery (3 parallel scouts; Completeness > Consensus); Dual-track architecture (Implementation track M1..Mn concurrent with E2E Testing track satisfying $11N + \max(5, \lfloor N/2 \rfloor)$ minimum test formula); 6-step canonical milestone loop; self-succession at 16 spawns. |
| **2. SWE Light** | `teamwork-swe-light` | Compact, single-unit bug fixes or localized refactoring | 4 Hard Rules: Direct dispatch without over-decomposition; sequential refinement (Implementer $\rightarrow$ Reviewer 1 $\rightarrow$ Reviewer 2); verbatim task propagation; independent automated test verification. |
| **3. Document Review** | `teamwork-doc-orchestrator` | RFCs, research papers, and architectural specifications | Document triage into discrete segments; Random Sample Aggregation (RSA) review trees across orthogonal fresh-context reviewer lenses; Synthesis Group Orchestration; verbatim citation verification. |
| **4. Math / Proof** | `teamwork-proof-orchestrator` | Formal theorem proving, mathematical derivations | 5-phase outer loop (Exploration, Lemma Decomposition, Subproblem Solving, Verification, Revision); layer tournament tree delegation with paired solvers and falsers. |
| **5. Swarm (Colosseum)** | `teamwork-colosseum` | Hard open conjectures, combinatorial search | Shared blackboard (`BLACKBOARD.md`) tournament waves of parallel solvers and falsers converging on mathematical ground truth. |

### Verification & Adversarial Gate Triad

Every milestone across engineering execution paths must pass three independent, fresh-context verification gates before progression is permitted:

1. **Critic (`teamwork-critic`)**: Reviews code architecture, completeness, interface conformance, and style conventions (`APPROVE` / `REJECT`).
2. **Challenger (`teamwork-challenger`)**: Authors and runs adversarial edge-case, boundary, stress, and regression suites (`SURVIVED` / `BROKEN`).
3. **Auditor (`teamwork-auditor`)**: Audits against the active **Integrity Mode** (`development`, `demo`, `benchmark`) and independently executes tests to confirm genuine execution with binary veto (`PASS` / `INTEGRITY VIOLATION`).

Composite milestone approval requires a strict logical conjunction (`Critic AND Challenger AND Auditor`). Final completion across the entire project is gated on an independent **Victory Auditor** (`teamwork-victory-auditor`) verifying every requirement and acceptance criterion against live command outputs.

---

## Subdirectories & System Boundaries

- **[`scripts/README.md`](scripts/README.md)**: Tooling contract for synchronization, frontmatter validation, markdown link verification, and clean-room policy enforcement via `sync_and_validate.py`.
- **[`examples/README.md`](examples/README.md)**: Reference walkthroughs and execution traces, including an end-to-end distributed key-value storage engine case study under the Project Pattern.
- **[`resources/templates/`](resources/templates/)**: Standard operational artifact templates (`briefing.md`, `dead_ends.md`, `gate_status.md`, `progress.md`, `project.md`, `scope.md`, `test_infra.md`, `test_ready.md`).
- **[`references/`](references/)**: Progressive-disclosure protocol manuals and specifications:
  - [`references/interview-protocol.md`](references/interview-protocol.md): 9-step scoping interview, intake triage, integrity mode mapping, and prompt crafting.
  - [`references/orchestration-patterns.md`](references/orchestration-patterns.md): Detailed mechanics for all 5 execution patterns, dual-track testing, and swarm DAGs.
  - [`references/verification-gates.md`](references/verification-gates.md): Adversarial gates (Critic, Challenger, Auditor), testing infrastructure, and integrity mode enforcement.
  - [`references/operational-protocols.md`](references/operational-protocols.md): 5-component handoff, 3-step state recovery, 16-spawn self-succession, heartbeat and liveness monitoring.
  - [`references/harness-delegation.md`](references/harness-delegation.md): Cross-harness mapping for subagent spawning, communication, and scheduling.
- **[`agents/`](agents/)**: Canonical subagent persona definitions for all 14 team roles.
- **[`skills/teamwork/`](skills/teamwork/SKILL.md)**: Generated self-contained portable distribution bundle synchronized by repository automation.

---

## Multi-Harness Installation

This repository supports both **direct skill directory installation** (using root `SKILL.md` or `skills/teamwork/`) and **native plugin installation**.

### 1. Claude Code

**Option A — Standalone Skill (User or Project Scope)**:
```bash
# User-wide skill (/teamwork)
mkdir -p ~/.claude/skills/teamwork
cp -R SKILL.md references agents resources examples ~/.claude/skills/teamwork/

# Or project-scoped skill
mkdir -p .claude/skills/teamwork
cp -R SKILL.md references agents resources examples .claude/skills/teamwork/
```

**Option B — Local Plugin Directory**:
```bash
claude --plugin-dir /path/to/teamwork
```

### 2. OpenAI Codex

**Option A — Standalone Skill**:
```bash
mkdir -p ~/.codex/skills/teamwork
cp -R SKILL.md references agents resources examples ~/.codex/skills/teamwork/
```

**Option B — Workspace `.agents/skills/`**:
```bash
mkdir -p .agents/skills/teamwork
cp -R SKILL.md references agents resources examples .agents/skills/teamwork/
```

### 3. Native Tool Harness / CLI

**Option A — User Configuration Directory**:
```bash
# User-wide skill installation
mkdir -p ~/.config/agent-skills/teamwork
cp -R SKILL.md references agents resources examples ~/.config/agent-skills/teamwork/
```

**Option B — Standard Plugin Registration**:
```bash
# Register plugin directory or plugin.json directly with your agent runtime
agent-cli plugin install /path/to/teamwork
```

**Option C — Workspace Skill Directory**:
```bash
mkdir -p .agents/skills/teamwork
cp -R SKILL.md references agents resources examples .agents/skills/teamwork/
```

### 4. Cursor / Windsurf / Other Harnesses

Copy `SKILL.md`, `references/`, `agents/`, `resources/`, and `examples/` into your harness skill discovery directory (e.g., `.agents/skills/teamwork/`), or reference `SKILL.md` directly from your environment configuration (`AGENTS.md` / `CLAUDE.md`).

---

## Global Invariants

- **Two-Phase Enforcement**: Phase 1 (Scoping Interview) must conclude with explicit user approval of `prompt_draft.md` before Phase 2 (Autonomous Execution) can begin.
- **Exclusive File Ownership**: Concurrent workers within a milestone must never edit overlapping files. File allocations in `PROJECT_PLAN.md` are strictly disjoint.
- **Metadata Workspace Isolation**: Agent working files, handoffs, and briefings must reside only in `.agents/teamwork/<agent_id>/`. Production code and tests must never be placed in metadata directories. Taboo filenames (`AGENTS.md`, `GEMINI.md`) must never be created.
- **Per-Agent Scratch Isolation**: Ephemeral test scripts, exploratory probes, and execution logs must be isolated in `<working_dir>/.teamwork/scratch/<agent_id>/`.
- **Adversarial Gate Triad**: Every implementation milestone must secure independent affirmative verdicts from Critic (`APPROVE`), Challenger (`SURVIVED`), and Auditor (`PASS`). Composite milestone pass requires strict logical AND.
- **Integrity Mode Conformance**: Subagents strictly adhere to the designated integrity mode (`development`, `demo`, or `benchmark`). The Auditor exercises a binary veto on mocks, faked passes, unauthorized tool delegation, or oracle peeking.
- **Self-Succession at 16 Spawns**: When cumulative subagent dispatches reach 16, orchestrators must serialize operational state and execute a clean soft handoff to a fresh-context successor.
- **Decoupled Victory Audit**: Implementers are prohibited from self-certifying completion. Final delivery requires an independent `teamwork-victory-auditor` running in a fresh context to confirm 100% requirement and acceptance criteria verification.

---

## Global Side Effects

- **Local Filesystem State**: Creates project specification and tracking files (`ORIGINAL_REQUEST.md`, `PROJECT_PLAN.md`, `PROGRESS.md`, `GATE_STATUS.md`, `TEST_INFRA.md`, `TEST_READY.md`) in the workspace, maintains metadata in `.agents/teamwork/`, and isolates temporary scripts in `.teamwork/scratch/`.
- **Automated Code and Test Modifications**: Modifies source files and writes automated test suites strictly within assigned file ownership boundaries.
- **Subprocess Execution**: Invokes build tools, compilers, test runners, and linters (e.g., `pytest`, `cargo test`, `npm test`, `go test`, `make test`) as specified by project configurations.
- **Repository Asset Synchronization**: Executes `python3 scripts/sync_and_validate.py` to mirror assets into `skills/teamwork/` and validate manifests and links.
- **Subagent Lifecycle Management**: Dispatches child agent sessions with fresh context windows and sends point-to-point coordinating messages.

---

## System Verification

Run the validation and sync script to mirror assets and verify manifests, frontmatter, links, and clean-room policy compliance:

```bash
python3 scripts/sync_and_validate.py
```
