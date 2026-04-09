---
name: api-contract-testing
description: Validate request and response payload contracts for API endpoints and produce compatibility reports. Use when users request API schema checks, backward compatibility checks, or release contract verification.
metadata:
  domain: api-quality
  level: intermediate
allowed-tools: Read Bash(pytest:*) Bash(python:*)
---

# API Contract Testing

## Workflow
1. Load endpoint contract from `references/CONTRACTS.md`.
2. Validate payload examples in both directions.
3. Summarize breaking changes before release.

## References
- [Contracts overview](references/CONTRACTS.md)
