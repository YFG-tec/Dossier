# Changelog

## v0.1.0 — 2026-10-02（预估结案日）

一套给 AI 编程代理用的流程约束和 harness 配置，第一个公开发行版。

### 这是什么

Dossier 以 git submodule 挂进你的仓库，`init` 在你的仓库根上铺出 `docs/` 骨架、约定文件和角色文件。此后代理按它的规矩干活：一次一刀、两席两会话、验收判据先行、说「通过」必须指得出能复现的证据。

### 这一版有什么

- 两席 + 两闸 + 卡片的全流程（`docs_meta/src/workflow.md`）
- 层 × 手的写权限表与目录权威分层（`directory.md` / `roles.md`）
- 骨架生成器：`python dossier/docs_meta/src/init.py` 铺桌
- 十八本机械把关（`docs_meta/tests/run.sh` 一条入口）
- `.mirror/` harness 一份（Claude Code 形状），开关两席共用
- 序列与代笔的建制：可盖谓词查询（`check-verdict.sh`）、队列授权（`queue.md`）、代理席与蓝印条款

### 没有什么（未实现，不写「下一阶段」）

- 英文全页翻译
- Codex（`.codex/`）落点
- 自动盖章的全自动队列（谓词与立法已就位，序列仍按刀呈报）
- `docs/reports/` 样例

### 已知的坑

见 `docs_meta/docs/todo.md` 第 6 章（历史 bug 攒批区），不复述。36 桌的反馈报告（`docs_meta/docs/reports/dossier-feedback-2026-09-17.md`）收录了十二条实测问题及回流情况。

### 许可证

MIT。
