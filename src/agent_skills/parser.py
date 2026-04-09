from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import yaml

from .models import SkillDocument, SkillMetadata


FRONTMATTER_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*\n?", re.DOTALL)
HEADING_RE = re.compile(r"^\s{0,3}#{1,6}\s+(.+?)\s*$", re.MULTILINE)
MARKDOWN_LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
PATH_HINT_RE = re.compile(r"\b(?:scripts|references|assets)/[^\s)]+")


class SkillParseError(ValueError):
    pass


def parse_skill_file(path: str | Path) -> SkillDocument:
    skill_md = Path(path).resolve()
    if not skill_md.exists():
        raise SkillParseError(f"SKILL.md does not exist: {skill_md}")
    if skill_md.name != "SKILL.md":
        raise SkillParseError(f"Expected SKILL.md file, got: {skill_md.name}")

    text = skill_md.read_text(encoding="utf-8")
    if text.startswith("\ufeff"):
        text = text.lstrip("\ufeff")
    frontmatter, body = _split_frontmatter(text)
    raw = _load_frontmatter(frontmatter)

    try:
        name = str(raw["name"])
        description = str(raw["description"])
    except KeyError as exc:
        raise SkillParseError(f"Missing required frontmatter field: {exc.args[0]}") from exc

    metadata_map = raw.get("metadata") or {}
    if not isinstance(metadata_map, dict):
        metadata_map = {}

    metadata = SkillMetadata(
        name=name,
        description=description,
        license=_optional_str(raw.get("license")),
        compatibility=_optional_str(raw.get("compatibility")),
        metadata={str(k): str(v) for k, v in metadata_map.items()},
        allowed_tools=_optional_str(raw.get("allowed-tools")),
        raw=raw,
    )

    headings = [h.strip() for h in HEADING_RE.findall(body)]
    file_refs = _extract_file_references(body)

    return SkillDocument(
        path=skill_md,
        root_dir=skill_md.parent,
        metadata=metadata,
        body=body,
        headings=headings,
        file_references=file_refs,
    )


def _split_frontmatter(text: str) -> tuple[str, str]:
    match = FRONTMATTER_RE.match(text)
    if not match:
        raise SkillParseError("SKILL.md is missing YAML frontmatter delimited by ---")
    return match.group(1), text[match.end() :]


def _load_frontmatter(frontmatter: str) -> dict[str, Any]:
    try:
        data = yaml.safe_load(frontmatter)
    except yaml.YAMLError as exc:
        raise SkillParseError(f"Invalid YAML frontmatter: {exc}") from exc
    if not isinstance(data, dict):
        raise SkillParseError("YAML frontmatter must decode to a mapping/object")
    return data


def _extract_file_references(body: str) -> list[str]:
    refs = set()
    for target in MARKDOWN_LINK_RE.findall(body):
        clean = target.strip()
        if clean and not clean.startswith(("http://", "https://", "mailto:")):
            refs.add(clean)
    for target in PATH_HINT_RE.findall(body):
        refs.add(target.strip())
    return sorted(refs)


def _optional_str(value: Any) -> str | None:
    if value is None:
        return None
    return str(value)
