---
name: json-transform-pipeline
description: Transform nested JSON records into normalized analytics-ready tables and export snapshots. Use when users ask for JSON flattening, normalization, or ETL-style transformations.
metadata:
  domain: json-etl
  level: advanced
allowed-tools: Read Bash(python:*) Write
---

# JSON Transform Pipeline

## Workflow
1. Parse source JSON batches.
2. Normalize with mapping defined in `references/MAPPING_RULES.md`.
3. Export intermediate and final outputs.

## Scripts
Run transformation script:
scripts/transform.py
