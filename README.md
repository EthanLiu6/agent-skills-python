# agent-skills-python

`agent-skills-python` is a production-ready toolkit that helps any Python-based agent
or automation platform adopt the Agent Skills format. The import package is
`agent_skills`.

This project is designed for:

- **High availability**: resilient parsing/validation, predictable CLI behavior
- **Maintainability**: layered architecture, typed models, small focused modules
- **Ease of use**: straightforward API + CLI + ready-to-run examples

## Version

- Current release: `v0.1.1`

## Core capabilities

- Parse `SKILL.md` into structured objects (`metadata`, `body`, headings, references)
- Validate skills against spec constraints and practical best-practice checks
- Discover and list skills from any directory tree
- Generate machine-readable payloads for integration (`JSON`) and human-readable text reports

## Installation

### Development install

```bash
pip install -e ".[dev]"
```

### Runtime install

```bash
pip install -e .
```

## Quickstart

```bash
# List all skills under a directory
agent-skills list ./examples --format json

# Inspect one skill
agent-skills inspect ./examples/pdf-processing --format json

# Validate all skills and fail on warnings in CI
agent-skills validate ./examples --format json --fail-on-warning
```

## CLI reference

### Global options

- `--format text|json`: output format (`text` by default)
- `--output <path>`: write output to file instead of stdout

### Commands

- `list <path>`: discover all `SKILL.md` files and print summaries
- `inspect <path>`: parse one skill directory or one `SKILL.md`
- `validate <path>`: validate one skill or all skills under a directory
  - `--fail-on-warning`: non-zero exit if warnings are present

### Examples

```bash
agent-skills --format text list ./examples
agent-skills --format json inspect ./examples/docx-authoring > inspect.json
agent-skills --format json validate ./examples --output reports/validation.json
```

## Python API

```python
from agent_skills import (
    discover_skills,
    inspect_skill,
    validate_skill,
    validation_to_payload,
)

skills = discover_skills("./examples")
doc = inspect_skill("./examples/json-schema-validation")
result = validate_skill("./examples/json-schema-validation")

payload = validation_to_payload([result])
print(payload[0]["valid"])
```

## Architecture

The package is intentionally split into stable layers:

- `models`: typed data contracts shared by all layers
- `parser`: robust frontmatter + markdown extraction
- `validator`: compliance + quality checks
- `discovery`: recursive skill discovery
- `service`: convenience entry points for apps
- `reporting`: output serializers for API/CLI integration
- `cli`: operator-facing command interface

See `docs/architecture.md` for details.

## Example skills

The repository includes multiple styles of skills:

- `examples/pdf-processing` (document extraction)
- `examples/docx-authoring` (document generation workflow)
- `examples/json-schema-validation` (JSON validation pipeline)
- `examples/json-transform-pipeline` (JSON transformation and export)
- `examples/api-contract-testing` (API contract checks)

## Quality and testing

```bash
pytest -q
```

The project targets Python `3.10+`.

## Documentation index

- `docs/architecture.md`: architecture and extension strategy
- `docs/usage.md`: practical API/CLI usage
- `docs/skill-authoring.md`: authoring rules and quality checklist
