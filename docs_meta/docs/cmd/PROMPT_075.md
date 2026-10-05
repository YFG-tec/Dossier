# PROMPT_075 · 4.2＋4.3 小修打包——`docs_meta/` 平写同步两层形、公共顶层树注只增不删

| | |
|---|---|
| **本刀是 TODO 哪一行** | `todo.md` `4.2`（主行）＋`4.3`（随刀同结）：naming/directory 里 `docs_meta/` 还写成平的；树注没写只增不删 |
| **状态** | 第 1 稿 |
| **落槌来源** | 队列 #30（第六章小修段）；人 2026-10-06 原话「代理启动，开始开发」＋2026-10-02 常设令「可以继续做一些小修小补」 |
| **前置，满足了** | 两行台账材料齐（`lean-rows.md#4.2/#4.3`）；4.5 已作废（人 2026-10-03 裁）不连带 |
| **档位** | 重——动条文（naming/directory 是源码层条文文件）。本刀不改档位的值 |
| **谁来建造** | 领班亲写（queue #30 注：归领班；workflow.md 现查无平写，本刀不碰） |
| **独立审查** | 派——动条文性质 |
| **写到哪几处** | ①`docs_meta/src/naming.md` 三句；②`docs_meta/src/directory.md` 两处；③记录件 |

## 裁定（卡上定死）

1. **4.2 修法（四处平写改两层形，一句换一句，不加段）**：
   - `naming.md:93`「桌长 `src/` / `tests/` / `.venv/`，母本里没有」已不成立（母本有 `docs_meta/src/`、`docs_meta/tests/`）。改成如实句：同层不长在根上、住 `docs_meta/` 下。
   - `naming.md:94`「`docs_meta/` 是 Dossier 自己怎么写 harness、图标放哪」→ 两层形：`src/` 是规范、工具与图标；`docs/` 是母本自己的在办层。
   - `naming.md:99`「规划先写在 `docs_meta/`」→ `docs_meta/docs/`。
   - `directory.md:144`「`docs_meta/` 是母本自己的规划与品牌」→ 同步两层形。
   - `naming.md:65`、`:88` 两处是整目录归属句（不铺宿主／留在子模块），语义仍真，**不动**。
2. **4.3 修法（树注一条）**：`directory.md`「建议的公共顶层」树后补一行注——`cmd/` 只增不删、卡号从 `000` 起流水永不改名；只给路标（指 `workflow.md`「TODO 只能长」与 todo 页头），不复制公式。
3. **台账过时项处置（卡上记录）**：`lean-rows#4.2` 连带的「无处安放」句已不在盘上（已消）；`#4.3` 的「产品面 7 处＋合同层 2 处旧格式占位符」现查全数落在豁免位（cmd/ 历史卡冻结、`paradigm.md` 思路层引用、todo 页头是规则本体），无占位符残留。
4. **结案形状**：4.2 主行随本卡搬已办（正常一卡一行）；4.3 行不搬、行内不引卡号（严口径整页恰好一次），注「已随本刀施工毕，搬行随 #35 吸收形状」。

## 验收命令（bash 用 Git Bash）

| 格 | 命令 | 应当读到 |
|---|---|---|
| 1 | `bash docs_meta/tests/run.sh` | `20 本`；`ALL PASS`；退出码 `0` |
| 2 | `rg -n '母本里没有' docs_meta/src/naming.md` | 0 命中（旧句已换） |
| 3 | `rg -c '只增不删' docs_meta/src/directory.md` | ≥2（树注新句＋六块表原有） |
| 4 | `bash docs_meta/tests/check-done.sh` | ALL PASS；PROMPT_075 在 todo 整页恰好 1 次 |
| 5 | `git status --porcelain` | ⊆ {naming.md, directory.md, todo.md, SESSION.md, PROMPT_075.md(新), queue.md} |

## 不交什么

- 不动 `naming.md:65/:88` 整目录句；不碰 `workflow.md`（:84 已是新形）；不动 cmd/ 历史卡与 `paradigm.md` 引用；不动已办区（4.4 只追加）；不改 `CLAUDE.md`/`AGENTS.md` 等转译产物（转译另走一刀）。

## 禁令

- 平写修正是把过时句改成如实句，不是重写章节；每处一句换一句。
- 树注只补路标不抄公式，防第二真相。

## 闸一请示

（无。两行判据在行内；修法是同步现状，不松任何判据。）
