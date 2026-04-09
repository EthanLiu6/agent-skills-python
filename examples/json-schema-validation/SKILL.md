---
name: json-schema-validation
description: Validate JSON payloads against domain schema rules and generate actionable error reports. Use when users request JSON quality checks, schema compliance, or payload gatekeeping.
compatibility: Requires Python 3.10+ with jsonschema package.
metadata:
  domain: json-data
  level: beginner
allowed-tools: Read Bash(python:*)
---

# JSON Schema Validation

## Workflow
1. Load schema from `assets/schema.json`.
2. Validate payload.
3. Emit structured result with failing field paths.

## References
- [Validation notes](references/VALIDATION_NOTES.md)
