from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .parser import SkillParseError
from .reporting import (
    inspect_to_payload,
    summaries_to_payload,
    to_json,
    validation_to_payload,
    write_output,
)
from .service import discover_skills, inspect_skill, validate_skill, validate_skills


def main() -> None:
    parser = _build_parser()
    args = parser.parse_args()
    if not hasattr(args, "func"):
        parser.print_help()
        return
    try:
        args.func(args)
    except SkillParseError as exc:
        print(f"Skill parse error: {exc}", file=sys.stderr)
        raise SystemExit(2) from exc
    except FileNotFoundError as exc:
        print(str(exc), file=sys.stderr)
        raise SystemExit(2) from exc


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="agent-skills")
    parser.add_argument(
        "--format",
        choices=["text", "json"],
        default="text",
        help="Output format (default: text)",
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Write output to file path",
    )
    sub = parser.add_subparsers(dest="command")

    list_cmd = sub.add_parser("list", help="List all discovered skills")
    list_cmd.add_argument("path", type=str, help="Directory to scan")
    list_cmd.set_defaults(func=_cmd_list)

    inspect_cmd = sub.add_parser("inspect", help="Inspect one skill")
    inspect_cmd.add_argument("path", type=str, help="Skill directory or SKILL.md path")
    inspect_cmd.set_defaults(func=_cmd_inspect)

    validate_cmd = sub.add_parser("validate", help="Validate a skill or directory")
    validate_cmd.add_argument("path", type=str, help="Skill directory, SKILL.md path, or root directory")
    validate_cmd.add_argument(
        "--fail-on-warning",
        action="store_true",
        help="Exit with code 1 if warnings exist",
    )
    validate_cmd.set_defaults(func=_cmd_validate)

    return parser


def _cmd_list(args: argparse.Namespace) -> None:
    skills = discover_skills(args.path)
    data = summaries_to_payload(skills)
    if args.format == "json":
        write_output(to_json(data), args.output)
        return
    if not data:
        write_output("No skills found.", args.output)
        return
    lines: list[str] = []
    for item in data:
        lines.append(f"- {item['name']}: {item['description']}")
        lines.append(f"  dir: {item['skill_dir']}")
    write_output("\n".join(lines), args.output)


def _cmd_inspect(args: argparse.Namespace) -> None:
    doc = inspect_skill(args.path)
    payload = inspect_to_payload(doc)
    if args.format == "json":
        write_output(to_json(payload), args.output)
        return
    lines = [
        f"name: {payload['name']}",
        f"description: {payload['description']}",
        f"skill_dir: {payload['skill_dir']}",
        f"skill_md: {payload['skill_md']}",
        f"body_line_count: {payload['body_line_count']}",
        f"headings: {len(payload['headings'])}",
        f"file_references: {len(payload['file_references'])}",
    ]
    write_output("\n".join(lines), args.output)


def _cmd_validate(args: argparse.Namespace) -> None:
    target = Path(args.path).resolve()
    if target.is_file() or (target.is_dir() and (target / "SKILL.md").exists()):
        results = [validate_skill(target)]
    else:
        results = validate_skills(target)

    payload = validation_to_payload(results)
    has_error = any(not r["valid"] for r in payload)
    has_warning = any(
        any(i["level"] == "warning" for i in r["issues"])
        for r in payload
    )
    if args.format == "json":
        write_output(to_json(payload), args.output)
    else:
        if not payload:
            write_output("No skills to validate.", args.output)
            return
        lines: list[str] = []
        for result in payload:
            lines.append(f"{'PASS' if result['valid'] else 'FAIL'} {result['skill_md']}")
            for issue in result["issues"]:
                field_part = f" [{issue['field']}]" if issue["field"] else ""
                lines.append(
                    f"  - {issue['level'].upper()} {issue['code']}{field_part}: {issue['message']}"
                )
        write_output("\n".join(lines), args.output)

    if has_error or (args.fail_on_warning and has_warning):
        raise SystemExit(1)

