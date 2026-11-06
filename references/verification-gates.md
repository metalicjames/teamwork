# Adversarial Verification Gates & Testing Infrastructure

Teamwork prevents premature self-certification by requiring candidate changes and final deliverables to pass independent, fresh-context verification gates before any milestone or project is approved.

---

## 1. Core Verification Invariants

1. **Fresh Context Isolation**:
   - Every gate agent (`Critic`, `Challenger`, `Auditor`, `Victory Auditor`) **MUST** be spawned as a fresh subagent with zero shared conversation history from the implementing Worker.
   - Never reuse a subagent after it has delivered its handoff report. If a milestone requires remediation, spawn **brand-new** gate subagents for the subsequent verification pass.
2. **Evidence Over Assertions**:
   - An implementer's assertion that *"all tests pass"* is not evidence.
   - Auditors and Victory Auditors must invoke verification commands directly in the workspace shell, inspecting raw exit codes, stdout/stderr streams, and output artifacts.
3. **Strict Separation of Evaluation and Modification**:
   - Gate reviewers (`Critic`, `Challenger`, `Auditor`, `Victory Auditor`) and Orchestrators **MUST NOT** edit production source code or test files to resolve defects. They report exact findings with `path/to/file:line` citations and reproduction scripts so the Orchestrator can assign remediation to a Worker.

---

## 2. Dual-Track Testing Architecture & The 4-Tier Formula

In the Project Pattern, the **E2E Testing Track** executes concurrently with the **Implementation Track**. Governed by an independent test orchestrator or test writers (`teamwork-test-writer`), tests are derived strictly from `ORIGINAL_REQUEST.md` and `PROJECT_PLAN.md § Feature Inventory`. The implementation is treated as an opaque black box to prevent co-dependent test bias.

### The 4-Tier Test Suite Specification
Given $N$ distinct functional features cataloged in `PROJECT_PLAN.md § Feature Inventory`:

| Tier | Category | Minimum Test Count Formula | Scope & Purpose |
| :--- | :--- | :---: | :--- |
| **Tier 1** | Feature Coverage | $5 \times N$ | Core functional paths, happy paths, and valid input domains for every cataloged feature. |
| **Tier 2** | Boundary & Corner Cases | $5 \times N$ | Empty collections, zero/null values, max/min bounds, malformed encodings, boundary transitions. |
| **Tier 3** | Cross-Feature Combinations | $1 \times N$ | Multi-step workflows, feature interactions, and state machine lifecycle transitions. |
| **Tier 4** | Real-World Application Scenarios | $\max(5, \lfloor N/2 \rfloor)$ | Realistic end-to-end user workflows, long-running simulations, system load, failure recovery. |

### Total Minimum Test Count Formula:
$$\text{Total Minimum Tests} = 5N + 5N + N + \max\left(5, \left\lfloor \frac{N}{2} \right\rfloor\right) = 11N + \max\left(5, \left\lfloor \frac{N}{2} \right\rfloor\right)$$

### Testing State Signals: `TEST_INFRA.md` & `TEST_READY.md`
- **`<working_dir>/TEST_INFRA.md`**: Maintained by the E2E Testing Track. Specifies:
  1. Test Philosophy & Isolation Guarantees.
  2. Feature Inventory Mapping (feature ID to test files).
  3. Tier Coverage Breakdown ($5N, 5N, N, \max(5, \lfloor N/2 \rfloor)$).
  4. Test Runner Invocations & Environment Setup.
- **`<working_dir>/TEST_READY.md`**: Published at the project root once the E2E test suite is fully authored and verified against stubs. Contains:
  1. Canonical test execution command.
  2. Feature-to-test verification matrix.
  3. Timestamp and readiness certification.

During the final project milestone, the Orchestrator polls for `TEST_READY.md` before initiating final acceptance execution.

---

## 3. Milestone Gate Specifications (Gates 1–3)

### Gate 1: Critic (`teamwork-critic`)
- **Role**: Independent Code & Architecture Reviewer ([../agents/teamwork-critic.md](../agents/teamwork-critic.md)).
- **Evaluation Criteria**:
  1. **Correctness & Completeness**: Logical completeness across all assigned requirements with zero placeholder stubs.
  2. **Robustness & Error Handling**: Graceful error propagation, resource release, and boundary checks.
  3. **Interface Conformance**: Strict alignment with contracts in `PROJECT_PLAN.md`.
  4. **Code Quality**: Maintainability, idiomatic style, and absence of debugging artifacts.
- **Verdicts**:
  - **`APPROVE`**: Zero `Blocker` or `Major` findings.
  - **`REJECT`**: One or more `Blocker` or `Major` defects identified, with `file:line` locations and required fixes.

