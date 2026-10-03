# PROMPT_060 · 6.13 三张表的权威关系写明——「哪张是出处」一句话裁定

| | |
|---|---|
| **本刀是 TODO 哪一行** | `todo.md` `6.13`：定义层×手的表有三张，正文声称只有一张出处 |
| **状态** | 第 1 稿 |
| **落槌来源** | 人 2026-10-02「ok，先把这三部分做完」（之三 P2 首刀）；细则在 `design/lean-rows.md#6.13` |
| **前置，满足了** | 材料齐；行内三问「三张各有用不必并；那句指准是哪张、另两张什么关系」——本卡裁 |
| **档位** | 重（动两份 src 条文）。本刀不改档位的值 |
| **谁来建造** | `codex exec`（执行席常态第四刀）；**领班**写卡、跑格、审查、收口 |
| **独立审查** | 派——动 src 必派 |
| **写到哪几处** | ①`docs_meta/src/claude-code.md`（那句改准）；②`docs_meta/src/directory.md`（两张表前各加一行身份句）；③记录件 |

## 裁定（卡上定死，Codex 照抄）

三张表的关系一句话：**`roles.md` 公共角色表是唯一权威出处（谁许写什么）；`directory.md` 的两张是视图——权限表是「层×手」投影视景，手×写表是快速查景；视图与出处不一致时改视图不改出处。**

- `claude-code.md` 那句「出处是 `roles.md` 那张表，角色文件不是第二处定义」改为：「**出处是 `roles.md` 公共角色表**——`directory.md` 的权限表与手×写表是它的两张投影视图，不是第二、第三处定义；三处对不上改视图，不改出处。」
- `directory.md` 权限表标题前加一行：「**本表是 `roles.md` 公共角色表的「层 × 手」投影视图（6.13，2026-10-02）**——与角色表不一致时改本表；角色表才是出处。」
- `directory.md` 手×写表（「实现席这一列还要再拆三只手」那张）前加同款一句：「**本表是 `roles.md` 公共角色表的手×写快速视图**——缺行不缺义，新增角色时两处同步加。」
- 顺带把行内点名的「手×写表缺 write-cmd/spec-guard/cursor-desk/领班」**补全四行**（只许动/不许动两列照 `roles.md` 公共角色表抄，失败时列写「写完停」等对应格）。

## 验收命令（bash 用 `D:\Tools\Git\bin\bash.exe`）

| 格 | 命令 | 应当读到 |
|---|---|---|
| 1 | `grep -c '投影视图' docs_meta/src/directory.md` | `2` |
| 2 | `grep -c '投影视图，不是第二、第三处定义' docs_meta/src/claude-code.md` | `1` |
| 3 | 手×写表行数：`awk '/手\*\*写|手×写|三只手/{f=1} f&&/^\|/{n++} END{print n}' docs_meta/src/directory.md` 或直接 `grep -c 'write-cmd' docs_meta/src/directory.md` | `write-cmd` 出现 ≥3（表内补全） |
| 4 | `bash docs_meta/tests/run.sh` | `20 本`；`ALL PASS`；`0` |
| 5 | `git status --porcelain` | ⊆ {claude-code.md, directory.md, todo.md, SESSION.md, PROMPT_060.md(新), queue.md} |
| 6 | `grep -c 'cmd/PROMPT_060.md' docs_meta/docs/todo.md` | `1` |

## 不交什么

- 不并表、不删任何视图；不动 `roles.md` 公共角色表本体（它已是权威，无需改）；不动权限表列结构（5.4 加的代理席列保留）。

## 禁令

- 補进手×写表的四行只许从 `roles.md` 抄，不许发明措辞。

## 闸一请示

（无。行内三问本卡全裁；判据 grep。）
