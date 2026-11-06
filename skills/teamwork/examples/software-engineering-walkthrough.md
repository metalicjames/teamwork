# Multi-Agent Software Engineering Walkthrough: TitanKV Storage Engine

This walkthrough provides a concrete, end-to-end case study of an autonomous multi-agent team implementing **TitanKV**, an embedded key-value storage engine with Write-Ahead Logging (WAL), an in-memory Memtable, SSTable flushing, and an HTTP REST interface.

The project demonstrates:
1. **Phase 1 Scoping Interview & Request Formalization**
2. **Phase 2 Routing & Pre-Flight Environment Verification**
3. **Phase 0 Reconnaissance Survey (Completeness > Consensus)**
4. **Dual-Track Decomposition (Implementation Track + E2E Testing Track)**
5. **The 6-Step Canonical Iteration Loop with Adversarial Verification Gates**
6. **Oscillation Guard Enforcement via `DEAD_ENDS.md`**
7. **The 16-Spawn Self-Succession Protocol**
8. **Final E2E Acceptance & 3-Phase Forensic Victory Audit**

---

## 1. Phase 1: Intake & Scoping Interview

### 1.1 User Prompt Intake
The user initiates the task with a concise request:
> *"Build an embedded key-value storage engine in Python that supports crash recovery, atomic write-ahead logging, background SSTable disk flushing, and a lightweight HTTP REST API."*

### 1.2 Scoping Questionnaire
`teamwork-interviewer` parses the request, inspects the empty workspace, and presents a focused 3-question questionnaire:
1. **Target Purpose & Integrity Mode**: Is this intended for production, demonstration, or benchmark validation?
   - *User selects*: `development` (permits standard Python libraries and standard ecosystem tools).
2. **Concurrency & Durability Invariants**: Should writes block on disk sync (`fsync`), or operate asynchronously with periodic flush?
   - *User specifies*: Synchronous `fsync` on commit for guaranteed crash recovery.
3. **Interface Scope**: Should HTTP endpoints include batch operations (`mget`, `mset`) or single-key CRUD?
   - *User specifies*: Standard CRUD (`GET`, `PUT`, `DELETE /keys/<key>`) plus a health check endpoint (`GET /health`).

### 1.3 Authoritative Request Artifact
The interviewer records the agreed specification into `ORIGINAL_REQUEST.md`:

```markdown
# Original User Request — TitanKV Storage Engine

Working directory: /workspace/titankv
Integrity mode: development

## Requirements
### R1. Write-Ahead Logging (WAL)
Append-only binary log recording record length, CRC32 checksum, operation type, key, and value. Must support crash recovery playback.
### R2. In-Memory Memtable
Concurrent skiplist or sorted structure supporting O(log N) lookups, point mutations, and range scans.
### R3. SSTable Disk Flusher
Background immutable disk format with index block, data block, and bloom filter.
### R4. HTTP REST API
HTTP service providing GET, PUT, DELETE for keys and GET /health.

## Acceptance Criteria
- [ ] 100% crash recovery replay integrity verified across simulated unexpected terminations.
- [ ] Concurrent writes maintain serializable order without data corruption.
- [ ] Independent E2E test suite passes 100%.
```

---

## 2. Phase 2: Routing & Pre-Flight Verification

The top-level **Project Sentinel** evaluates `ORIGINAL_REQUEST.md`:
- Multi-component software engineering task requiring multiple files, concurrent work tracks, and rigorous testing.
- No single-file opt-in directive present.
- **Routing Decision**: Route to **Pattern 1: Project Pattern** (`teamwork-orchestrator`).

Sentinel conducts pre-flight checks:
- Python 3.10+ available (`python3 --version`).
- `pytest` installed.
- Shell write permissions confirmed.

Sentinel launches `teamwork-orchestrator` and provides `ORIGINAL_REQUEST.md`.

---

## 3. Phase 0: Survey Stage (Completeness > Consensus)

The Orchestrator dispatches 3 read-only Explorers in parallel:
- **Explorer 1**: Analyzes WAL binary framing, record checksumming, and crash recovery mechanics.
- **Explorer 2**: Researches concurrency primitives, lock-free structures, and SSTable disk layout.
- **Explorer 3**: Evaluates HTTP server libraries, routing protocols, and packaging.

### Orchestrator Synthesis: `PROJECT_PLAN.md`
The Orchestrator aggregates explorer findings adhering to **Completeness > Consensus** (unique observations with concrete citations are preserved):
- **Feature Inventory ($N = 4$)**:
  - `F-001`: Write-Ahead Log (WAL) Engine
  - `F-002`: In-Memory Memtable Engine
  - `F-003`: SSTable Disk Storage & Flusher
  - `F-004`: HTTP REST API Service
- **4-Tier E2E Testing Target**:
  $$\text{Total Tests} = 11(4) + \max(5, \lfloor 4/2 \rfloor) = 44 + 5 = \mathbf{49\text{ tests}}$$
- **Milestone Decomposition**:
  - `M1`: Core Storage Engine (WAL & Memtable)
  - `M2`: SSTable Disk Flusher & Compaction
  - `M3`: HTTP REST API & Final E2E Integration

---

## 4. Dual-Track Launch

The Orchestrator immediately launches both tracks in parallel:
1. **Implementation Track**: Dispatches `teamwork-worker-1` to begin Milestone 1.
2. **E2E Testing Track**: Dispatches `teamwork-test-writer` to author `TEST_INFRA.md` and the 49-test black-box suite derived strictly from `ORIGINAL_REQUEST.md`.

---

## 5. Milestone 1 Iteration Loop & Verification Gates

