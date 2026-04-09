# Skill 编写指南

## 必填字段

每个 `SKILL.md` 顶部都需要 YAML frontmatter：

- `name`（必填）
- `description`（必填）

可选字段：

- `compatibility`
- `metadata`
- `allowed-tools`

## 命名规则

- 最长 64 字符
- 只允许小写字母、数字、连字符
- 不允许首尾连字符、连续连字符
- `name` 必须与 skill 所在目录同名

## 描述建议

`description` 应包含两部分：

- Skill 做什么
- 什么时候使用（建议包含 `Use when ...`）

## 可维护性建议

- 主体内容尽量简洁（建议小于 500 行）
- 长内容拆到 `references/`、`assets/`、`scripts/`
- 使用清晰标题，方便模型按需读取

## 安全建议

- 将外部 skill 当作不可信代码审查
- 检查脚本是否存在越权访问和数据泄露风险
- 避免在日志中输出敏感信息