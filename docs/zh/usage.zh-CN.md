# 使用指南

## 1) 安装

```bash
pip install -e ".[dev]"
```

## 2) CLI 使用

### 列出 skill

```bash
agent-skills --format text list ./examples
```

### 查看 skill 详情

```bash
agent-skills --format json inspect ./examples/docx-authoring
```

### 校验并用于 CI

```bash
agent-skills --format json validate ./examples --fail-on-warning
```

### 输出到文件

```bash
agent-skills --format json validate ./examples --output reports/validation.json
```

## 3) Python API

```python
from agent_skills import discover_skills, inspect_skill, validate_skills

skills = discover_skills("./examples")
doc = inspect_skill("./examples/json-transform-pipeline")
results = validate_skills("./examples")
print(len(skills), len(results))
```
