# PROMPT_081 · 6.22 转译坑续块——坑一~四、六修法五点落正身

| | |
|---|---|
| **本刀是 TODO 哪一行** | `todo.md` `6.22`：转译层机械保护——坑一~四、六修法五点（反馈建议 11） |
| **状态** | 第 1 稿 |
| **落槌来源** | 队列 #44（硬化批授权，人签批排 #39 前）；反馈建议 11 修法原文 |
| **前置，满足了** | 侦察在案（run 2bd7e3e7：五点全未落、6.22 甲乙丙三块旁路防重、5.23 两指针不在坑一锚点） |
| **档位** | 重——动条文＋先读顺序（正身在根锁）。本刀不改档位的值 |
| **谁来建造** | **codex exec（值日首演）**：领班写卡发牌，codex 吃牌施工，subagent 备胎 |
| **独立审查** | 派三只并行手 |
| **写到哪几处** | ①`workflow.md`（坑一半句＋17 节计数行）；②`naming.md`（坑四总则句）；③`claude-code.md`/`cursor.md`/`roles.md`/`directory.md`（坑三兜底行五张表＋坑二计数行）；④根 `CLAUDE.md`＋`directory.md`（坑六第五档同刀同步）；⑤`CHANGELOG.md`（残留偏差记一笔）；⑥记录件 |

## 裁定（卡上定死）

1. **坑一**：`workflow.md:170`「一次只做未勾的一行」句尾补「（占位行除外：它不是一刀，见「TODO 只能长」那一节。）」——落 :170，不落 :139/:127/:448（后两者 5.23 已有指针，再加即重复）。根 `CLAUDE.md:58` 产物侧随下次重编跟，本刀不动。
2. **坑二（计数式）**：全部 17 个「（→ harness）」标记节（workflow 9／directory 2／roles 2／verify 2／claude-code 1／cursor 1，行号以侦察表为准、施工时现算核对）节尾各加一行：「本节共 n 条可转译项（条＝bullet 或表格数据行，计数时点 2026-10-06）」。n 由施工时按定义实数。
3. **坑三（兜底行）**：五张转译用查找表末行各加：「｜以上都不匹配 → 停，回出处，或问人；不许挑最近的一条套用」（表格则加为末行，清单则加为末条）——`claude-code.md` 目标文件清单、`cursor.md` 目标文件清单、`roles.md` 公共角色表、`roles.md` 模型下限表、`directory.md` 六块表。
4. **坑四**：`naming.md:68-71` 转译总则段尾补一句正身：「**转译没写不等于出处没写**；转译盖不住的输入一律回出处，不许挑最近的一条套用。」现有总则只管矛盾，此句补缺失那一半。
5. **坑六（第五档，同刀同步）**：根 `CLAUDE.md` 先读顺序补第五档「维护在办层文件先读 `directory.md` 那张寿命表——只补通往出处的路，不复制内容」；`directory.md:157-160` 同步（该节自注「锁在 CLAUDE.md」，正身在产物）。此档落地后 `directory.md:216`「五档」自洽。
6. **载体归 #40**：原修法「收进换根/init 检查单」的载体（换根已摒弃、init 无清单结构）**本刀不造**，归 #40（5.20 宿主无关层清单）同刀立——坑三兜底行的形状机检也随彼刀。`workflow.md:270`「换根带走」残留偏差本刀不治，CHANGELOG 记一笔。

## 验收命令（bash 用 Git Bash）

| 格 | 命令 | 应当读到 |
|---|---|---|
| 1 | `bash docs_meta/tests/run.sh` | `20 本`；无 FAIL |
| 2 | `rg -c '占位行除外' docs_meta/src/workflow.md` | 1 |
| 3 | `rg -c '本节共.*条可转译项' docs_meta/src` | 17 |
| 4 | `rg -c '以上都不匹配' docs_meta/src` | 5 |
| 5 | `rg -n '转译没写' docs_meta/src/naming.md` | 1；`rg -n '维护在办层' CLAUDE.md docs_meta/src/directory.md` | 两处各 1 |
| 6 | `git status --porcelain` | ⊆ {workflow.md, naming.md, claude-code.md, cursor.md, roles.md, directory.md, verify.md, CLAUDE.md, CHANGELOG.md, todo.md, SESSION.md, PROMPT_081.md(新), queue.md} |

## 不交什么

- 不动 6.22 甲乙丙三块旁路（naming:73／directory:216／workflow:408）与 5.23 两指针；不动产物侧除坑六第五档外的一切（随重编跟）；不造检查单载体；不动 `.mirror/`。

## 禁令

- 计数行只数不改：节内既有文字一字不动；n 按定义实数，不凑整不估算。
- 兜底行是末行，不插表中间；五张表外不加。

## 闸一请示

（无。行判据在行内；五点是收紧转译保护，不松任何判据；载体延展已注 #40。）
