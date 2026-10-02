# PROMPT_051 · 7.1 门口五件——发行准备

| | |
|---|---|
| **本刀是 TODO 哪一行** | `todo.md` `7.1`。人 2026-09-27 立案（原话逐字在行内）；2026-10-02 序列 #4 |
| **状态** | 第 1 稿。LICENSE 已由人当回合裁定（原话「MIT」）——发授权落槌在案 |
| **落槌来源** | 人 2026-10-02 序列授权；LICENSE 裁定同回合原文「MIT」 |
| **前置，满足了** | `6.24` 已结案（`bce0e0e`） |
| **档位** | 重。本刀不改档位的值 |
| **谁来建造** | `builder` 落门口五件；**领班**跑格、派审查、收口 |
| **举证谁跑** | 实现席跑格，日志落 `/d/tmp/051-*.log`（树外） |
| **独立审查** | 派——发行件，错一字就是门外的事故 |
| **写到哪几处** | ①`LICENSE`（新，MIT）；②`.gitignore`（已提前落，复验）；③`readme.md` 换 `<母本仓库地址>` 为真地址（**待人给地址**）；④`.github/ISSUE_TEMPLATE/feedback.md`（新）；⑤`CHANGELOG.md`（新）；⑥记录件 `todo.md`、`SESSION.md` |

## 现状

1. ②已在 `e6b5175` 落（巡查 #1 验过 `git check-ignore -v` 命中仓库行）——本刀只复验。
2. ③的地址是人字段：人未给之前，本刀其余四件先走，③留断点格；地址一到即换（只换这一处字面，不动别的句子）。
3. CHANGELOG 版本号 `v0.1.0`（材料 §2.5 建议）；打 tag、push、GitHub 上点 release 三样是人的动作，本刀不交（不 push 铁律）。

## 验收命令（工作目录 = 项目根；bash 用 `D:\Tools\Git\bin\bash.exe`）

| 格 | 命令 | 应当读到 |
|---|---|---|
| 1 | `git ls-files LICENSE .github/ISSUE_TEMPLATE/feedback.md CHANGELOG.md` | 三行齐（add 后） |
| 2 | `git check-ignore -v .claude/settings.local.json` | 命中仓库 `.gitignore` 行 |
| 3 | `head -3 LICENSE` | 首行 `MIT License`；含 `Copyright (c) 2026` |
| 4 | `grep -c '现象' .github/ISSUE_TEMPLATE/feedback.md`；同文件 `grep -c '出处'`、`grep -c '该改的地方'` | 各 `1` |
| 5 | `grep -c 'v0.1.0' CHANGELOG.md`；`grep -c 'MIT' CHANGELOG.md` | `1`；`≥1` |
| 6 | `grep -c '<母本仓库地址>' readme.md` | **待人地址后**：`0`（地址未到时此格留断点记录） |
| 7 | `bash docs_meta/tests/run.sh` | `跑了 18 本`；`ALL PASS`；`0` |
| 8 | `git status --porcelain` | ⊆ {LICENSE, feedback.md, CHANGELOG.md(新), readme.md(③后), todo.md, SESSION.md, PROMPT_051.md(新)} |
| 9 | `grep -c 'cmd/PROMPT_051.md' docs_meta/docs/todo.md` | `1` |

## 不交什么

- 不打 tag、不 push、不在 GitHub 上点 release（人的动作）；不翻英文页；不动 `docs_meta/src/`；不动帽子与三节。

## 禁令

- LICENSE 文本只许标准 MIT 形＋版权行；判据不因便利放宽；不 push 铁律在本刀同样生效。

## 闸一请示

- 〔爪：发授权〕LICENSE 选型——**人 2026-10-02 已裁「MIT」**，已落。
- 〔爪：待补字段〕③的 GitHub 仓库地址——人到即换，不阻塞其余四件。
