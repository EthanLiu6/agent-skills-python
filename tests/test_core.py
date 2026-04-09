from pathlib import Path

from agent_skills import discover_skills, parse_skill_file, validate_skill


def test_parse_and_discover() -> None:
    doc = parse_skill_file(Path("examples/pdf-processing/SKILL.md"))
    assert doc.metadata.name == "pdf-processing"
    assert doc.headings

    skills = discover_skills("examples")
    assert any(s.name == "pdf-processing" for s in skills)


def test_validate_passes() -> None:
    result = validate_skill("examples/pdf-processing")
    assert result.valid is True
