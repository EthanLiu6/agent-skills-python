from __future__ import annotations

import re

from .models import SkillDocument, ValidationIssue, ValidationResult


NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
XML_TAG_RE = re.compile(r"<[^>]+>")


def validate_skill_document(document: SkillDocument) -> ValidationResult:
    issues: list[ValidationIssue] = []
    meta = document.metadata

    if not meta.name:
        issues.append(_err("name.required", "name is required", "name"))
    else:
        if len(meta.name) > 64:
            issues.append(_err("name.length", "name must be <= 64 chars", "name"))
        if not NAME_RE.match(meta.name):
            issues.append(
                _err(
                    "name.pattern",
                    "name must use lowercase letters, digits, and single hyphens only",
                    "name",
                )
            )
        if meta.name.startswith("-") or meta.name.endswith("-") or "--" in meta.name:
            issues.append(_err("name.hyphen", "name hyphen usage is invalid", "name"))
        if "anthropic" in meta.name or "claude" in meta.name:
            issues.append(_err("name.reserved", "name contains reserved words", "name"))
        if XML_TAG_RE.search(meta.name):
            issues.append(_err("name.xml_tag", "name must not contain XML tags", "name"))
        if meta.name != document.root_dir.name:
            issues.append(_err("name.dir_mismatch", "name must match parent directory name", "name"))

    if not meta.description:
        issues.append(_err("description.required", "description is required", "description"))
    else:
        desc = meta.description.strip()
        if not desc:
            issues.append(_err("description.required", "description cannot be empty", "description"))
        if len(desc) > 1024:
            issues.append(_err("description.length", "description must be <= 1024 chars", "description"))
        if XML_TAG_RE.search(desc):
            issues.append(_err("description.xml_tag", "description must not contain XML tags", "description"))
        if "use when" not in desc.lower() and "在" not in desc:
            issues.append(
                _warn(
                    "description.discoverability",
                    "description should mention usage trigger for discovery",
                    "description",
                )
            )

    if meta.compatibility is not None:
        if not meta.compatibility.strip():
            issues.append(_err("compatibility.empty", "compatibility must be non-empty when provided", "compatibility"))
        if len(meta.compatibility) > 500:
            issues.append(_err("compatibility.length", "compatibility must be <= 500 chars", "compatibility"))

    if not isinstance(meta.metadata, dict):
        issues.append(_err("metadata.type", "metadata must be key-value mapping", "metadata"))
    else:
        for k, v in meta.metadata.items():
            if not isinstance(k, str) or not isinstance(v, str):
                issues.append(_err("metadata.kv_type", "metadata keys/values must be strings", "metadata"))
                break

    if len(document.body.splitlines()) > 500:
        issues.append(
            _warn(
                "body.length",
                "SKILL.md body exceeds 500 lines; consider splitting references",
                "body",
            )
        )

    valid = not any(issue.level == "error" for issue in issues)
    return ValidationResult(skill_path=document.path, valid=valid, issues=issues)


def _err(code: str, message: str, field: str | None = None) -> ValidationIssue:
    return ValidationIssue(level="error", code=code, message=message, field=field)


def _warn(code: str, message: str, field: str | None = None) -> ValidationIssue:
    return ValidationIssue(level="warning", code=code, message=message, field=field)
