# PROMPT_043 · 6.8 改了横线以上，没有必跑的结构本

| | |
|---|---|
| **本刀是 TODO 哪一行** | `todo.md` `6.8`。第 6 章队列 `6.2`–`6.7` 之后下一名，人 2026-09-25 点行 |
| **状态** | **第 2 稿。规划席审卡点名格 3 与抄件路径（`spec-guard/SKILL.md`→`agents/spec-guard.md`），已修正。停在闸一前，等印第 1 版。** 本阶段 `check-gate` 红（版次 0）与 `check-link` D 段红是设计，落印自绿 |
| **落槌来源** | 人 2026-09-25：「写6.8卡」。本席荐 6.8（理由：今天 6.12 现形两回——第二指针与 A 段字段名，全是同一失效类；4.10 审查意见 1 已上架；3.5 跟稿时又踩一次） |
| **这一行怎么来的** | 4.10 审查意见 1 收件，3.5 跟稿时再踩，今天 6.12 现形两回。三次同形：改 SESSION 上半页后没当场重跑结构本，红了由下一趟撞见 |
| **前置，满足了** | 无依赖行。`6.12` 已结案（`48cd1b5`） |
| **档位** | 重。本刀不改档位的值 |
| **谁来建造** | 三只手：`builder` 改 `workflow.md` 收口纪律加一条硬格；**领班**改两份 skill（`write-cmd`、`spec-guard`）加同一条；`contract-tester` 不加新本（既有 `check-link`/`check-gate` 已够）；**领班**跑全部格、派审查、收口 |
| **举证谁来跑** | 实现席自己跑；日志落 `/d/tmp/043-*` |
| **独立审查** | 派——本刀动 `src/`（`workflow.md` 是母本源码），按 `roles.md` 必派 |
| **写到哪几处** | 三份：①`docs_meta/src/workflow.md`（收口纪律加一条）；②`.claude/skills/write-cmd/SKILL.md`（加一条）；③`.claude/agents/spec-guard.md`（加一条——spec-guard 是 agent 不是 skill，`claude-code.md`:16-19 把 `spec-guard.md` 落在 `.claude/agents/`）。别的不沾 |

## 写卡阶段现算

### 一、三次同形，全是「改完没跑」

- **4.10 审查意见 1**：「改了上半页之后，结构本必跑，不是选跑。」上架货架。
- **3.5 跟稿**：卡上给自己加了补跑格，跟稿时仍把那个字段名写进了页。规矩没进 skill，靠卡上临时写。
- **今天 6.12**：收口前改台账，上半页出现第二处指针（gate/link/ask 三本同因红）+ A 段字段名第三次踩雷。审查用 mtime 链证死是本刀的账。

三次都是同一失效类：改了 SESSION 上半页后没当场重跑结构本。本刀修的是**每一刀都会重犯的失效类**，改动面小（workflow + 两份 skill），回报按刀计。

### 二、修法：三处加同一条硬格

- **`workflow.md` 收口纪律**：加一条——改 SESSION 上半页后必跑 `check-link` 与 `check-gate`，绿了才往下。
- **`write-cmd` skill**：加同一条（写卡那只手每次改 SESSION 必跑）。
- **`spec-guard` skill**：加同一条（spec-guard 只覆盖 SESSION，更要守）。

既有 `check-link` 守 A 段四个字段名 + B 段恰好一处指针 + C 段链接不悬空 + D 段闸一红印 + E 段横线以下无别刀；`check-gate` 守版次连号。两本已够，不加新本。

### 三、动作归纪律，不属机械检查

「改完必跑」这个动作本身不进 `check-*.sh`——动作归 workflow 纪律，机械检查守的是「跑完的结果」（字段名、指针、链接、红印、版次）。本刀只加纪律，不改检查。

### 四、无产品面同步

权限表未被根锁/`.mirror` 任何一句引用（实测零命中），本刀只动母本源码一份文件 + 两份 skill。

## 交什么

### 一 · `docs_meta/src/workflow.md`（builder）

收口纪律那一节（`## 收口纪律（领班收口 = 绿落盘 + 对账）` 之后），加一条硬格，冻结文本：

```markdown
- **改 SESSION 上半页后必跑结构本。** 每次改 `SESSION.md` 横线以上之后，当场跑 `check-link.sh` 与 `check-gate.sh`，两本全绿才往下。红即停，不改完不收口。这一条不是选跑，是硬格——4.10 审查意见 1 上架、3.5 跟稿再踩、6.12 现形两回，三次同形。
```

只加这一条；收口纪律其余一字不动。

### 二 · `.claude/skills/write-cmd/SKILL.md`（领班）

加一条，冻结文本：

```markdown
- **改 SESSION 上半页后必跑结构本。** 每次改 `SESSION.md` 横线以上之后，当场跑 `check-link.sh` 与 `check-gate.sh`，两本全绿才往下。红即停，不改完不收口。
```

只加这一条；skill 其余一字不动。

### 三 · `.claude/agents/spec-guard.md`（领班）

加同一条，冻结文本：

```markdown
- **改 SESSION 上半页后必跑结构本。** 每次改 `SESSION.md` 横线以上之后，当场跑 `check-link.sh` 与 `check-gate.sh`，两本全绿才往下。红即停，不改完不收口。
```

