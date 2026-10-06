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

### 刀外落盘记账

- `c1f449b`：text-to-image 的 skill 与命令在刀外提交，其提交文自认 outside the knife commits——记一笔账，不回改（反馈建议 12；2026-10-06 落账，哈希本仓亲核为提交）。
- `workflow.md:270`「换根带走」为 src 残留旧词（换根 2026-09-14 已摒弃，2.8b 判据 src 归零）——既有偏差记档不治，待回流刀（6.22 续块侦察指认，2026-10-06）。
- `4d45ae0`：`design/model-tiers.md`＋`figures/model-tiers.png` 调研稿，刀外提交（空转期调研授权，人 2026-10-02 原话在 `queue.md`；5.26 记账形，2026-10-06 落账）。
- （本笔随账）：`tests/check-skel.sh` 骨架计数 36→37——PROMPT_083 裁定 5 的必然机械连带（init 多铺 `docs/SETUP.md` 一件，幂等末行跟着走）；卡面格 7 立格时漏收该件，台账留痕判刀内连带，不松判据（2026-10-06）。

### 重译分拣（宿主需重译）

- 2026-10-06（5.19/PROMPT_082）：17 转译源节取法入法（span/元数据排除/EOL）＋豁免声明形状出生——宿主侧转译需按 `src/tools/section_stamp.py` 现算比对跟进。

### 许可证

MIT。
