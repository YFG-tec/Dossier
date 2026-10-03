# PROMPT_058 · 运行时契约——环境自检本与三处声明

| | |
|---|---|
| **本刀是 TODO 哪一行** | `todo.md` `5.9`（本刀新立，代理席日常裁定；外部报告 P0 第一条） |
| **状态** | 第 1 稿 |
| **落槌来源** | 人 2026-10-02「ok，先把这三部分做完」；外部报告 §3.1/§3.2（close_cut 3.12 炸＋bash alias 不可复现） |
| **前置，满足了** | 报告两红点在案；本席今夜 3.12 兼容补丁已打（6.21 刀内），本刀把它升成契约 |
| **档位** | 重（动 src + 新检查本，本数 18→19）。本刀不改档位的值 |
| **谁来建造** | `codex exec`（执行席·常态第二刀）写环境自检本＋三处声明；**领班**写卡、跑格、审查、收口 |
| **独立审查** | 派——动 src 与检查本 |
| **写到哪几处** | ①新 `docs_meta/tests/check-env.sh`（第 19 本）；②`docs_meta/src/tools/close_cut.py` 头部版本声明；③`docs_meta/src/init.py` 头部版本声明；④`readme.md` 细则表后加一行运行时要求；⑤记录件 |

## 现状（builder 会踩的）

1. **契约内容三条**：Python ≥ 3.13（close_cut 用 `read_bytes` 兼容 3.12，但契约声明 3.13 为基准——工具已双兼容，声明取高线）；Windows 下 bash 必须 Git Bash 形（`D:\Tools\Git\bin\bash.exe` 这类，WSL shim 跑不动 CRLF——巡查 #1 实证）；UTF-8 输出（`--output` 落文件防乱码的既有惯例写明）。
2. `check-env.sh` 干四件：①`python -c "import sys; sys.exit(0 if sys.version_info>=(3,13) else 1)"`（3.12 时 WARN 不 FAIL——close_cut 已兼容，降为提示）；②bash 自检：`uname -o` 含 `MSYS`/`Cygwin` 为 Git Bash，`microsoft`/`linux` 为 WSL → **WSL 直接 FAIL**（实证跑不动）；③`git rev-parse --is-inside-work-tree`；④三处声明在盘 grep（close_cut/init 头部、readme 行）。fail 只认②③，①④为 WARN/PASS——**不把「换机器」变成恒红**（fresh clone 有 git 无 WSL 就绿）。
3. 19 本会被 `check-skel` 的跳过数影响吗——不会：skel 量 init 铺装件数，不量 tests 本数；`run.sh` glob 自动发现第 19 本。
4. Codex 指令与 6.23 同形：只碰点名文件＋输出行数，不 commit。

## 交什么

1. `check-env.sh`：四段如上，退出码 0/1，末行 ALL PASS/FAILED；
2. `close_cut.py` docstring 首行后插一行：`运行时契约：Python >= 3.13（3.12 兼容模式可用）＋ Git Bash（Windows）。详见 docs_meta/tests/check-env.sh。`；
3. `init.py` 同款一行；
4. `readme.md` 细则表（「要干什么 | 读」那张）下方加一行：`运行时 | Python ≥ 3.13、Windows 用 Git Bash 跑检查——环境自检 `bash docs_meta/tests/check-env.sh`` 。

## 验收命令（bash 用 `D:\Tools\Git\bin\bash.exe`）

| 格 | 命令 | 应当读到 |
|---|---|---|
| 1 | `bash docs_meta/tests/check-env.sh` | `ALL PASS`；退出 `0`（本机 Git Bash + 3.13） |
| 2 | `grep -c '运行时契约' docs_meta/src/tools/close_cut.py docs_meta/src/init.py` | 各 `1` |
| 3 | `grep -c 'check-env' readme.md` | `1` |
| 4 | `bash docs_meta/tests/run.sh` | `跑了 19 本`；`ALL PASS`；`0` |
| 5 | `git status --porcelain` | ⊆ {check-env.sh(新), close_cut.py, init.py, readme.md, todo.md, SESSION.md, PROMPT_058.md(新)} |
| 6 | `grep -c 'cmd/PROMPT_058.md' docs_meta/docs/todo.md` | `1` |

## 不交什么

- 不改 18 本既有检查口径；不动 close_cut 逻辑（只加声明行）；不做 PowerShell 入口（报告建议的 PS 路留待裁）。

## 禁令

- check-env 不得成为「换机器恒红」——只有 WSL bash 与非 git 环境才 FAIL。

## 闸一请示

（无。人已点名「先把这三部分做完」；报告 P0 在案。）
