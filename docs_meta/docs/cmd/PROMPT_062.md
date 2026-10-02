# PROMPT_062 · 6.19 permissions 层补格——「名单≠生效、热重载分两型」入条文，守卫随附形状立案

| | |
|---|---|
| **本刀是 TODO 哪一行** | `todo.md` `6.19`：权限名单不是机械边界：在名单上 ≠ 在生效——部分已治 |
| **状态** | 第 1 稿 |
| **落槌来源** | 人 2026-10-02「先把这三部分做完」（之三 P2 第三刀）；细则在 `design/lean-rows.md#6.19` |
| **前置，满足了** | PreToolUse 守卫已在本机用户级（2026-09-23 追记）；本刀把知识层与随附层补上 |
| **档位** | 重（动 `claude-code.md`＋新一行立案）。本刀不改档位的值 |
| **谁来建造** | `codex exec`（执行席常态第六刀）；**领班**写卡、跑格、审查、收口 |
| **独立审查** | 派——动 src 必派 |
| **写到哪几处** | ①`docs_meta/src/claude-code.md`（permissions 层补格一节）；②`todo.md` 新行 5.11（守卫产品化立案）；③记录件 |

## 裁定（卡上定死）

1. **claude-code.md 加一节「permissions 层的机械边界」（放在 tools 白名单段之后）**，三句写死：
   - **名单 ≠ 生效**：`permissions.allow/deny` 是声明，不是机械保证——前缀通配盖不住带 flag 的复合用法（`chmod 644` 拦、`chmod -v 644` 溜）；配了就默认生效，错了会归罪「配置坏了」，这一格默认是错的。
   - **热重载分两型**：`deny` 与 `hooks` 中途改即时生效；`allow` 不热重载——中途加 allow 当场无效，要重开会话。
   - **机械兜底是 PreToolUse 守卫**：复合命令与 flag 形状归守卫判（本桌 2026-09-23 已装，用户级）；**改任何 permissions 设置之后，重开会话再信**。
2. **守卫产品化另立一行（5.11，本刀只立案不施工）**：守卫脚本进 `.mirror/` 的形状（随附还是文档指引）、装法、与 `init.py` 的关系——判据写进行里，等人点或队列轮到。

## 验收命令（bash 用 `D:\Tools\Git\bin\bash.exe`）

| 格 | 命令 | 应当读到 |
|---|---|---|
| 1 | `grep -c '名单 ≠ 生效' docs_meta/src/claude-code.md` | `1` |
| 2 | `grep -c '热重载分两型' docs_meta/src/claude-code.md` | `1` |
| 3 | `grep -c 'PreToolUse' docs_meta/src/claude-code.md` | `≥1` |
| 4 | `grep -cE '^- \[ \] \*\*5\.11\*\*' docs_meta/docs/todo.md` | `1`（立案行在） |
| 5 | `bash docs_meta/tests/run.sh` | `20 本`；`ALL PASS`；`0` |
| 6 | `git status --porcelain` | ⊆ {claude-code.md, todo.md, SESSION.md, PROMPT_062.md(新), queue.md} |
| 7 | `grep -c 'cmd/PROMPT_062.md' docs_meta/docs/todo.md` | `1` |

## 不交什么

- 不写守卫脚本本体（5.11 的活）；不动 `.mirror/`；不动本机用户级守卫；不改 20 本口径。

## 禁令

- 三句裁定只许搬运不许改写；守卫立案行不得夹带「已随附」的许诺——它还没进 mirror。

## 闸一请示

（无。行内两问本卡裁：补格=是、随附=另立行；判据 grep。）
