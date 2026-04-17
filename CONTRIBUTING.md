# Contributing to dao-genesis

感谢你愿意为 dao-genesis 做贡献。本仓库聚焦“技能规范与可复用资产”，欢迎提交对 Prompt、Schema、文档与多平台追踪策略的改进。

## 贡献范围

- `src/system-prompt.md`：系统提示词优化（更稳定、更低 Token、更可解释）
- `src/memory-schema.json`：数据结构演进、向后兼容与迁移规则补充
- `docs/`：更清晰的文档、示例、FAQ、最佳实践
- `.github/workflows/`：CI 校验与基础质量门禁

## 提交规范

- 请优先创建 Issue 描述问题/动机，再提交 PR
- PR 描述需包含：变更动机、兼容性影响、如何验证
- 任何破坏性改动必须：
  - 更新 Changelog
  - 提供兼容层/迁移策略
  - 增加回归验证说明

## 数据与隐私

请勿在本仓库提交真实业务复盘数据（`.storage/`）。如需提供示例，请进行脱敏，并确保不包含任何密钥、账号、内部链接、客户信息等敏感内容。

