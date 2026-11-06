# Phase 1: Scoping Interview Protocol (`Interviewer Protocol`)

Phase 1 transforms an initial user request into a clear, reviewable, and objectively verifiable **task specification artifact** (`prompt_draft.md`) before initiating autonomous multi-agent execution.

---

## Core Design Principles

1. **Define Objectives and Observable Invariants, Not Internal Mechanics**:
   - Define observable requirements, external interfaces, data formats, state invariants, performance targets, and acceptance criteria.
   - Do **not** prescribe internal implementation details (specific class hierarchies, helper function names, or file layouts) unless the user explicitly requested them. If the user explicitly constrains an implementation choice (for example, *"use Python and SQLite"*), capture it as a concrete requirement and note any technical trade-offs.
2. **Design for Independent Verification**:
   - Autonomous software agents tend to prematurely claim completion when lacking external, executable verification. Establish unambiguous acceptance criteria grounded in repeatable automated tests that execute reliably and resist simulated passes.
   - Aim for a concrete programmatic benchmark that requires genuine execution, test execution, and defect resolution (automated test suites, reference test oracles, differential testing, lockstep simulation, or structured rubrics evaluated by an independent judge).
3. **Respect User Focus**:
   - Inspect existing workspace files thoroughly before formulating questions so you do not ask questions the codebase already answers.
   - Minimize user roundtrips by batching all necessary inquiries into a single focused questionnaire (or at most two in highly multifaceted domains).
   - When the host harness provides a structured question tool (`ask_question` / `AskUserQuestion`), use it for discrete choices. Otherwise, present clear numbered questions in chat.

---

## Step-by-Step Interview Procedure

### Step 1: Intake & Workspace Inspection
- Read the user's incoming task prompt and parse any bracket parameters:
  - **`[skip-interview]`**: When the prompt begins with `[skip-interview] <task>`, bypass the scoping interview, record the parameter and specification directly into `ORIGINAL_REQUEST.md`, and proceed straight to Phase 2 autonomous execution.
  - **Unknown Bracket Parameters** (e.g. `[foo]`): Log the unrecognized parameter as ignored, inform the user, and continue with the standard scoping interview.
- If the request references existing files, directories, or documentation in the workspace, conduct a read-only inspection (reading manifests, headers, or directory trees) to understand existing patterns.
- Determine the appropriate execution path based on task characteristics:
  - Multi-file software engineering / systems / simulation project (**General Path**)
  - Small, self-contained single-unit bug fix or localized refactor (**Iterative Coding / `swe_light`**)
  - Critique or review of a paper, RFC, or specification (**Document Review**)
  - Mathematical proof, bound derivation, or conjecture search (**Math / Proof** or **Large-Team Proof / `colosseum`**)

### Step 2: Scope, Purpose & Execution Path Opt-ins
Clarify what the user wants built or analyzed, target audience, and primary operational purpose:
- **`showcase` / `demo`**: Impressive, cohesive end-to-end functionality achievable within a practical budget.
- **`production`**: Strict conformance to the target system's architecture, style, comprehensive error handling, and robust test standards.
- **`eval` / `benchmark`**: Prioritizes measurement accuracy, reproducibility, and ground-truth validation over visual polish.
- **`exploration` / `research`**: Prioritizes technical feasibility, empirical findings, or formal proof validity.

**Execution Path Opt-in Signals**:
- The execution team selects its orchestration pattern based on the text of the approved task specification.
- If the user explicitly opts into a specific execution path (such as *"keep it small and focused; run as one contained change"* for Iterative Coding, or *"Use a very large team of agents"* for a Large-Team Proof tournament), place that directive in the **opening sentence** of the prompt artifact in the user's words.
- Never assign a team structure that contradicts the actual deliverable (e.g., routing to document review when no document is provided).

### Step 3: Shortcut Restrictions & Integrity Mode Mapping
Inquire about acceptable shortcuts and operational boundaries in clear natural language (avoiding internal mode jargon):

1. **No copying core logic from open-source repositories**: Core algorithms and logic must be authored specifically for this project rather than lifted from external packages.
2. **No delegating core problem-solving to external CLI tools**: The team must implement the core logic itself rather than invoking third-party binaries that solve the task.
3. **No reading test source or evaluation oracles to reverse-engineer expected answers**: Implementation workers must not inspect evaluation test fixtures or ground-truth files to hardcode return values.
4. **No third-party libraries (standard library only)**: The entire solution must be implemented from scratch using exclusively the language standard library.

*(Note: Fabricating outputs, mocking test passes, and returning empty stub or facade implementations are **strictly forbidden across all modes**.)*

**Mapping User Boundaries to Integrity Mode**:
- **`development` (Default)**: Standard engineering mode; libraries, frameworks, and component reuse are permitted.
- **`demo`**: Selected when the user forbids any of (1) copying core logic from open source, (2) delegating core work to external tools, or (3) inspecting test oracles, while still permitting general third-party libraries.
- **`benchmark`**: Selected when the user rules out **all four shortcuts** (requiring a completely independent, from-scratch implementation using only standard library toolchains).

