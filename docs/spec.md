# dao-genesis Spec

## 技术设计说明书 (Specification)

本文档是 `dao-genesis` 的核心架构设计与功能规范文档。为保证根目录的整洁，完整版 Spec 放置在仓库根目录下的 [review_memory_skill_spec.md](../review_memory_skill_spec.md) 文件中。

### 快速导航

- [1. 技能概述与核心价值](../review_memory_skill_spec.md#1-技能概述与核心价值-overview--core-value)
- [2. 核心系统提示词 (System Prompt) 设计](../review_memory_skill_spec.md#2-核心系统提示词-system-prompt-设计)
- [3. 核心功能与架构设计](../review_memory_skill_spec.md#3-核心功能与架构设计-core-features--architecture)
- [4. Token 消耗优化与上下文控制](../review_memory_skill_spec.md#4-token-消耗优化与上下文控制-token-optimization)
- [5. 跨系统与跨平台集成策略 (含 GitHub/GitLab/AtomGit) ](../review_memory_skill_spec.md#5-跨系统与跨平台集成策略-cross-platform-integration-strategy)
- [6. 最佳实践与实施指南](../review_memory_skill_spec.md#6-最佳实践与实施指南-best-practices--implementation-guide)
- [7. 故障排除与 FAQ](../review_memory_skill_spec.md#7-故障排除与-faq-troubleshooting)
- [8. 版本历史 (Changelog)](../review_memory_skill_spec.md#8-版本历史-changelog)

---
> *如果你希望向本文档提交修改，请遵循 [CONTRIBUTING.md](../CONTRIBUTING.md) 的指引并提交 PR。*

