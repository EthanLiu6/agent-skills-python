# Usage Guide

## 1) Install

```bash
pip install -e ".[dev]"
```

## 2) CLI usage

### Discover skills

```bash
agent-skills --format text list ./examples
```

### Inspect one skill

```bash
agent-skills --format json inspect ./examples/docx-authoring
```

### Validate skills in CI mode

```bash
agent-skills --format json validate ./examples --fail-on-warning
```

### Write validation report to file

```bash
agent-skills --format json validate ./examples --output reports/validation.json
```

## 3) Python API usage

```python
from agent_skills import discover_skills, inspect_skill, validate_skills

skills = discover_skills("./examples")
print(f"discovered={len(skills)}")

doc = inspect_skill("./examples/json-transform-pipeline")
print(doc.metadata.name, len(doc.file_references))

results = validate_skills("./examples")
print(sum(1 for r in results if r.valid), "valid skills")
```
