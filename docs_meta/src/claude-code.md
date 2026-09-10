# Claude Code 规划

原则见仓库根 `readme.md`。职责表见 `roles.md`。本文只写**这个 harness 怎么落**。
还没落成 `.claude/`；落之前先在这里对齐。`CLAUDE.md` / `AGENTS.md` 已落在仓库根上。换根不带走。

默认坐**实现席**。主会话当领班，自己少写核。规划席默认是 Cursor，见 `cursor.md`。
席可以换，两席必须两个会话——这一条在 `readme.md`，这里不重复。

## 目标文件

```text
CLAUDE.md                      每会话细锁：先读、干活在哪、禁令
AGENTS.md                      同一份锁，写短的
.claude/agents/
  spec-guard.md                只覆盖 SESSION；写完停
  builder.md                   只改卡片「交什么」里的 src/；.tmp/ 探针
  contract-tester.md           只动 tests/；核错了写红测
  review.md                    禁 Write / Edit；只读只跑
.claude/skills/
  write-cmd/SKILL.md           写 PROMPT + 覆盖 SESSION；写完停
  one-slice/SKILL.md           串行顺序；自己不改核
  example-report/SKILL.md      算例报告公式写法；不是角色
```

调度 skill 不是角色。`one-slice` 只规定 `roles.md` 那条顺序。
`31` 的 `tmp-experiment` 是探索模式，对应 `.tmp/` 层，不落成第五个实现角色。

## 轻档 / 重档

| | 轻 | 重 |
|---|---|---|
| 锁 | `CLAUDE.md` + `AGENTS.md` | 同上 |
| 角色文件 | 职责仍按 `roles.md`，不落 agent | 上表四份 agent + 三份 skill |
| 何时 | 核还干净、一刀不易超售 | 改共享离散核、一刀容易超售 |

轻档不是混岗许可证。单会话也要先写卡、停、再改 `src/`、红了先报、审查只读。
文件只是把原则变成机械隔离。旧桌没有义务补文件。

## 从三桌提取时要丢掉的

- `docs/HARNESS.md`：人怎么开工并进桌的 `CLAUDE.md` 头几行，不另开一页。
- 课题锁（四步 API、残差 Riemann、C 核不写化学）：写在各桌自己的「不可以改」里，不抽进公共角色文件。
- `scripts/`、`docs/figures/`、`docs/archive/`、`docs/HARNESS.md`：公共目录已经删了，agent 正文不要再写这些落点。
- 审查禁写：Xenia / `29` 用 `disallowedTools: Write, Edit`。这条进公共层——审查的手不写文件。

## 主会话当领班

tester（及需要时的审查）结束之后、请人勾 TODO 之前：跑卡片里的验收、stdout 落盘、对照「交什么」逐条对账。不 commit、不勾 TODO。详见 `workflow.md`。

## 未决

先落轻档（两份锁），还是规范定稿一次铺到重档——见 `../docs/design/open.md`。
