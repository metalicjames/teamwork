# Cross-Harness Subagent Delegation Guide

Teamwork is an autonomous, harness-agnostic multi-agent framework designed to operate consistently across diverse agent environments. Its core operational guarantees—fresh-context subagent isolation, strict role specialization, exclusive file ownership, and adversarial verification gates—adapt cleanly to any host platform that supports subagents or multi-turn task delegation.

Follow the guidance below for your active host environment.

---

## 1. Subagent-Native & Hierarchical Agent Harnesses

Environments with built-in hierarchical subagent primitives (such as platforms providing `invoke_subagent`, `define_subagent`, `schedule`, `manage_task`, and `send_message`) provide the highest degree of autonomy and concurrency.

### Core Tool Mapping
- **Subagent Invocation**: `invoke_subagent` (specifying `TypeName`, `Role`, `Prompt`, and optional `TimerCondition`).
- **Dynamic Persona Definition**: `define_subagent` (registering persona prompts, tool restrictions, and roles).
- **Inter-Agent Messaging**: `send_message` (delivering concise state updates and handoff notifications).
- **Periodic Heartbeats & Monitoring**: `schedule` (running recurring cron jobs, e.g. `*/8 * * * *`).
- **Schedule Lifecycle**: `manage_task` (cancelling monitors or aborting unresponsive tasks).
- **Interactive Scoping**: `ask_question` (for structured discrete user choices during Phase 1) or conversational turns for open-ended discussion.

### Persona Discovery & Registration
Host platforms discover Teamwork subagent personas in one of three ways:
1. **Automatic Directory Registration**: When installed as a plugin or skill, the platform scans `agents/teamwork-*.md` and registers each persona by its YAML frontmatter `name` (`teamwork-sentinel`, `teamwork-interviewer`, `teamwork-orchestrator`, `teamwork-swe-light`, `teamwork-doc-orchestrator`, `teamwork-proof-orchestrator`, `teamwork-colosseum`, `teamwork-explorer`, `teamwork-worker`, `teamwork-critic`, `teamwork-challenger`, `teamwork-auditor`, `teamwork-victory-auditor`, `teamwork-dependency-auditor`).
2. **Dynamic Runtime Registration (`define_subagent`)**: If personas are not pre-registered in the host catalog, the coordinator calls `define_subagent` using the `name`, `description`, and body of `agents/<persona>.md`:
   - **Read-Only Personas (`EnableWriteTools: false`)**: `teamwork-explorer`, `teamwork-critic`, `teamwork-interviewer`, `teamwork-dependency-auditor`.
   - **Armed Implementers & Probers (`EnableWriteTools: true`)**: `teamwork-worker`, `teamwork-challenger`, `teamwork-auditor`, `teamwork-victory-auditor`.
3. **General-Purpose Subagent Fallback**: If dynamic definition is unavailable, invoke the platform's general subagent persona and instruct it at the very top of `Prompt` to read the absolute path to `agents/<persona>.md` before taking action.

### Hierarchical Nesting & Concurrency
- Platforms supporting nested subagent trees allow the canonical two-phase hierarchy:
  `Sentinel` (top level) -> `Orchestrator` -> `Workers` (parallel implementation) & `Gate Reviewers` (Critic, Challenger, Auditor).
- Supported up to 10 nesting levels. When orchestrator spawn count reaches 16, execute self-succession with a soft handoff to prevent context exhaustion.

### Liveness & Heartbeat Deadlines
- The coordinator registers a background heartbeat check via `schedule` (`CronExpression: "*/8 * * * *"`).
- Every active subagent maintains a heartbeat in its `<working_dir>/.agents/teamwork/<subagent_id>/progress.md` containing `Last visited: [timestamp]`.
- **10-Minute Check**: Inspect subagent `progress.md`. If no progress or state change is observed, issue a status query.
- **20-Minute Hard Deadline**: If a worker or reviewer remains completely unresponsive for 20 minutes, treat as hung, terminate via `manage_task`, and spawn a fresh replacement. Cancel background schedules via `manage_task` upon project victory confirmation.

---

## 2. Claude Code & Claude Cowork

Claude environments run Teamwork through the `Agent` (`Task`) subagent tool.

### Persona Resolution
- **Plugin Installation**: When installed via `.claude-plugin/plugin.json`, Claude Code discovers the skill via `"skills": "./skills/"` (exposing `skills/teamwork/SKILL.md` and bundled personas in `skills/teamwork/agents/`).
- **Standalone Skill Installation**: When installed in `.claude/skills/teamwork/` or `~/.claude/skills/teamwork/`, personas reside in `agents/teamwork-*.md`.
- **Agent Invocation Pattern**: Spawn a fresh `Agent` and instruct it at the start of its prompt:
  > *"Adopt the role defined in `<skill_dir>/agents/<persona>.md`. You are acting as `<persona_name>` for Milestone `<M>`. Read `<working_dir>/ORIGINAL_REQUEST.md` and `<working_dir>/BRIEFING.md`. Follow all role constraints strictly. Your assignment: <task description>."*

