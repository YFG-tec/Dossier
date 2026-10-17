---
name: conventional-commit
description: 根据实际 diff 拟定约定式提交信息，用于请求提交、写 commit message 或整理提交摘要。
---

# 约定式提交

先读宿主仓库的提交约定和用户授权，宿主约定优先。用 `git status --short`、`git diff --cached` 和 `git diff` 区分已暂存、未暂存及未跟踪工作；需要包含未跟踪文件时读取实际内容。只为本次授权范围内的真实变更拟消息，不把工作区的其他改动算进去。

标题通常为 `type(scope): 摘要`，scope 可省略，摘要可用中文。按主要行为选 type：新能力用 `feat`，修复缺陷用 `fix`；纯文档、重构、测试或维护按宿主约定选 `docs`、`refactor`、`test`、`chore` 等。scope 只在能准确指出模块时添加，摘要说明实际结果。

有必要解释原因、关联 TODO 或补充上下文时再加正文，与标题空一行。确有破坏性变更时，在 type/scope 后加 `!`，或用 `BREAKING CHANGE: 说明` footer 标明不兼容影响。只写有证据的验证结果，不虚构已运行的检查。

简单改动只需标题，不强制长模板、细碎分类或为凑格式拆开同一任务。拟消息不增加提交授权；执行提交仍遵守用户授权和宿主规则，不自动暂存无关工作。

格式来源：[Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/)。
