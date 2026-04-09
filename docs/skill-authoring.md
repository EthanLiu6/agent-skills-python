# Skill Authoring Guide

## Required fields

Each `SKILL.md` must include YAML frontmatter:

- `name` (required)
- `description` (required)

Recommended optional fields:

- `compatibility`
- `metadata`
- `allowed-tools`

## Naming constraints

- max 64 chars
- lowercase letters, digits, hyphen
- no leading/trailing hyphen, no consecutive hyphens
- must match parent folder name

## Description quality

Descriptions should include:

- what the skill does
- when to use it (`Use when ...`)
- task keywords for discovery

## Maintainability checklist

- keep `SKILL.md` concise (prefer under 500 lines)
- split large content into referenced files
- use clear section headings
- keep file references shallow and explicit

## Security checklist

- treat third-party skills as untrusted code
- review scripts and external data usage
- avoid leaking sensitive inputs in scripts/logs