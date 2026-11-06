# Milestone Scope & Work-Package Decomposition — Milestone [M-XX]

## 1. Sub-Orchestrator Context
- **Milestone Identifier**: `[M-XX]`
- **Sub-Orchestrator Conversation ID**: `[Sub-Orchestrator Conv ID]`
- **Parent Orchestrator Conversation ID**: `[Parent Conv ID]`
- **Milestone Objective**: [Concise summary of functional deliverables for this milestone]

---

## 2. Work-Package Decomposition
Decomposes the milestone into parallel or sequential work-packages assigned to individual workers.

| WP ID | Package Name | Assigned Worker | Primary Deliverables | Pre-requisites | Status |
| :--- | :--- | :--- | :--- | :--- | :---: |
| **WP-01** | [Package 1 Name] | `teamwork-worker-1` | [Core component implementation & unit tests] | None | `IN_PROGRESS` |
| **WP-02** | [Package 2 Name] | `teamwork-worker-2` | [Supporting subsystem implementation & unit tests] | WP-01 Interfaces | `PENDING` |

---

## 3. Exclusive File Ownership Boundaries
To eliminate merge conflicts and concurrent modification collisions, workers are strictly confined to assigned paths:

| Worker Role | Exclusive Write Paths (Allowed) | Read-Only Paths (Reference) | Prohibited Paths |
| :--- | :--- | :--- | :--- |
| `teamwork-worker-1` | `src/module_a/`<br>`tests/unit/test_module_a.py` | `src/common/`<br>`PROJECT_PLAN.md` | Any other directory in `src/` |
| `teamwork-worker-2` | `src/module_b/`<br>`tests/unit/test_module_b.py` | `src/module_a/`<br>`src/common/` | `src/module_a/` |

---

## 4. Work-Package Handshake Contracts
Specifies the exact interfaces connecting distinct work-packages:

### Handshake: WP-01 ──► WP-02
- **Exported Symbol / Interface**: `[Class, function, or API signature]`
- **Data Invariant**: `[State guarantees, invariants, thread-safety]`
- **Mock / Stub Harness for Testing**: `[Path to test doubles or interface fixtures]`

---

## 5. Local Verification Requirements
Before delivering a handoff report, each worker must execute and document these local checks:

1. **Compilation / Static Analysis**:
   ```bash
   [Exact linting or type-checking command, e.g., mypy src/module_a/]
   ```
2. **Local Unit Test Suite**:
   ```bash
   [Exact unit test execution command, e.g., pytest tests/unit/test_module_a.py -v]
   ```

---

## 6. Milestone Consolidation & Gate Aggregation
Upon completion of all work packages:
1. Sub-Orchestrator compiles integrated diff across all work packages.
2. Sub-Orchestrator runs full workspace test command: `[Integrated test command]`.
3. Sub-Orchestrator dispatches fresh `teamwork-critic`, `teamwork-challenger`, and `teamwork-auditor` to evaluate the integrated milestone.
4. Sub-Orchestrator records verdicts in `GATE_STATUS.md` and submits soft handoff to Parent Orchestrator.
