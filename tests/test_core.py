from pathlib import Path

from agent_skills import discover_skills, parse_skill_file, validate_skill


def test_parse_and_discover() -> None:
    doc = parse_skill_file(Path("examples/pdf-processing/SKILL.md"))
    assert doc.metadata.name == "pdf-processing"
    assert doc.headings

    skills = discover_skills("examples")
    names = {s.name for s in skills}
    assert "pdf-processing" in names
    assert "docx-authoring" in names
    assert "json-schema-validation" in names
    assert "json-transform-pipeline" in names
    assert "api-contract-testing" in names


def test_validate_passes() -> None:
    result = validate_skill("examples/pdf-processing")
    assert result.valid is True


def test_validate_includes_heading_warning_when_missing(tmp_path: Path) -> None:
    skill_dir = tmp_path / "no-heading-skill"
    skill_dir.mkdir()
    (skill_dir / "SKILL.md").write_text(
        """---
name: no-heading-skill
description: Validate minimal content for warnings. Use when testing warning paths.
---
plain body without headings
""",
        encoding="utf-8",
    )
    result = validate_skill(skill_dir)
    assert result.valid is True
    assert any(i.code == "body.headings" for i in result.issues)
