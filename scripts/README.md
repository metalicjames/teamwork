# Scripts Component Package

## System Overview
The `scripts/` directory provides repository-level automation, build synchronization, and clean-room validation tooling for the Teamwork multi-agent orchestration framework. Its core utility, `sync_and_validate.py`, acts as the continuous integration and structural gatekeeper for the codebase.

The tooling guarantees architectural parity between primary authoring assets and distribution artifacts, ensuring that:
1. Canonical skill definitions, agent persona files, operational protocols, reference templates, and workflow examples in the repository root are mirrored cleanly into the standalone bundle directory (`skills/teamwork/`).
2. All markdown files, plugin manifests, license declarations, and git ignore configurations strictly adhere to clean-room standards, valid relative links, and the project's MIT license.

---

## Interface

### Command-Line Interface (CLI)

The primary entry point is executable directly from the shell or via Python 3:

```bash
# Executable script invocation
./scripts/sync_and_validate.py

# Explicit Python 3 interpreter invocation
python3 scripts/sync_and_validate.py
```

- **Arguments**: None required. Execution resolves paths dynamically relative to the script location.
- **Exit Codes**:
  - `0`: All validations and synchronization routines succeeded without errors.
  - `1`: One or more validation checks failed (errors logged to `sys.stderr`).

### Programmatic API (`sync_and_validate.py`)

The script can be imported and executed programmatically within automated test suites or build runners:

```python
from pathlib import Path
import sync_and_validate

# Run full synchronization and validation pipeline (returns int exit code: 0 or 1)
exit_code: int = sync_and_validate.validate()

# Or invoke discrete lifecycle stages:
sync_and_validate.sync_skill_bundle()
frontmatter_errors: list[str] = sync_and_validate.check_frontmatter(Path("SKILL.md"), ("name", "description", "license"))
link_errors: list[str] = sync_and_validate.check_markdown_links(Path("references/orchestration-patterns.md"))
token_errors: list[str] = sync_and_validate.check_prohibited_terms(Path("agents/teamwork-orchestrator.md"))
license_errors: list[str] = sync_and_validate.validate_license()
gitignore_errors: list[str] = sync_and_validate.validate_gitignore()
resource_errors: list[str] = sync_and_validate.validate_resources_and_examples()
```

#### Exported Symbols & Constants

| Symbol | Type | Description |
| :--- | :--- | :--- |
| `ROOT` | `Path` | Absolute path resolving to the repository root directory. |
| `SKILL_BUNDLE_DIR` | `Path` | Target distribution directory path (`skills/teamwork`). |
| `PROHIBITED_PATTERNS` | `list[tuple[Pattern, str]]` | Compiled regex patterns identifying forbidden legacy branding, proprietary provenance phrases, and internal paths. |
| `REQUIRED_TEMPLATES` | `list[str]` | Canonical set of 8 mandatory operational template files required in `resources/templates/`. |
| `sync_skill_bundle()` | `() -> None` | Recursively mirrors root assets (`SKILL.md`, `references/`, `agents/`, `resources/`, `examples/`) into `skills/teamwork/`. |
| `check_frontmatter()` | `(Path, tuple[str, ...]) -> list[str]` | Verifies YAML frontmatter delimitation (`---`) and mandatory key presence. |
| `check_markdown_links()` | `(Path) -> list[str]` | Extracts relative markdown links outside code fences and validates disk existence. |
| `check_prohibited_terms()`| `(Path) -> list[str]` | Audits files for forbidden branding tokens and proprietary path markers. |
| `validate_license()` | `() -> list[str]` | Asserts MIT license text and copyright notice in `LICENSE`. |
| `validate_gitignore()` | `() -> list[str]` | Confirms `.gitignore` ignore rules while forbidding blanket ignores of `.agents`. |
| `validate_resources_and_examples()` | `() -> list[str]` | Verifies presence and non-zero size of templates and example walkthroughs. |
| `validate()` | `() -> int` | Executes the complete validation pipeline; returns `0` on success, `1` on failure. |

### Component Contract Boundaries

- **Subdirectories**: None (all tooling scripts reside directly in `scripts/`).
- **Related Contracts & References**:
  - [Repository Root Blueprint](../README.md): System-wide architecture and multi-harness installation.
  - [Examples Package](../examples/README.md): Reference implementations and execution walkthroughs.
  - [Operational Protocols](../references/operational-protocols.md): Agent handoffs, state recovery, and heartbeats.
  - [Orchestration Patterns](../references/orchestration-patterns.md): Canonical execution workflows.
  - [Verification Gates](../references/verification-gates.md): Gate audit specifications and victory criteria.
  - [Harness Delegation](../references/harness-delegation.md): Adapter contracts across supported execution engines.
  - [Interview Protocol](../references/interview-protocol.md): Scoping interview lifecycle.

