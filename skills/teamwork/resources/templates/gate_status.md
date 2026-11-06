# Milestone Gate Status — Milestone [M-XX] (Iteration [N])

## Verification Gate Invariants
1. **Fresh Context Isolation**: Critic, Challenger, and Auditor were spawned in pristine context with zero prior conversational history with the implementer.
2. **Empirical Reproduction Guarantee**: Challenger defects are backed by executable reproduction scripts.
3. **Forensic Integrity Tier**: Checked under active mode: `[development | demo | benchmark]`.
4. **Composite Determination Rule**: Gate Pass requires strict logical AND:
   $$\text{Gate Pass} = \text{Build/Test Pass} \land (\text{Critic} == \text{APPROVE}) \land (\text{Challenger} == \text{SURVIVED}) \land (\text{Auditor} == \text{PASS})$$

---

## Gate Review Ledger

| Gate | Assigned Agent | Verdict | Findings & Evidence Summary | Citations / Probes |
| :--- | :--- | :---: | :--- | :--- |
| **Gate 1: Critic** | `teamwork-critic` | `[APPROVE \| REJECT]` | [Summary of code quality, design soundness, and error handling. State Blocker/Major/Nit counts.] | `[path/to/file:line]` |
| **Gate 2: Challenger** | `teamwork-challenger` | `[SURVIVED \| BROKEN]` | [Adversarial stress results, race condition probes, or edge cases evaluated.] | `[reproduction_script.py]` |
| **Gate 3: Auditor** | `teamwork-auditor` | `[PASS \| INTEGRITY VIOLATION]` | [Forensic integrity check results (stubs, fakes, mocked tests) and independent shell test execution.] | `[Exit code: 0, 100% tests pass]` |

---

## Composite Gate Determination
- **Build / Local Test Status**: `[PASS | FAIL]`
- **Overall Milestone Result**: `[PASS | REMEDIATION_REQUIRED]`
- **Determination Detail**: [State whether all 4 criteria were met or detail which gate blocked acceptance]

---

## Remediation Plan (Required if REMEDIATION_REQUIRED)
If any gate rejected the candidate submission, document the remediation mandate before re-dispatching:
1. **Defects to Resolve**:
   - `[Defect 1 citation and required remediation]`
   - `[Defect 2 citation and required remediation]`
2. **Assigned Worker**: `[teamwork-worker]`
3. **Oscillation Check**: [Confirm failure has not occurred across 2 consecutive iterations; if so, log to DEAD_ENDS.md first]
