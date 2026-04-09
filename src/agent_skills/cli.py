from __future__ import annotations

import argparse
import json
from pathlib import Path

from .service import discover_skills, inspect_skill, validate_skill, validate_skills


def main() -> None:
    parser = _build_parser()
    args = parser.parse_args()
    if not hasattr(args, "func"):
        parser.print_help()
        return
    args.func(args)


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="agent-skills")
    sub = parser.add_subparsers(dest="command")

    list_cmd = sub.add_parser("list", help="List all discovered skills")
    list_cmd.add_argument("path", type=str, help="Directory to scan")
    list_cmd.add_argument("--json", action="store_true", help="Output JSON")
    list_cmd.set_defaults(func=_cmd_list)

    inspect_cmd = sub.add_parser("inspect", help="Inspect one skill")
    inspect_cmd.add_argument("path", type=str, help="Skill directory or SKILL.md path")
    inspect_cmd.add_argument("--json", action="store_true", help="Output JSON")
    inspect_cmd.set_defaults(func=_cmd_inspect)

    validate_cmd = sub.add_parser("validate", help="Validate a skill or directory")
    validate_cmd.add_argument("path", type=str, help="Skill directory, SKILL.md path, or root directory")
    validate_cmd.add_argument("--json", action="store_true", help="Output JSON")
    validate_cmd.set_defaults(func=_cmd_validate)

    return parser


def _cmd_list(args: argparse.Namespace) -> None:
    skills = discover_skills(args.path)
    data = [
        {
            "name": s.name,
            "description": s.description,
            "skill_dir": str(s.root_dir),
            "skill_md": str(s.skill_md_path),
        }
        for s in skills
    ]
    if args.json:
        print(json.dumps(data, ensure_ascii=False, indent=2))
        return
    if not data:
        print("No skills found.")
        return
    for item in data:
        print(f"- {item['name']}: {item['description']}")
        print(f"  dir: {item['skill_dir']}")


def _cmd_inspect(args: argparse.Namespace) -> None:
    doc = inspect_skill(args.path)
    payload = {
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
    print(json.dumps(payload, ensure_ascii=False, indent=2))


def _cmd_validate(args: argparse.Namespace) -> None:
    target = Path(args.path).resolve()
    if target.is_file() or (target.is_dir() and (target / "SKILL.md").exists()):
        results = [validate_skill(target)]
    else:
        results = validate_skills(target)

    payload = [
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

    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return

    if not payload:
        print("No skills to validate.")
        return

    for result in payload:
        print(f"{'PASS' if result['valid'] else 'FAIL'} {result['skill_md']}")
        for issue in result["issues"]:
            field_part = f" [{issue['field']}]" if issue["field"] else ""
            print(f"  - {issue['level'].upper()} {issue['code']}{field_part}: {issue['message']}")
