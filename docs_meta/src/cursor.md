# Cursor 规划

原则见仓库根 `readme.md`。职责表见 `roles.md`。本文只写**这个 harness 怎么落**。
`.cursor/` 已经开始落；哪几份在盘上见下面「目标文件」那张清单；没落的那几份，落之前仍在这里对齐。不铺进宿主工作区。

默认坐**规划席**。读合同、写卡、对账、拒超售。改核走另一会话里的实现席（Claude Code 规划见 `claude-code.md`）。
席可以换，两席必须两个会话——这一条在 `readme.md`，这里不重复。

## 目标文件（→ harness）

```text
AGENTS.md                      与 Claude Code 共用的短锁
.cursor/rules/switches.mdc     本桌开关的唯一现态；alwaysApply: true；两席共用，不是规划席专属
.cursor/skills/
  cursor-desk/SKILL.md         规划席默认：写文档，不改核
  example-report/SKILL.md      算例报告公式；与 Claude 侧同名 skill 同一口径
```

不另开「用户指南」。从哪启动、第一段贴什么，写进 `CLAUDE.md` 头几行（`init` 铺到宿主上的锁），不写进 `docs/`。

## `cursor-desk` 要锁住的

默认可写：`docs/`（含在办、合同、交付）、`research/`、`examples/` 的叙述与图、`.tmp/`。

要用户点名才动：`src/`、`tests/`、派 builder / tester / 审查、commit / push、对照材料。

用户说「继续推进」只够写卡或改文档，打不开 `src/`。改核必须点名 `src/`、一刀、或「按卡片做」。

写卡按 `write-cmd` 的口径：**新增** `PROMPT_xx.md`、**覆盖** `SESSION.md`——两份都要出，写完停。本窗口不接着改核。

不要把规划席的自我说明写进 `SESSION.md`——SESSION 是本刀卡片，下一刀整篇覆盖。

## 和 Claude Code 的接口

不是互读聊天。接口是在办层三份文件：`docs/TODO.md`、`docs/SESSION.md`、`docs/cmd/PROMPT_*.md`。
对账读落盘产物（卡片、diff、`.tmp/`、报告）。

规划席写报告（`docs/reports/`）发生在领班收口之后；实现席不擅自写「通过」。

## 从三桌提取时要丢掉的

- `29` 的 `cursor-desk` 里「正式图可写 `docs/figures/`」：公共层禁止 `docs/figures/`，图进各层自己的 `figures/`。
- Cursor 窗口不落 builder / tester / 审查的 agent 文件。那些是实现席的机械隔离，见 `claude-code.md`。
- 课题锁不进公共 `cursor-desk`。

## 未决

`.cursor/rules/` 要不要再加一页短锁，还是 skill 够用——技能文件没落之前先不铺。
