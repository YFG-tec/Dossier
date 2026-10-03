# PROMPT_054 · `.mirror/` 加 `.codex/` 编译目标——角色落点 TOML 化

| | |
|---|---|
| **本刀是 TODO 哪一行** | `todo.md` `5.7`（本刀新立，代理席日常裁定）：`.mirror/` 加 `.codex/` 兄弟落点，编译器多一个目标 |
| **状态** | 第 1 稿 |
| **落槌来源** | 人 2026-10-02 定「那就用codex吧」＋序列授权（`queue.md` #3）；`later.md` 附三§六 早画好这条路 |
| **前置，满足了** | Codex CLI v0.153.4 在机；`~/.codex/` 配置体系在（config.toml/sessions/skills 齐活） |
| **档位** | 重（动 `src/` 一份＋检查两本＋`.mirror/` 扩容）。本刀不改档位的值 |
| **谁来建造** | `builder` 四处落件；**领班**跑格、派审查、收口 |
| **独立审查** | 派——动 `src/` 与两本检查 |
| **写到哪几处** | ①`docs_meta/src/claude-code.md`（目标文件清单加 `.codex/` 三行）；②`.mirror/.codex/agents/` 四份 TOML（builder/contract-tester/review/spec-guard）；③`docs_meta/tests/check-mirror.sh`（清单 11→15 件）；④`docs_meta/tests/check-role.sh` 若射程需扩（TOML 无 `tools:` 行——D 段认形需认 TOML 的工具字段）；⑤记录件 |

## 现状（builder 会踩的）

1. **Codex 子代理形**：`~/.codex/agents/*.toml`，字段 `name/description/instructions/model`（公开场一致口径）；工具面走 `config.toml` 的 sandbox/approval，不逐 agent 写 tools 白名单——**TOML 版把「工具面」一段改写为指向 Codex 的 sandbox 说明**，不硬造 `tools:` 行。
2. `check-role` C 段认 `*agents/` 目录下 `tools:` 行——TOML 落点没有这行会 BAD。**D 段同理**。改法：认形扩为「`.md` 查 `tools:`、`.toml` 查 `[agent]` 或 `instructions` 字段」——具体以实际 TOML 形状定，卡上不冻结细节，审查复认。
3. `check-mirror` 清单 11 件钉死、总数恰好 11——加 4 份 TOML 后改 15；占位符 `{{DOSSIER_SRC}}` 同款置换；LF 入库（E 段量 blob 形）。
4. `{{DOSSIER_SRC}}` 置换由 `init.py` 现有机制走，不动 init。
5. `.codex/` 落点里 AGENTS.md 通用入口已存在（Codex 原生读仓库根 AGENTS.md）——`.mirror/AGENTS.md` 已有，**不重复造**；本刀只落 agents 四份＋`claude-code.md` 清单三行（清单里 `.codex/` 段）。

## 交什么（要点冻结）

1. `claude-code.md`「目标文件」code block 加三行：`.codex/agents/builder.toml` 等四份里的三份（spec-guard 是否落 Codex 同款——落，四份全）；
2. 四份 TOML：字段 name/description/instructions；instructions 正文从 `.claude/agents/*.md` 同源搬运（只许动/不许动/红了许做什么三段＋出处指 `{{DOSSIER_SRC}}/roles.md`），工具面段改写为 Codex sandbox 口径；
3. `check-mirror.sh`：EXPECTED_FILES 加四行、总数 11→15；
4. `check-role.sh`：C/D 段认 TOML 形（`.toml` 结尾查 `instructions` 或 `[` 字段行，不查 `tools:`）；
5. todo 立 5.7 行＋指针。

## 验收命令（bash 用 `D:\Tools\Git\bin\bash.exe`）

| 格 | 命令 | 应当读到 |
|---|---|---|
| 1 | `ls .mirror/.codex/agents/` | builder.toml contract-tester.toml review.toml spec-guard.toml 四份 |
| 2 | `grep -c 'instructions' .mirror/.codex/agents/*.toml` | 各 ≥1 |
| 3 | `grep -c 'roles.md' .mirror/.codex/agents/builder.toml` | ≥1（出处指针在） |
| 4 | `bash docs_meta/tests/check-mirror.sh` | `15 件`；`ALL PASS`；`0` |
| 5 | `bash docs_meta/tests/check-role.sh` | `ALL PASS`；`0` |
| 6 | `bash docs_meta/tests/run.sh` | `18 本`；`ALL PASS`；`0` |
| 7 | `python docs_meta/src/init.py --check`（若 init 有 check 形；无则跑 init 后 `git status` 验占位符置换不破） | 不红 |
| 8 | `git status --porcelain` | ⊆ {claude-code.md, 4×toml, check-mirror.sh, check-role.sh, todo.md, SESSION.md, PROMPT_054.md(新)} |
| 9 | `grep -c 'cmd/PROMPT_054.md' docs_meta/docs/todo.md` | `1` |

## 不交什么

- 不动 `.claude/` 既有五件；不动 `init.py`；不删任何既有落点；不做 Codex 实测（下一刀）；
- 不把 TOML 正文写成第二定义——出处仍指 `roles.md`。

## 闸一请示

（无。人已定用 Codex；日常裁定授权在案。）
