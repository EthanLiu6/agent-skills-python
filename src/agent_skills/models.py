from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass(slots=True)
class SkillMetadata:
    name: str
    description: str
    license: str | None = None
    compatibility: str | None = None
    metadata: dict[str, str] = field(default_factory=dict)
    allowed_tools: str | None = None
    raw: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class SkillDocument:
    path: Path
    root_dir: Path
    metadata: SkillMetadata
    body: str
    headings: list[str] = field(default_factory=list)
    file_references: list[str] = field(default_factory=list)


@dataclass(slots=True)
class ValidationIssue:
    level: str
    code: str
    message: str
    field: str | None = None


@dataclass(slots=True)
class ValidationResult:
    skill_path: Path
    valid: bool
    issues: list[ValidationIssue]


@dataclass(slots=True)
class SkillSummary:
    root_dir: Path
    skill_md_path: Path
    name: str
    description: str
