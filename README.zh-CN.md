# agent-skills-python

[English](README.md) | 简体中文

`agent-skills-python` 是一个面向生产的 Agent Skills 工具包，帮助 Python Agent
或自动化平台快速接入 Skill 能力。导包名为 `agent_skills`。

## 版本

- 当前版本：`v0.1.1`

## 核心能力

- 解析 `SKILL.md`（frontmatter、正文、标题、引用文件）
- 按规范校验 skill（错误 + 告警）
- 递归发现并列举 skills
- 输出结构化 JSON，便于 CI 和系统集成

## 安装

### 开发安装

```bash
pip install -e ".[dev]"
```

### 运行安装

```bash
pip install -e .
```

## 快速开始

```bash
# 列举目录中的 skill
agent-skills list ./examples --format json

# 查看单个 skill 详情
agent-skills inspect ./examples/pdf-processing --format json

# 校验所有 skill，并在告警时返回非 0（CI 模式）
agent-skills validate ./examples --format json --fail-on-warning
```

## CLI 参数

### 全局参数

- `--format text|json`：输出格式（默认 `text`）
- `--output <path>`：输出写入文件

### 子命令

- `list <path>`：发现并列举所有 `SKILL.md`
- `inspect <path>`：解析单个 skill 目录或 `SKILL.md`
- `validate <path>`：校验单个或批量 skill
  - `--fail-on-warning`：出现 warning 也返回非 0

## Python API 示例

```python
from agent_skills import discover_skills, inspect_skill, validate_skill

skills = discover_skills("./examples")
doc = inspect_skill("./examples/json-schema-validation")
result = validate_skill("./examples/json-schema-validation")
print(result.valid)
```

## 文档索引

- `docs/architecture.md` / `docs/zh/architecture.zh-CN.md`
- `docs/usage.md` / `docs/zh/usage.zh-CN.md`
- `docs/skill-authoring.md` / `docs/zh/skill-authoring.zh-CN.md`
