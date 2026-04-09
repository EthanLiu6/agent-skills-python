from __future__ import annotations

from pathlib import Path

from .models import SkillSummary
from .parser import SkillParseError, parse_skill_file


def find_skill_files(base_dir: str | Path) -> list[Path]:
    root = Path(base_dir).resolve()
    if not root.exists():
        return []
    return sorted(root.rglob("SKILL.md"))


def list_skills(base_dir: str | Path) -> list[SkillSummary]:
    summaries: list[SkillSummary] = []
    for skill_file in find_skill_files(base_dir):
        try:
            doc = parse_skill_file(skill_file)
        except SkillParseError:
            continue
        summaries.append(
            SkillSummary(
                root_dir=doc.root_dir,
                skill_md_path=doc.path,
                name=doc.metadata.name,
                description=doc.metadata.description,
            )
        )
    return summaries
