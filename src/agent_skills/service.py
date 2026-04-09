from __future__ import annotations

from pathlib import Path

from .discovery import find_skill_files, list_skills
from .models import SkillDocument, SkillSummary, ValidationResult
from .parser import parse_skill_file
from .validator import validate_skill_document


def inspect_skill(path: str | Path) -> SkillDocument:
    target = Path(path).resolve()
    skill_md = target / "SKILL.md" if target.is_dir() else target
    return parse_skill_file(skill_md)


def validate_skill(path: str | Path) -> ValidationResult:
    doc = inspect_skill(path)
    return validate_skill_document(doc)


def validate_skills(base_dir: str | Path) -> list[ValidationResult]:
    results: list[ValidationResult] = []
    for skill_md in find_skill_files(base_dir):
        doc = parse_skill_file(skill_md)
        results.append(validate_skill_document(doc))
    return results


def discover_skills(base_dir: str | Path) -> list[SkillSummary]:
    return list_skills(base_dir)
