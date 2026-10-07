# PROMPT_090 · 5.32 Python 环境自足——惰性 venv＋领班管库

| | |
|---|---|
| **本刀是 TODO 哪一行** | `todo.md` `5.32`：Python 环境自足（人 2026-10-07 原话＋三裁逐字在行内） |
| **状态** | 第 1 稿 |
| **落槌来源** | 人 2026-10-07 点名＋「你开工吧，这点儿活儿按自动流程做了就行」（点火原话）；三裁：①惰性建 ②requirements 领班维护＋执行席上提 ③pip 归领班 |
| **前置，满足了** | 契约句镜像位亲枚举（init/close_cut 头注、A 段文案、冻结卡与历史报告不动）；verify :51 现句亲读；议事纪要在案（本会话 2026-10-07） |
| **档位** | 重（动检查本＋条文＋工具头注）。本刀不改档位的值 |
| **谁来建造** | subagent builder（工牌 b1） |
| **独立审查** | 派两只并行手（表面／语义）；A 段功能领班亲跑 |
| **写到哪几处** | ①`docs_meta/tests/check-env.sh`（A 段 venv 感知）；②`docs_meta/src/tools/close_cut.py` :3 与 `docs_meta/src/init.py` :3（契约句）；③`docs_meta/src/roles.md`（代理席节一段）；④`docs_meta/src/verify.md` :51（对齐句）；⑤`readme.md` 运行时行（补括注）；⑥记录件（含 queue #48 台账行） |

## 裁定（卡上定死）

1. **check-env A 段 venv 感知**（替换现有 A 段块，保持 pass/warn/fail 三值风格；其余段零改动）：
   - 探测顺序：`$ROOT/.venv/Scripts/python.exe` → `$ROOT/.venv/bin/python` → 都不在用 `python`；
   - venv 在：版本读数用 venv 的 python，三档文案前缀 `[venv]`（如 `pass "A Python[venv]：$py_line（>= 3.13）"`）；
   - venv 不在：照旧用系统 python，三档文案前缀 `[系统·venv 未建——首次需要时建 5.32]`，**不算红**（未建是正常态，WARN 仅沿版本旧规）；
   - 注释一行注明正身＝PROMPT_090 裁定 1、人裁①。
2. **契约句三处同文**（close_cut.py :3、init.py :3 原句内插，插后逐字）：
   `运行时契约：Python >= 3.13（3.12 兼容模式可用；解释器优先项目内 \`.venv\`，未建则系统，首次需要时建——5.32）＋ Git Bash（Windows）。详见 docs_meta/tests/check-env.sh。`
   （PROMPT_058 冻结卡与历史报告里的旧句不改——历史不追改。）
3. **roles.md 代理席节加一段**（值日手两段之后、「### 副官」之前，行文逐字）：
   `**库安装与 \`requirements.txt\` 维护归领班（5.32，2026-10-07 人三裁）。** \`.venv\` 首次需要时由领班创建（人裁①）；执行手缺库经信箱上提（5.29 形），领班验后装库并维护桌根 \`requirements.txt\`（人裁②）；pip 由领班自动执行，**只装 \`requirements.txt\` 点名的库，装前把命令与版本记进台账**（人裁③＋网络写边界）。`
4. **verify.md :51 对齐**（原句改写，逐字）：
   `- 解释器优先项目内 \`.venv\`（未建则系统，首次需要时建——5.32），命令写进卡片和报告。`
5. **readme 运行时行补括注**（仅此一行）：`Python ≥ 3.13` 后插 `（解释器优先 \`.venv\`，未建则系统，首次需要时建）`。
6. **记录件**：`todo.md` `5.32` 行挂本卡指针；`SESSION.md` 覆盖；`queue.md` 新增 #48 行（5.32，在办——批外直令刀，点火原话在案）。

## 验收命令（bash 用 Git Bash）

| 格 | 命令 | 应当读到 |
|---|---|---|
| 1 | `bash docs_meta/tests/run.sh` | `21 本`；无 FAIL |
| 2 | `bash docs_meta/tests/check-env.sh` | ALL PASS；A 行含 `[venv]`（本桌 venv 在——领班亲跑） |
| 3 | `rg -n '首次需要时建' docs_meta/tests/check-env.sh docs_meta/src/tools/close_cut.py docs_meta/src/init.py docs_meta/src/roles.md docs_meta/src/verify.md readme.md` | 六件各 ≥1 |
| 4 | `rg -n '只装 \`requirements.txt\` 点名的库' docs_meta/src/roles.md` | 恰 1 |
| 5 | `bash docs_meta/tests/check-done.sh` | ALL PASS；PROMPT_090 恰 1 |
| 6 | `git status --porcelain` | ⊆ {check-env.sh, close_cut.py, init.py, roles.md, verify.md, readme.md, todo.md, SESSION.md, queue.md, PROMPT_090.md(新)} |

## 不交什么

- 不动 E 段与 A–D 段其余逻辑；不建 venv、不建 requirements.txt（本仓母本纯标准库，无需——建点在桌侧首次需要时）；不动 `.mirror/`；不动 PROMPT_058 冻结卡与历史报告；不动 17 标记节（roles 代理席节、verify 环境节均未标记）；不加新工具（pip 由领班现跑，台账留痕）。

## 禁令

- 「未建不算红」不得写成 WARN（正常态不当故障报）；契约句三处必须逐字同文；「只装 requirements 点名的库」不得软化。

## 闸一请示

（无。三裁皆人原话；pip 边界是收权不是放权。）