### 5.1 Step a & b: Assess & Explore
`teamwork-worker-1` reviews `ORIGINAL_REQUEST.md` and `PROJECT_PLAN.md`, establishing its exclusive file ownership boundary:
- Write paths: `src/titankv/wal.py`, `src/titankv/memtable.py`, `tests/unit/test_wal.py`

### 5.2 Step c: Implement & Local Verification
The worker implements the WAL record structure using standard `struct.pack` and CRC32 checksums.
Worker runs local unit tests:
```bash
pytest tests/unit/test_wal.py -v
# Result: 8 passed in 0.24s
```
Worker compiles its 5-component `handoff.md` and notifies the Orchestrator.

### 5.3 Step d: Gate 1 (Critic) & Gate 2 (Challenger) Review
The Orchestrator spawns fresh, isolated verification subagents:

#### Gate 1: Critic (`teamwork-critic`)
- Inspects `src/titankv/wal.py` for correctness, error handling, and style.
- Verdict: **`APPROVE`** (0 Blockers, 0 Majors, 1 Nit: suggest adding docstring type hints).

#### Gate 2: Challenger (`teamwork-challenger`)
- Authors adversarial probe `probes/probe_wal_crash.py` simulating ungraceful process kills during midway record writing.
- **Empirical Failure**: Truncated records without padding trigger an unhandled `ValueError` rather than clean recovery to the last valid transaction!
- Verdict: **`BROKEN`** with executable reproduction script.

### 5.4 Remediation & Re-Verification
1. Orchestrator records Gate Status: `REMEDIATION_REQUIRED`.
2. Worker updates WAL recovery parser to handle truncated tail records gracefully, discarding incomplete transactions safely.
3. Fresh Challenger re-executes probe:
   ```bash
   python3 probes/probe_wal_crash.py
   # Output: PASSED — Clean recovery across 50 simulated crash points.
   ```
   Verdict: **`SURVIVED`**.

### 5.5 Step e: Gate 3 (Auditor) Forensic Review
Fresh `teamwork-auditor` executes Gate 3:
- Checks for stubs (`TODO`, `NotImplementedError`, empty passes): None found.
- Verifies integrity mode compliance: Standard library used, zero mocked assertions.
- Executes test suite directly in shell:
  ```bash
  pytest tests/unit/ -v
  # Output: 14 passed in 0.38s (Exit code: 0)
  ```
- Verdict: **`PASS`**.

### 5.6 Step f: Gate Evaluation
Orchestrator computes composite verdict:
$$\text{Pass} = \text{Build Pass} \land (\text{Critic} == \text{APPROVE}) \land (\text{Challenger} == \text{SURVIVED}) \land (\text{Auditor} == \text{PASS}) = \mathbf{PASS}$$
Milestone 1 is certified and merged.

---

## 6. Anti-Degradation in Action

### 6.1 Oscillation Guard (`DEAD_ENDS.md`)
During Milestone 2 (SSTable Compaction), a worker attempts an in-place file rewrite strategy that fails twice due to concurrent read lock deadlocks.
- Orchestrator halts the worker.
- Logs entry `DE-001` in `DEAD_ENDS.md`:
  - Failed Strategy: In-place file modification during active reads.
  - Root Cause: OS-level mandatory locking prevents concurrent reads.
  - Mandated Alternative: Append-only immutable SSTable creation with atomic directory rename on completion.
- Worker adopts the mandated alternative; Milestone 2 succeeds cleanly.

### 6.2 The 16-Spawn Self-Succession Protocol
By Milestone 3, the Orchestrator reaches 16 subagent invocations ($\text{spawn\_count} = 16$).
1. Current orchestrator verifies all child workers have completed.
2. Compiles soft handoff in `handoff.md` detailing project state and next steps.
3. Updates `BRIEFING.md § Succession Status`:
   ```markdown
   - Succession required: Yes
   - Spawn count: 16 / 16
   ```
4. Terminates background cron monitors via `manage_task(Action="kill")`.
5. Spawns `teamwork-orchestrator` successor, passing the **original Sentinel conversation ID** as parent.
6. Successor executes 3-Step State Recovery, seamlessly continuing Milestone 3.

---

## 7. E2E Testing Completion & Acceptance

The E2E Testing Track finishes authoring the 49-test suite across Tiers 1-4 and publishes `TEST_READY.md`:
- Tier 1 (Feature Coverage): 20 tests
- Tier 2 (Boundary Cases): 20 tests
- Tier 3 (Cross-Feature Combinations): 4 tests
- Tier 4 (Real-World Application Scenarios): 5 tests
- Total: 49 tests (100% target achieved).

---

## 8. Final Victory Audit

The Orchestrator reports project completion to Sentinel. Sentinel dispatches a fresh `teamwork-victory-auditor`:

1. **Phase A — Traceability Audit**:
   - Traced all requirements from `ORIGINAL_REQUEST.md` (`R1` through `R4`) to implementation files. Zero omissions.
2. **Phase B — Forensic Integrity Audit**:
   - Audited all files in `src/` and `tests/`.
   - Verified zero stubs, zero forbidden shortcuts, zero temporary scratch files.
3. **Phase C — Autonomous Ground-Truth Execution**:
   - Auditor executes full test suite in workspace shell:
     ```bash
     pytest tests/e2e/ -v
     # Result: 49 passed in 4.12s (Exit code: 0)
     ```
   - Auditor executes simulated crash benchmark:
     ```bash
     python3 tests/benchmarks/benchmark_crash_recovery.py
     # Result: 100% recovery verified across 1,000,000 keys.
     ```

### Final Verdict: `VICTORY CONFIRMED`
Sentinel delivers completed project summary, test metrics, and repository documentation to the user.
