# 架构说明

## 设计目标

本项目优先保证三点：

- 稳定性（适合持续集成与自动化）
- 可扩展性（便于加规则和加输出渠道）
- 可维护性（模块职责清晰、改动成本低）

## 模块分层

- `agent_skills.models`
  - 核心数据结构（`SkillDocument`、`ValidationResult` 等）
- `agent_skills.parser`
  - 解析 `SKILL.md` 的 frontmatter 和 markdown 正文
  - 抽取标题和文件引用
- `agent_skills.validator`
  - 规则校验与最佳实践告警
- `agent_skills.discovery`
  - 递归发现 `SKILL.md`
- `agent_skills.service`
  - 对业务侧提供统一接口（inspect/validate/discover）
- `agent_skills.reporting`
  - 统一输出 payload，便于 CLI 与 API 复用
- `agent_skills.cli`
  - 命令行入口、参数处理和退出策略

## 可扩展建议

- 在 `validator` 增加企业自定义规则
- 在 `reporting` 增加 HTML/Markdown 报告输出
- 在 `cli` 增加更细粒度命令（如 stats/profile）