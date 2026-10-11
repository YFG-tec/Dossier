# PROMPT_102 · 5.47 档案目录——todo 只瘦不胖，案卷永不清

| | |
|---|---|
| **本刀是 TODO 哪一行** | `todo.md` `5.47`（人 2026-10-11 原话逐字在行内） |
| **状态** | 第 1 稿（写完停，等「按卡片做」） |
| **落槌来源** | 人 2026-10-11「docs 下面需要一个新的目录，专门处理归档问题，archives？」＋「我觉得是时候处理这个问题了」；材料 `design/archive.md` |
| **前置，满足了** | `design/archive.md` 亲读；`check-done.sh` A/B/C 段现文亲读；`directory.md` 十层表/寿命表亲读；todo.md 全文清点（362 行：开放 ~15、其余闭行三区） |
| **档位** | 重（动 src 条文＋tests＋init＋百行物理搬迁）。本刀不改档位的值 |
| **谁来建造** | 独立 subagent（工牌制） |
| **独立审查** | 事实与结构手第一顺位；账房手第二顺位（专审：搬迁零丢行、每卡恰一次跨并集、编号零改） |
| **写到哪几处** | ①`docs_meta/docs/archives/todo-v0.2.md`（新；首把收 v0.2.0 及之前全部已办＋废除＋退卡留档）②`docs_meta/docs/todo.md`（搬空三区、留开放行＋章头；页首自述改「搬进当代档案页」）③`docs_meta/src/workflow.md`（搬行句＋发布章归档格）④`docs_meta/src/directory.md`（archives/ 入十层表＋寿命表）⑤`docs_meta/tests/check-done.sh`（A/B 改扫 todo＋archives/todo-*.md 并集）⑥`docs_meta/src/init.py`（骨架加 docs/archives/＋一行 README）⑦计数连带（check-skel 等骨架计数现算随刀）⑧根 harness 现算对应行 ⑨记录件 |

## 裁定（卡上定死）

1. **两层制**：todo.md＝工作面（开放行＋章语境）；`archives/`＝案卷层（已办＋废除＋退卡留档，**只增不删、永不清理**）。首把分代线＝v0.2.0（`eaa1f7d`）：该 tag 及之前**全部闭行**归入 `todo-v0.2.md` 一页；tag 之后的已办行（5.36–5.45 等）**随本刀一并归入同页尾段**并注明「2026-10-11 首把连同代内行一次归档」——工作面从刀后起算。
2. **check-done 并集**：A 段（每卡恰一次）与 B 段（行两行限）改扫 `todo.md`＋`archives/todo-*.md` 全档并集；C 段不动。**搬迁前后各跑一次**，读数入 report（前=现绿基线，后=并集绿）。
3. **workflow 两处**：「勾完不删，搬进页末已办」→「勾完不删，搬进**当代档案页** `archives/todo-vX.md`；发布时代更替」；发布章（7.x）加一格「发布刀含归档：当代闭行入档、开新页、todo 重生」。
4. **directory.md**：十层表加 `archives/` 行（记录层；只增不删）；寿命表同步；init 铺面注记。
5. **init**：骨架 `docs/` 下加 `archives/`（含一行 README：档案目录，只增不删）；骨架计数连带（check-skel 等）现算随刀改。
6. **三不动**：僵尸开放行（6.2/6.3/5.6）原位不动；编号零改零重用；旧卡/旧 SESSION 的「todo.md 5.x」引用不回改。
7. **记录件**：todo 5.47 挂卡指针；SESSION 覆盖；queue 新批首行（或直令刀，随点火定）。

## 验收命令（bash 用 Git Bash；日志树外）

| 格 | 命令 | 应当读到 |
|---|---|---|
| 1 | `bash docs_meta/tests/run.sh`（树外日志） | 22 本；ALL PASS（结案时） |
| 2 | 搬迁对账：归档前后**闭行总数**一致（逐行计数，零丢零重）；todo.md 仅剩开放行＋章头，行数 ≈60 级 | report 带前后计数 |
| 3 | `bash docs_meta/tests/check-done.sh` 单跑 | ALL PASS（每卡恰一次跨并集） |
| 4 | `rg -n "当代档案页" docs_meta/src/workflow.md` ＋ `rg -n "archives" docs_meta/src/directory.md` | 命中 |
| 5 | 树外 `init.py --here` | `docs/archives/README.md` 在；骨架计数连带全绿 |
| 6 | `git status --porcelain` | ⊆ 本卡点名处 |

## 不交什么

- 不动僵尸开放行；不预铺 todo-v0.3；不动 5.46；不清理任何已归档内容；不动 .mirror/。

## 禁令

- 档案页只增不删（首把搬运是「搬」不是「复制留双份」——todo 侧必须搬空）；写卡手回避；新句循画风；两稿对得上。

## 闸一请示

（无。目录形与时机系人两句话直接定；首把连同代内行一并归档系领班刀内取舍——理由：v0.2 tag 后已闭九行留工作面无意义，留档反成第二真相源头；呈人可否决。）