### Nesting & Topology
- **Claude Code**: Supports multi-level nested subagents (up to 3 levels). The top-level thread acts as `Sentinel`, spawning `teamwork-orchestrator`, which in turn spawns `teamwork-worker`, `teamwork-critic`, `teamwork-challenger`, and `teamwork-auditor`.
- **Claude Cowork / Single-Depth Hosts**: Subagents cannot spawn child subagents. In this topology:
  1. The primary thread combines **Sentinel + Orchestrator** functions.
  2. Dispatches all subagents (`teamwork-explorer`, `teamwork-worker`, `teamwork-critic`, `teamwork-challenger`, `teamwork-auditor`, `teamwork-victory-auditor`) directly as flat depth-1 subagents.
  3. Uses filesystem artifacts in `<working_dir>/.agents/teamwork/` as explicit state transitions.

### Inviolable Context Isolation
- **Gate Independence**: Always launch a **brand new** `Agent` invocation for each Critic, Challenger, Auditor, and Victory Auditor.
- **No Conversation Reuse**: Never resume or fork an implementer's conversation thread for a verification gate. Reusing context blinds reviewers to omission errors and invalidates the adversarial guarantee.

---

## 3. OpenAI Codex & ChatGPT Work

OpenAI and Codex environments provide subagent execution through tools such as `spawn_agent`, `send_message`, and `wait`.

### Fresh Context Isolation (Mandatory)
- Whenever `spawn_agent` accepts context parameters, explicitly enforce fresh context:
  - `fork_context: false`
  - `fork_turns: "none"`
- Never copy previous conversation turns or deliberation logs into the reviewer's prompt. Reviewers must evaluate code artifacts objectively from disk.

### State Transfer via Filesystem
Pass references to filesystem artifacts rather than multi-kilobyte prompt transcripts:
- Role Persona: `<skill_dir>/agents/<persona>.md`
- Verbatim User Objective: `<working_dir>/ORIGINAL_REQUEST.md`
- Project Plan & Roadmap: `<working_dir>/PROJECT.md`
- Agent Workspace: `<working_dir>/.agents/teamwork/<subagent_id>/`

### Topology Handling
If the host platform prevents subagents from spawning subagents, run Sentinel and Orchestrator logic in the primary session, dispatching parallel worker and reviewer waves at depth 1.

---

## 4. Cursor, Windsurf, OpenCode, omp & Other Agent Harnesses

Environments supporting task or subagent tools (such as `task` in omp or native background tasks in Cursor/Windsurf) execute Teamwork using standard filesystem conventions.

### Named vs. Generic Dispatch
- If the harness registers custom agent personas from `agents/*.md`, invoke them directly by name.
- Otherwise, launch a general-purpose agent in a clean session, passing the absolute path to `agents/<persona>.md` as the first instruction.

### Fallback for Single-Session Environments (No Subagent Primitive)
If a developer runs Teamwork in an agent environment that lacks any subagent or background task tool:
1. **User Notification**: Warn the user before commencing Phase 2 that physical context isolation is unavailable, and adversarial gates will be executed sequentially within the main thread.
2. **Explicit State Checkpoints**: Strictly compartmentalize roles across sequential turns:
   - Worker writes changes and publishes `<working_dir>/.agents/teamwork/worker_1/handoff.md`.
   - The coordinator resets mental context, reads `agents/teamwork-critic.md`, inspects the diff objectively, and writes `handoff.md`.
   - The coordinator adopts `agents/teamwork-challenger.md` and runs adversarial reproduction probes.
   - The coordinator adopts `agents/teamwork-auditor.md` and validates integrity mode compliance.
3. This sequential discipline preserves structured artifacts even when process-level context separation cannot be enforced by the host.

---

## 5. Unified Cross-Harness Capability Matrix

| Feature / Capability | Subagent-Native Harnesses | Claude Code / Cowork | OpenAI Codex / Work | Cursor / omp / Other | Single-Session Fallback |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Subagent Tool** | `invoke_subagent` | `Agent` (`Task`) | `spawn_agent` | Native `task` / subagent | None (sequential main thread) |
| **Persona Registration** | Pre-registered or `define_subagent` | `./skills/` or prompt path | Prompt path (`agents/*.md`) | Prompt path (`agents/*.md`) | Prompt role transition |
| **Context Isolation** | Hardware / session isolation | New `Agent` call | `fork_context: false` | Fresh task context | Artifact-based discipline |
| **Max Nesting Depth** | 10 levels | 3 levels (Code) / 1 (Cowork) | 1 to 2 levels | 1 level | 0 (flat session) |
| **Background Heartbeat** | `schedule` (`CronExpression`) | Turn-based polling | Turn-based polling | Native timers / polling | Turn-based polling |
| **Liveness Deadline** | 10 min query / 20 min timeout | 10 min / 20 min rule | 10 min / 20 min rule | 10 min / 20 min rule | Manual user supervision |
| **Interactive Scoping** | `ask_question` / chat | `AskUserQuestion` / chat | User question tool / chat | Chat turns | Chat turns |
