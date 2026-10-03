# PROMPT_059 · 状态一致性对账——三面分叉检查入 run.sh

| | |
|---|---|
| **本刀是 TODO 哪一行** | `todo.md` `5.10`（本刀新立，代理席日常裁定；人点名三部分之二） |
| **状态** | 第 1 稿 |
| **落槌来源** | 人 2026-10-02「ok，先把这三部分做完」；外部报告 §3.3（三状态面分叉） |
| **前置，满足了** | 5.9 结案；谓词（check-verdict）已会读 SESSION 行号与卡号——本刀是它「对账面」的扩展 |
| **档位** | 重（新检查本，本数 19→20）。本刀不改档位的值 |
| **谁来建造** | `codex exec`（执行席常态第三刀）；**领班**写卡、跑格、审查、收口 |
| **独立审查** | 派 |
| **写到哪几处** | ①新 `docs_meta/tests/check-sync.sh`（第 20 本）；②`docs_meta/src/tools/close_cut.py`（一处小改：queue 行不存在时的 FAIL 文案带上提示「先在 queue 登记本刀」）；③记录件 |

## 现状（builder 会踩的）

1. **三面**：SESSION 横线以上（点的行＋许可面卡号）、todo（该行勾选态＋已办指针）、queue（该刀状态格）。分叉形：①SESSION 说在办、todo 已勾（半推进）；②queue 标在办但 SESSION 指着另一刀；③todo 行已勾但已办区无指针；④queue 双「在办」（今天真实撞过）。
2. **判定的「无刀态」**：SESSION 上半页没有 `cmd/PROMPT_` 指针（刀间歇）→ 四段全 SKIP 不红（合法静默）。谓词 v1 同款哲学：宁可放过间歇，不许误伤空场。
3. check-verdict 与本刀分工：verdict 答「这一刀走到哪一档」（结案判定用）；sync 答「三个状态面说的是不是同一刀」（对账用）。两本并存不合并。
4. close_cut 小改动机：本刀收口时刚撞过「queue 无行 FAIL」——文案升级让下一个撞的人知道怎么办。

## 交什么

1. `check-sync.sh` 四段：
   - A **有刀态判定**：SESSION 上半页取行号（「点的行」格首个 X.Y）与卡号（唯一 `cmd/PROMPT_NNN` 指针）；取不到 → SKIP 全本（印「刀间歇，四段跳过」），退出 0；
   - B **SESSION↔todo**：该行号在 todo 为未勾 → 要求 SESSION 状态格非「已结案」类字样；已勾 → 要求已办区有该卡指针且 SESSION 状态含结案字样；违者 FAIL；
   - C **SESSION↔queue**：queue 中该行号（或其文字）所在行状态格；「已结」时 SESSION 应含结案态；「在办」时卡号应与 SESSION 卡号一致；「挂起/断点/排队」时 SESSION 若指它则 FAIL（挂着却占着 SESSION）；
   - D **queue 单在办**：queue 全表「在办」行数 ≤1，>1 FAIL 点名各行。
2. close_cut 的 queue FAIL 文案改为：`FAIL: queue.md 没有 #<n> 行——先在 queue.md 登记本刀再收口`。

## 验收命令（bash 用 `D:\Tools\Git\bin\bash.exe`）

| 格 | 命令 | 应当读到 |
|---|---|---|
| 1 | `bash docs_meta/tests/check-sync.sh` | 当前刀间歇 → `刀间歇，四段跳过`；退出 `0` |
| 2 | `bash docs_meta/tests/run.sh` | `跑了 20 本`；`ALL PASS`；`0` |
| 3 | `python docs_meta/src/tools/close_cut.py 9.9 099 --dry-run` | FAIL 文案含「先在 queue.md 登记本刀」；退出 `1` |
| 4 | 造红（沙箱）：`bash docs_meta/tests/check-sync.sh` 对临时夹具（LINK_ROOT 形，参照 check-link 的 ROOT 开关）造「双在办」样本 → FAIL 复现 → 还原 | FAIL 点名两行 |
| 5 | `git status --porcelain` | ⊆ {check-sync.sh(新), close_cut.py, todo.md, SESSION.md, PROMPT_059.md(新), queue.md} |
| 6 | `grep -c 'cmd/PROMPT_059.md' docs_meta/docs/todo.md` | `1` |

## 不交什么

- 不改 check-verdict 判定逻辑；不动 workflow 条文（对账规则住检查本头注，出处指本卡）；不做三面自动修复（只红不修——修是 close_cut 和人的事）。

## 禁令

- 刀间歇必须全 SKIP 不红；任何「空场假红」即断点。

## 闸一请示

（无。人点名；报告 §3.3 在案。）