### Gate 2: Challenger (`teamwork-challenger`)
- **Role**: Adversarial Stress Tester & Falser ([../agents/teamwork-challenger.md](../agents/teamwork-challenger.md)).
- **Empirical Reproduction Guarantee**: Theoretical defects without executable reproduction scripts are invalid. Every challenge must include an executable probe demonstrating failure.
- **Probe Vectors**:
  - Boundary and degenerate inputs (empty payloads, zero bounds, extreme ranges).
  - Race conditions, concurrent access hazards, and resource exhaustion limits.
  - Pathological algorithmic inputs and failure-path injections.
  - Mathematical counterexample sweeps (for Proof paths).
- **Verdicts**:
  - **`SURVIVED`**: All adversarial probes executed without triggering unhandled failures or contract breaks.
  - **`BROKEN`**: At least one probe triggered a crash, contract violation, resource leak, or valid counterexample.

### Gate 3: Forensic Integrity Auditor (`teamwork-auditor`)
- **Role**: Multi-Mode Integrity & Ground-Truth Test Verifier ([../agents/teamwork-auditor.md](../agents/teamwork-auditor.md)).
- **Integrity Tier Checks**:
  1. **Universal Invariants (All Modes: `development`, `demo`, `benchmark`)**:
     - Reject fabricated outputs, lookup-table cheats, or hardcoded return constants.
     - Reject incomplete stubs, empty functions, or placeholder markers (`TODO`, `FIXME`, `unimplemented!`, `NotImplementedError`).
     - Reject bypassed assertions, skipped tests (`#[ignore]`, `.skip`), or tests mocking the primary system under test.
  2. **`demo` and `benchmark` Invariants**:
     - Reject core logic lifted from external repositories.
     - Reject delegating core problem-solving logic to external CLI tools or subprocesses.
     - Reject code designed to parse evaluation test files or reverse-engineer test fixtures.
  3. **`benchmark` Invariants**:
     - Enforce standard library exclusive implementation (zero third-party dependencies in production manifests or code).
- **Binary Gate Verdict**:
  Exhaustively audit every codebase artifact, dependency, and test result under the active integrity tier. If any non-compliant pattern, stubbed routine, or mocked test pass is detected, immediately issue an **`INTEGRITY VIOLATION`** verdict, which acts as a non-negotiable blocking veto on milestone acceptance.
  - **`PASS`**: All integrity checks and independent test executions pass cleanly.
  - **`INTEGRITY VIOLATION`**: Non-compliant code pattern, stub, or test cheat detected.

---

## 4. Gate 4: Final Victory Auditor (`teamwork-victory-auditor`)

Dispatched exclusively by **Project Sentinel** in a fresh context when the Orchestrator reports project completion.

### 3-Phase Victory Audit Procedure:
1. **Phase A — Request & Timeline Traceability**:
   - Ingest `<working_dir>/ORIGINAL_REQUEST.md`.
   - Verify that every requirement (`R1..Rn`) and acceptance criterion (`- [ ]`) traces through the implementation without omission.
2. **Phase B — Forensic Integrity Audit**:
   - Execute full Gate 3 integrity review across all files, checking for stubs, forbidden dependencies, or oracle peeking under the active `Integrity mode`.
   - Validate workspace hygiene (zero temporary files or debug artifacts in root).
3. **Phase C — Autonomous Ground-Truth Execution**:
   - Independently run the full compilation, test suite, and benchmark suites in the workspace shell.
   - For **Document Review** tasks: verify that every quotation, line number, equation, and figure reference exists verbatim in the source document.
   - For **Math / Proof** tasks: verify that the lemma dependency graph is acyclic, all hypotheses match conclusions, and proofs compile without errors.
- **Blocking Final Verdict**:
  - **`VICTORY CONFIRMED`**: All requirements, criteria, and integrity rules verified through live execution.
  - **`VICTORY REJECTED`**: Any failure or integrity defect triggers immediate rejection and return to remediation.

---

## 5. Destruction & Safety Vetting (`vet_destruction`)

To prevent catastrophic workspace damage during autonomous execution, destructive shell commands are evaluated against safety policies:

1. **Decomposition of Compound Pipelines**:
   Commands combining operations (`&&`, `;`, `|`, `||`) are decomposed into atomic invocations and analyzed individually.
2. **Evaluation Invariants**:
   - Inspect commands for unintended file deletions (`rm -rf /`, wildcards outside scratch directories).
   - Inspect for unauthorized git history rewrites (`git reset --hard` destroying uncommitted user work) or force pushes.
   - Inspect for process killing affecting processes outside assigned subagent task IDs.
3. **Default Policy**:
   - Default determination is **`ALLOW`**.
   - Issue **`DENY`** only upon identifying concrete, named destructive consequences to project assets or host environments.
