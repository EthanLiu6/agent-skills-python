# Architecture

## Goals

The architecture prioritizes three traits:

- Stability for repeated CI/CD and automation usage
- Extensibility for custom checks and output integrations
- Operational simplicity for developers and agent operators

## Module design

- `agent_skills.models`
  - Core typed contracts (`SkillDocument`, `ValidationResult`, etc.)
  - Isolates data schema from implementation details
- `agent_skills.parser`
  - Parses `SKILL.md` frontmatter and markdown body
  - Extracts headings and relative file references
- `agent_skills.validator`
  - Enforces required fields and naming constraints
  - Provides warning-level quality checks for maintainability
- `agent_skills.discovery`
  - Recursively finds `SKILL.md` files
  - Builds summary objects for skill registries
- `agent_skills.service`
  - High-level API for app integration (`inspect`, `validate`, `discover`)
- `agent_skills.reporting`
  - Converts rich objects into stable payloads and serializations
  - Keeps CLI and API output logic reusable
- `agent_skills.cli`
  - User-facing command interface
  - Handles formatting, output redirection, and process exit policy

## Why this structure scales

- Parser/validator can evolve independently.
- Apps can skip CLI and call `service` directly.
- CI can consume JSON payloads from `reporting`.
- New checks can be added in validator without touching parser.

## Extension points

- Add organization-specific checks in `validator`.
- Add custom output targets by extending `reporting`.
- Add new commands in `cli` without changing service contracts.