只加这一条；agent 文件其余一字不动。

### 四 · 记录件（领班，写卡阶段已落）

`todo.md` `6.8` 行下挂指针一行；`SESSION.md` 整篇覆盖（横线以下清零，第六次执行；6.12 各页已随 `48cd1b5` 入库，清零有据）。

## 不交什么

1. 不改 `check-link.sh`、`check-gate.sh`——既有本已够，本刀不加新本。
2. 不改 `SESSION.md`——本刀是改规则，不是改当前刀。
3. 不改 `roles.md`、`claude-code.md`、`cursor.md`、`directory.md`。
4. 不改根锁、`.mirror/`、`init.py`、`run.sh`。
5. 不勾 `6.8`、不写日期、不搬已办；不 commit、不 push、不 `git add`、不动 index。
6. 不碰 `SESSION.md` 横线以下（写卡交接清零除外）。

## 禁令

- 一次只做未勾的一行；不发明新阶段，不顺手并刀。
- 不准自己勾 `todo.md`；结案、发授权、松判据都是人那一爪。
- 判据不许放宽：若施工中发现要放宽任何一格，停，报人。
- 冻结文本逐字落盘，落完与抄件比对；有出入当场停，不改判据去凑盘。
- 不准 commit / push，除非人本回合点名（「结案」二字即 commit 点名，push 另点）。
- `SESSION.md` 横线以下只追加；`.tmp/` 与 `/d/tmp/` 零权威，只作证。

## 施工顺序

1. **领班**基线：盘面（开工现算重数，写卡时 4 行，不拿旧数凑）、`HEAD`、整盘 17 本；三份基线抄件 `/d/tmp/043-base-*`（`workflow.md`、`write-cmd/SKILL.md`、`agents/spec-guard.md`）。
2. **builder** 落 `workflow.md` 收口纪律那一条（冻结文本），落完与抄件逐字比对。
3. **领班**落两份 skill 那一条（冻结文本），落完与抄件逐字比对。
4. **领班**跑格 1–11（含整盘、结构两本）。
5. **领班**派 `review`（先说五件：盘面分账口径；三次同形的账；动作归纪律不属机械检查；既有本已够不加新本；三份文件各加一条）。
6. **领班**收口：重写横线以上、贴审查页、补跑格 12。

## 验收命令，和预先声明的读数

一律仓库根；模式零反引号；`/d/tmp/` 探针跑完留着（证据），验完不进盘账。

| 格 | 命令 | 应当读到 |
|---|---|---|
| 1 | `grep -c '必跑.*check-link.*check-gate' docs_meta/src/workflow.md` | `≥1`（基线 `0`） |
| 2 | `grep -c '必跑.*check-link.*check-gate' .claude/skills/write-cmd/SKILL.md` | `≥1`（基线 `0`） |
| 3 | `grep -c '必跑.*check-link.*check-gate' .claude/agents/spec-guard.md` | `≥1`（基线 `0`） |
| 4 | `bash docs_meta/tests/check-link.sh; echo $?` | `0`（本刀不改 SESSION，check-link 维持现状） |
| 5 | `bash docs_meta/tests/check-gate.sh; echo $?` | `0`（本刀不改 SESSION，check-gate 维持现状） |
| 6 | `bash docs_meta/tests/run.sh; echo $?` | `0`；「跑了 17 本」；`ALL PASS`（本数不涨——不加新本） |
| 7 | `git diff --name-only -- docs_meta/src` | 仅 `workflow.md` 一份 |
| 8 | `git diff --name-only -- .claude` | 恰 2 份（`skills/write-cmd/SKILL.md`、`agents/spec-guard.md`） |
| 9 | `git rev-parse --short HEAD`；`git diff --cached --name-only` | 第 1 步记录值（写卡时 `48cd1b5`）；空 |
| 10 | `wc -l < docs_meta/src/workflow.md` | 基线行数 + 2（冻结文本两行：一条正文 + 一条空行分隔） |
| 11 | `python -c "t=open('D:/tmp/043-frozen-wf.txt',encoding='utf-8').read().strip(); print(open('docs_meta/src/workflow.md',encoding='utf-8').read().count(t))"` | `1`（冻结文本逐字在盘） |
| 12 | 贴审查页后补跑格 4、5、6 | 同上（039 立的贴页必重跑，续用） |

## 缺口，照记不补

一、这一条只守「改完跑一次」，不守「跑完再改」——改了又撞、撞了又改的循环，纪律补不了。
二、check-link 守的是四个字段名 + 指针 + 链接 + 红印 + 别刀，不守「改完必跑」这个动作本身——动作归 workflow 纪律，不属机械检查。
三、旧桌若没这两份 skill，这一条落不到它身上；新桌按本桌形状铺，自然带上。
四、三份文件各加一条，措辞略有差异（workflow 带三次同形的账，skill 不带）——skill 是操作指令，不带历史；workflow 是纪律，带理由。

## 退卡的条件

- 要同时改 `check-link.sh` / `check-gate.sh` 才能继续——停，报人。
- 要改 `SESSION.md` 才能继续——停，报人。
- 整盘出未预告的红——停，报人。
