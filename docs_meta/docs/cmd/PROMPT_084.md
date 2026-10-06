# PROMPT_084 · 5.24 管理类刀派手补格——路径×席表给 harness 件一个格子

| | |
|---|---|
| **本刀是 TODO 哪一行** | `todo.md` `5.24`：管理类刀派手补格：路径×席表加 `.claude/` `.cursor/` 行，管理类刀有手可派（反馈建议 10） |
| **状态** | 第 1 稿 |
| **落槌来源** | 队列 #41（硬化批授权）；反馈建议 10（`reports/dossier-feedback-2026-09-17.md` 第 10 条「管理类刀的派手缺格」；处置节裁：立行） |
| **前置，满足了** | `design/hardening.md` §五 :101 亲读句在案（写权限表无此二行，管理类刀备手为零）；`check-role` 只验 `roles.md` 目标文件清单、`check-sync` 不 parse 本表（亲读两脚本头）；权限表一节不在任何「本节共 N 条」计数节内（亲数） |
| **档位** | 重——动权威条文（`directory.md` 权限表）。本刀不改档位的值；改面小不降档 |
| **谁来建造** | subagent builder（工牌 b1；单行立法件，codex 不派） |
| **独立审查** | 两只并行手（表面／语义） |
| **写到哪几处** | ①`docs_meta/src/directory.md`（路径×席表一行）；②记录件（todo/SESSION/queue） |

## 裁定（卡上定死）

1. **路径×席表补一行**（「一张目录把两席的写权限钉死」节内、`src/` `tests/` 行之后、`.tmp/` 行之前），行文逐字：
   `| \`.claude/\` \`.cursor/\`（harness 件） | 只读 | **卡片点名才动**——管理类刀（harness 活）有手可派：\`builder\` 落件，正身在 \`src/\`，同步随 \`.mirror/\`（5.24） | 只读——经工牌派 \`builder\`，不亲笔 | 写 |`
2. **表后不加散文，不动第二张表**：出处与理由住卡与反馈文件；「手×写快速视图」不触发（无新角色，roles.md 两处同步规则不启动）。本节无计数行（亲数在案），无计数连带。
3. **记录件**：`todo.md` `5.24` 行挂本卡指针；`SESSION.md` 覆盖；`queue.md` #41 状态列。

## 验收命令（bash 用 Git Bash）

| 格 | 命令 | 应当读到 |
|---|---|---|
| 1 | `bash docs_meta/tests/run.sh` | `21 本`；无 FAIL |
| 2 | `rg -n '管理类刀（harness 活）有手可派' docs_meta/src/directory.md` | 恰 1 |
| 3 | `rg -n 'harness 件' docs_meta/src/directory.md` | 恰 1（新行路径列） |
| 4 | `bash docs_meta/tests/check-done.sh` | ALL PASS；PROMPT_084 恰 1 |
| 5 | `git status --porcelain` | ⊆ {directory.md, todo.md, SESSION.md, queue.md, PROMPT_084.md(新)} |

## 不交什么

- 不动「手×写快速视图」、`roles.md`、`workflow.md`；不动 `.mirror/` 与根 harness 件本身（本刀只立格，不落件）；不动本节以外的任何行；不动 `AGENTS.md`。

## 禁令

- 新行五列形状与既有行逐列对齐（路径列反引号包路径；席列沿用「只读／写／卡片点名才动」措辞族）；**不得给代理席开 harness 亲笔写权**——只经 builder。

## 闸一请示

（无。行判据在行内；本刀是给管理类刀补派手格，不松任何判据、不添授权。）
