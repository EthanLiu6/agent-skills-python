# agent-skills-python

独立的 Agent Skills Python 工具包项目目录，导包名为 `agent_skills`。

## 安装

```bash
pip install -e ".[dev]"
```

## CLI

```bash
agent-skills list ./examples --json
agent-skills inspect ./examples/pdf-processing --json
agent-skills validate ./examples --json
```

## Python API

```python
from agent_skills import discover_skills, inspect_skill, validate_skill

skills = discover_skills("./examples")
doc = inspect_skill("./examples/pdf-processing")
result = validate_skill("./examples/pdf-processing")
```
