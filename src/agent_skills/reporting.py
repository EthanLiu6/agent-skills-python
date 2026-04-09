from __future__ import annotations

import json
from pathlib import Path

from .models import SkillDocument, SkillSummary, ValidationResult


def summaries_to_payload(items: list[SkillSummary]) -> list[dict[str, str]]:
    return [
        {
            "name": s.name,
            "description": s.description,
            "skill_dir": str(s.root_dir),
            "skill_md": str(s.skill_md_path),
        }
        for s in items
    ]


def inspect_to_payload(doc: SkillDocument) -> dict[str, object]:
    return {
        "name": doc.metadata.name,
        "description": doc.metadata.description,
        "license": doc.metadata.license,
        "compatibility": doc.metadata.compatibility,
        "metadata": doc.metadata.metadata,
        "allowed_tools": doc.metadata.allowed_tools,
        "headings": doc.headings,
        "file_references": doc.file_references,
        "body_line_count": len(doc.body.splitlines()),
        "skill_dir": str(doc.root_dir),
        "skill_md": str(doc.path),
    }


def validation_to_payload(results: list[ValidationResult]) -> list[dict[str, object]]:
    return [
        {
            "skill_md": str(r.skill_path),
            "valid": r.valid,
            "issues": [
                {"level": i.level, "code": i.code, "field": i.field, "message": i.message}
                for i in r.issues
            ],
        }
        for r in results
    ]


def write_output(content: str, output_path: str | None) -> None:
    if not output_path:
        print(content)
        return
    path = Path(output_path).resolve()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content + "\n", encoding="utf-8")


def to_json(data: object) -> str:
    return json.dumps(data, ensure_ascii=False, indent=2)