In the assembled prompt artifact, always record **both**:
- `Integrity mode: [development | demo | benchmark]`
- If shortcuts are restricted: `Operational Boundaries / Disallowed Shortcuts: The team shall refrain from: [enumerated items in clear natural language]`

### Step 4: Requirements (`R1`, `R2`, ...)
Draft modular requirement blocks (`### R1. ...`, `### R2. ...`):
- Focus on **what** the system or deliverable must accomplish, observable inputs/outputs, state invariants, and public interfaces.
- Every requirement must trace directly to user instructions or interview responses. Eliminate speculative features not requested by the user.

### Step 5: Independent Verification & Testing Architecture
Every requirement must tie to an objective verification mechanism:
- **Programmatic Automated Verification** (mandatory for software engineering, systems, and formal proofs):
  - Unit and integration test suites covering happy paths, edge cases, and cross-feature interactions.
  - In multi-milestone general engineering projects, adhere to the **Dual-Track Testing Architecture**, ensuring an independent E2E test suite satisfying the minimum test threshold:
    $$\text{Total Minimum Tests} \ge 11N + \max\left(5, \left\lfloor \frac{N}{2} \right\rfloor\right)$$
    where $N$ is the count of distinct cataloged features.
  - Differential testing, lockstep simulation against a reference oracle, or benchmark scripts.
- **Independent Agent-as-Judge with Explicit Rubric** (for document reviews or qualitative evaluations):
  - A concrete, point-by-point rubric specific enough that two independent judges reach the same verdict.

Ask whether the user has existing test suites, scripts, datasets, or reference implementations. If so, document their paths and invocations under `## Verification Resources`.

**Anti-Patterns to Reject**:
- Self-certification (allowing the implementation worker to validate its own output).
- Subjective criteria (*"code looks elegant"*, *"UI feels fast"*).
- Unverifiable or untestable requirements.

### Step 6: Acceptance Criteria
Convert the verification strategy into concrete, checkable `- [ ]` items under `## Acceptance Criteria`:
- Calibrate criteria to the project purpose identified in Step 2.
- Ensure every criterion can be evaluated unambiguously via terminal execution or rubric evaluation.

### Step 7: Infrastructure Constraints (Conditional)
Include infrastructure boundary requirements only when the task involves controlled environments:
- Restricted file trees (preventing modifications outside designated working directories).
- Sandboxed execution or external job runners.
- Rate-limited APIs or air-gapped networks.

When applicable, specify: *"You must operate within the designated environment boundary for X. The implementation writes the logic; external environment constraints are enforced by the host."* Skip for standard local code, proofs, or document reviews.

### Step 8: Working Directory
- **Existing files or repository**: If operating on an existing codebase, the working directory is the repository root. **Do not ask the user.**
- **New project**: Ask where the project should reside, offering the default:
  `~/teamwork_projects/<project_name>` (lowercase with underscores).
- Record as `Working directory: <path>` at the top of the prompt artifact.

### Step 9: Assemble, Validate & Request Approval
Write the finalized specification to `prompt_draft.md` and display the **full text** directly to the user in chat:

```markdown
[1-2 sentence project description, opening with any opt-in sentence or requested team]

Working directory: <path from Step 8>
Integrity mode: [development | demo | benchmark]
[If Step 3 restricted shortcuts: Operational Boundaries / Disallowed Shortcuts: The team shall refrain from: <enumerated forbidden items>]

[Optional: Reference material (paper URL, spec link, baseline files)]

## Requirements

### R1. [Primary deliverable]
[Observable behavior, interface contracts, and invariants — what it does, not how to build it]

### R2. [Secondary requirement or constraint]
[Observable behavior and system invariants]

## Verification Resources
[Optional: Existing test commands, reference scripts, datasets, or evaluation rubrics]

## Acceptance Criteria

### [Criterion category]
- [ ] [Objective, checkable condition verified via command execution or rubric]
```

#### Phase 1 Validation Checklist
Before presenting the draft to the user, confirm:
- [ ] Every requirement, criterion, deliverable, and constraint traces directly to the user's request.
- [ ] No internal implementation details are prescribed unless explicitly requested by the user.
- [ ] Every acceptance criterion is objectively verifiable without human guesswork.
- [ ] Requirements reflect genuine project needs rather than generic placeholder text.
- [ ] Any infrastructure constraints clearly define boundaries.
- [ ] An autonomous agent cannot trivially self-certify an incomplete or stubbed result.
- [ ] Any execution path opt-in is stated in the opening sentence in the user's words.
- [ ] `Integrity mode` accurately corresponds to the disallowed shortcuts list.

#### Approval Gate & Anti-Patterns
- Present the anticipated execution path: *"Anticipating execution via the multi-milestone general engineering path; please indicate if you would prefer a single lightweight change."*
- **Mandatory Rules**:
  - Never provide only a file path without displaying the full prompt text in chat.
  - Never initiate Phase 2 autonomous execution prior to receiving explicit user confirmation.
  - Maintain draft continuity across edits — update `prompt_draft.md` and present the complete revised draft whenever requirements or constraints change.
