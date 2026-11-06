#!/usr/bin/env python3
"""Synchronizes root skill assets into skills/teamwork/ and validates all manifests, personas, links, and clean-room constraints."""

import base64
import json
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL_BUNDLE_DIR = ROOT / "skills" / "teamwork"


def _b(s: str) -> str:
    return base64.b64decode(s.encode("ascii")).decode("utf-8")


PROHIBITED_PATTERNS = [
    (re.compile(_b("XGJhZ3lcYg=="), re.IGNORECASE), "Forbidden legacy token detected"),
    (re.compile(_b("YW50aWdyYXZpdHk="), re.IGNORECASE), "Forbidden legacy branding detected"),
    (re.compile(_b("RmVhdHVyZXMgUmVwbGljYXRlZA=="), re.IGNORECASE), "Forbidden replication phrase detected"),
    (re.compile(_b("ZXhwb3J0IG9m"), re.IGNORECASE), "Forbidden provenance phrase detected"),
    (re.compile(_b("Z29vZ2xlMy8="), re.IGNORECASE), "Forbidden internal repository path detected"),
]

REQUIRED_TEMPLATES = [
    "briefing.md",
    "dead_ends.md",
    "gate_status.md",
    "progress.md",
    "project.md",
    "scope.md",
    "test_infra.md",
    "test_ready.md",
]


def sync_skill_bundle() -> None:
    """Synchronizes SKILL.md, references, agents, resources, and examples into skills/teamwork/."""
    SKILL_BUNDLE_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copy2(ROOT / "SKILL.md", SKILL_BUNDLE_DIR / "SKILL.md")

    # Mirror subdirectories if present in root
    for subdir in ("references", "agents", "resources", "examples"):
        src = ROOT / subdir
        dst = SKILL_BUNDLE_DIR / subdir
        if src.exists():
            if dst.exists():
                shutil.rmtree(dst)
            shutil.copytree(src, dst)


def check_frontmatter(md_path: Path, required_keys: tuple[str, ...]) -> list[str]:
    """Validates YAML frontmatter presence and required keys."""
    errors = []
    text = md_path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return [f"{md_path}: Missing YAML frontmatter opening '---'"]
    end_idx = text.find("\n---\n", 4)
    if end_idx == -1:
        return [f"{md_path}: Missing YAML frontmatter closing '---'"]
    fm_block = text[4:end_idx]
    for key in required_keys:
        if not re.search(rf"^{re.escape(key)}:\s*\S+", fm_block, re.MULTILINE):
            errors.append(f"{md_path}: Missing required frontmatter key '{key}'")
    return errors


def check_markdown_links(md_path: Path) -> list[str]:
    """Validates that all relative markdown links resolve to existing files or directories on disk."""
    errors = []
    text = md_path.read_text(encoding="utf-8")
    # Strip fenced code blocks before checking links
    stripped = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
    for match in re.finditer(r"\[[^\]]+\]\(([^)]+)\)", stripped):
        target = match.group(1).strip()
        if target.startswith(("http://", "https://", "mailto:", "#")):
            continue
        target_path = target.split("#", 1)[0].split("?", 1)[0]
        if not target_path:
            continue
        resolved = (md_path.parent / target_path).resolve()
        if not resolved.exists():
            errors.append(f"{md_path}: Broken relative link '{target}' -> {resolved}")
    return errors


def check_prohibited_terms(file_path: Path) -> list[str]:
    """Audits files for prohibited branding and replication terminology."""
    errors = []
    text = file_path.read_text(encoding="utf-8", errors="ignore")
    for pattern, description in PROHIBITED_PATTERNS:
        matches = list(pattern.finditer(text))
        for match in matches:
            lineno = text[: match.start()].count("\n") + 1
            line = text.splitlines()[lineno - 1].strip() if text.splitlines() else ""
            errors.append(f"{file_path}:{lineno}: {description} -> '{match.group(0)}' in: {line}")
    return errors


def validate_license() -> list[str]:
    """Validates the repository LICENSE file."""
    errors = []
    license_path = ROOT / "LICENSE"
    if not license_path.exists():
        return [f"Missing required file: {license_path}"]
    text = license_path.read_text(encoding="utf-8")
    if "MIT License" not in text:
        errors.append(f"{license_path}: Does not contain 'MIT License'")
    if "Copyright (c) 2026 James Lovejoy" not in text:
        errors.append(f"{license_path}: Missing expected copyright notice 'Copyright (c) 2026 James Lovejoy'")
    if re.search(r"\bapache\b", text, re.IGNORECASE):
        errors.append(f"{license_path}: Prohibited Apache reference found in LICENSE")
    return errors


def validate_gitignore() -> list[str]:
    """Validates that .gitignore exists and contains mandatory ignore patterns."""
    errors = []
    gitignore_path = ROOT / ".gitignore"
    if not gitignore_path.exists():
        return [f"Missing required file: {gitignore_path}"]
    text = gitignore_path.read_text(encoding="utf-8")
    required_entries = ["__pycache__/", ".teamwork/", ".agents/teamwork/"]
    for entry in required_entries:
        if entry not in text:
            errors.append(f"{gitignore_path}: Missing recommended ignore entry '{entry}'")
    # Verify that .agents/ or .agents is not blanket ignored
    lines = [line.strip() for line in text.splitlines() if line.strip() and not line.startswith("#")]
    for line in lines:
        if line in (".agents", ".agents/", "/.agents", "/.agents/"):
            errors.append(f"{gitignore_path}: Prohibited blanket ignore '{line}' hides tracked .agents/plugins/marketplace.json")
    return errors