---

## Invariants

The scripts tooling strictly guarantees and enforces the following repository invariants:

1. **Directory Symmetry & Bundle Parity**:
   - `skills/teamwork/` is guaranteed to be an exact, deterministic mirror of root authoring files (`SKILL.md`, `references/`, `agents/`, `resources/`, `examples/`).
   - Destination subdirectories in `skills/teamwork/` are purged prior to copying, preventing stale or deleted root files from surviving in the bundle.
2. **Relative Link Integrity**:
   - Every relative markdown link (formatted with standard link syntax outside code fences) across all documentation files (root, subdirectories, and mirrored distribution bundle) must resolve to an existing file or directory path on disk.
   - Fenced code blocks are stripped prior to link scanning to eliminate false positives from code samples.
3. **Clean-Room & Prohibited Token Elimination**:
   - Zero occurrences of deprecated platform branding, predecessor project monikers, internal corporate repository paths, or replication phrases are permitted in any tracked repository file.
4. **MIT License Uniformity**:
   - The repository `LICENSE` file must contain standard MIT License terms with `Copyright (c) 2026 James Lovejoy`.
   - All agent persona files (`agents/*.md`), root skill manifests (`SKILL.md`), and plugin configuration files (`plugin.json`, `.claude-plugin/plugin.json`, `.codex-plugin/plugin.json`, `.agents/plugins/marketplace.json`) must explicitly declare the MIT license.
5. **Specification Completeness**:
   - The repository must define at least 14 canonical agent personas under `agents/`.
   - All 8 operational templates (`briefing.md`, `dead_ends.md`, `gate_status.md`, `progress.md`, `project.md`, `scope.md`, `test_infra.md`, `test_ready.md`) in `resources/templates/` must exist and be non-empty.
6. **Git Hygiene & Marketplace Tracking**:
   - `.gitignore` must ignore runtime scratch directories (`__pycache__/`, `.teamwork/`, `.agents/teamwork/`).
   - Blanket ignores on `.agents` are prohibited to ensure `.agents/plugins/marketplace.json` remains tracked.

---

## Side Effects

Running `sync_and_validate.py` produces the following deterministic side effects:

- **Filesystem Creation & Mirroring**:
  - Creates the directory `skills/teamwork/` if it does not already exist.
  - Copies `ROOT / "SKILL.md"` to `skills/teamwork/SKILL.md` (overwriting the destination).
  - Copies all files from `ROOT / references/`, `ROOT / agents/`, `ROOT / resources/`, and `ROOT / examples/` into corresponding locations under `skills/teamwork/`.
- **Destructive Deletion of Bundle Mirrors**:
  - Prior to mirroring, if destination directories (`skills/teamwork/references`, `skills/teamwork/agents`, `skills/teamwork/resources`, `skills/teamwork/examples`) already exist, they are completely deleted via `shutil.rmtree()` and recreated from the root source. Any untracked modifications made directly inside `skills/teamwork/` subdirectories will be discarded.
- **Process Output**:
  - Emits diagnostic error messages to `sys.stderr` if any invariant fails.
  - Emits a concise validation summary to `sys.stdout` upon successful completion.
- **Isolation**:
  - No network traffic, database mutations, or remote git commands are executed.

---

## Verification

### Automated Verification Command

Run the test suite directly from the repository root:

```bash
python3 scripts/sync_and_validate.py
```

### Expected Output

When all invariants are satisfied, the script completes with exit code `0` and outputs:

```
OK: Synced skills/teamwork/ and validated 5 manifests, 14 agent personas, 66 markdown files, LICENSE, .gitignore, and resources/examples with 0 errors.
```

### Verification Commands & Health Checks

1. **Exit Code Check**:
   ```bash
   python3 scripts/sync_and_validate.py && echo "STATUS: PASS (Exit Code $?)"
   ```
2. **Interpreter Syntax Check**:
   ```bash
   python3 -m py_compile scripts/sync_and_validate.py
   ```
3. **Negative Fault Injection Test**:
   - Temporarily inserting an invalid markdown target path in a documentation file causes the validation to halt with exit code `1` and print the exact file, line number, and broken path to `sys.stderr`.