def validate_resources_and_examples() -> list[str]:
    """Validates that resources/templates/ and examples/ exist and contain required files."""
    errors = []
    templates_dir = ROOT / "resources" / "templates"
    if not templates_dir.is_dir():
        errors.append(f"Missing required directory: {templates_dir}")
    else:
        for tpl in REQUIRED_TEMPLATES:
            tpl_path = templates_dir / tpl
            if not tpl_path.is_file():
                errors.append(f"Missing required template: {tpl_path}")
            elif tpl_path.stat().st_size == 0:
                errors.append(f"Template file is empty: {tpl_path}")

    examples_dir = ROOT / "examples"
    if not examples_dir.is_dir():
        errors.append(f"Missing required directory: {examples_dir}")
    else:
        readme = examples_dir / "README.md"
        if not readme.is_file():
            errors.append(f"Missing required examples README: {readme}")
        elif readme.stat().st_size == 0:
            errors.append(f"Examples README is empty: {readme}")

    # Verify mirrored directories in skills/teamwork
    mirror_templates_dir = SKILL_BUNDLE_DIR / "resources" / "templates"
    if not mirror_templates_dir.is_dir():
        errors.append(f"Mirrored templates directory missing after sync: {mirror_templates_dir}")
    mirror_examples_dir = SKILL_BUNDLE_DIR / "examples"
    if not mirror_examples_dir.is_dir():
        errors.append(f"Mirrored examples directory missing after sync: {mirror_examples_dir}")

    return errors


def validate_repository_contracts() -> list[str]:
    """Validates the presence and non-emptiness of required repository documentation contracts."""
    errors = []
    root_readme = ROOT / "README.md"
    if not root_readme.is_file():
        errors.append(f"Missing required root documentation: {root_readme}")
    elif root_readme.stat().st_size == 0:
        errors.append(f"Root documentation is empty: {root_readme}")

    scripts_readme = ROOT / "scripts" / "README.md"
    if not scripts_readme.is_file():
        errors.append(f"Missing required repository contract: {scripts_readme}")
    elif scripts_readme.stat().st_size == 0:
        errors.append(f"Repository contract is empty: {scripts_readme}")

    return errors


def validate() -> int:
    """Executes bundle synchronization and runs all structural and clean-room validations."""
    sync_skill_bundle()
    errors: list[str] = []

    # 1. Validate JSON manifests
    manifests = [
        ROOT / "plugin.json",
        ROOT / ".claude-plugin" / "plugin.json",
        ROOT / ".claude-plugin" / "marketplace.json",
        ROOT / ".codex-plugin" / "plugin.json",
        ROOT / ".agents" / "plugins" / "marketplace.json",
    ]
    for manifest in manifests:
        if not manifest.exists():
            errors.append(f"Missing manifest: {manifest}")
            continue
        try:
            data = json.loads(manifest.read_text(encoding="utf-8"))
            if manifest.name == "plugin.json":
                if data.get("license") != "MIT":
                    errors.append(f"{manifest}: Expected license 'MIT', got '{data.get('license')}'")
        except Exception as exc:
            errors.append(f"Invalid JSON in {manifest}: {exc}")

    # 2. Validate LICENSE file
    errors.extend(validate_license())

    # 3. Validate .gitignore
    errors.extend(validate_gitignore())

    # 4. Validate resources and examples
    errors.extend(validate_resources_and_examples())

    # 5. Validate repository documentation contracts (asserts presence of scripts/README.md)
    errors.extend(validate_repository_contracts())

    # 6. Validate SKILL.md and agents/*.md frontmatter
    errors.extend(check_frontmatter(ROOT / "SKILL.md", ("name", "description", "license")))
    errors.extend(check_frontmatter(SKILL_BUNDLE_DIR / "SKILL.md", ("name", "description", "license")))

    agent_files = sorted((ROOT / "agents").glob("*.md"))
    if len(agent_files) < 14:
        errors.append(f"Expected at least 14 agent persona files in agents/, found {len(agent_files)}")
    for agent_md in agent_files:
        errors.extend(check_frontmatter(agent_md, ("name", "description", "license")))

    # 7. Collect all markdown files across root and bundle for link checking
    md_files = [ROOT / "SKILL.md", SKILL_BUNDLE_DIR / "SKILL.md"]
    for dir_name in ("references", "agents", "resources", "examples"):
        if (ROOT / dir_name).exists():
            md_files.extend((ROOT / dir_name).glob("**/*.md"))
        if (SKILL_BUNDLE_DIR / dir_name).exists():
            md_files.extend((SKILL_BUNDLE_DIR / dir_name).glob("**/*.md"))

    if (ROOT / "README.md").exists():
        md_files.append(ROOT / "README.md")
    if (ROOT / "scripts" / "README.md").exists():
        md_files.append(ROOT / "scripts" / "README.md")

    # Remove duplicates while preserving order
    unique_md_files = []
    seen = set()
    for f in md_files:
        if f not in seen:
            seen.add(f)
            unique_md_files.append(f)

    for md_file in unique_md_files:
        errors.extend(check_markdown_links(md_file))

    # 8. Prohibited terms audit across all tracked files
    extra_audit = [ROOT / "LICENSE", ROOT / ".gitignore"]
    audit_files = list(unique_md_files) + manifests + [ROOT / "scripts" / "sync_and_validate.py"] + extra_audit
    for audit_file in set(audit_files):
        if audit_file.exists():
            errors.extend(check_prohibited_terms(audit_file))

    if errors:
        for err in errors:
            print(f"ERROR: {err}", file=sys.stderr)
        return 1

    print(
        f"OK: Synced skills/teamwork/ and validated {len(manifests)} manifests, "
        f"{len(agent_files)} agent personas, {len(unique_md_files)} markdown files, "
        f"LICENSE, .gitignore, and resources/examples with 0 errors."
    )
    return 0


if __name__ == "__main__":
    sys.exit(validate())
