# PROMPT_088 · 5.29 值日手与双向巡查——定时件有谓词，巡查会回头

| | |
|---|---|
| **本刀是 TODO 哪一行** | `todo.md` `5.29`：值日手与双向巡查：schtasks＋codex 常设工牌（每周期一刀、心跳 deadman、断点全嵌入）建造；巡查升双向——代理席轮询枚举回复（OK/BLOCKED/NEED_REPLAN）＋执行手信箱式求助＋盘上交叉验证＋重拆路由（人 2026-10-06「我觉得巡查分两部分…这种双向制有 code产品采用么？」） |
| **状态** | 第 1 稿 |
| **落槌来源** | 队列 #46（硬化批授权，批末刀）；人 2026-10-06 问名在行内；#45 审查遗留两句随刀（借载许可面归属、定时件谓词） |
| **前置，满足了** | `design/loop.md` 定时手节与追记亲读（三只角色、六机械件、留言非拉起）；载体现役亲测（schtasks Enabled/Ready、monitor ca31880e、wake 节律）；codex 挂死病理在案（queue 值日首演读数） |
| **档位** | 重——动条文一件＋新工具一件。本刀不改档位的值 |
| **谁来建造** | subagent builder（工牌 b1） |
| **独立审查** | 派两只并行手（表面／语义）；探针功能由领班亲跑 |
| **写到哪几处** | ①`docs_meta/src/roles.md`（代理席节两段）；②`docs_meta/src/tools/duty_probe.py`（新，心跳 deadman 探针）；③记录件 |

## 裁定（卡上定死）

1. **roles.md 代理席节加两段**（5.28 段之后、「### 副官」之前，行文逐字）：

   段一（值日手）：
   `**值日手＝常设工牌，不是新席（5.29，2026-10-07）。** 唤醒周期即值日周期：每周期至多一刀，工牌由领班从队列现排现写，实例落 \`.tmp/duty/\`（零权威层，收口即焚）；建造块照派单路由可派 codex，**借载运行仍受被借会话所在席的许可面辖**。**断点全嵌入**：工牌写死七断点（松判据、发授权、改序列、动根基、胖行、卡做不到、审查返工），值日手不自行判断断点——命中即停、盘上留痕、等领班呈人。**定时件谓词（5.21 族）＝ \`duty_probe.py\`**：载体/心跳/锁三面探针，红即断点呈人，代理不自行修载体。`

   段二（双向巡查）：
   `**巡查是双向的（5.29）。** 领班每周期轮询执行手回信（信箱约定 \`.tmp/duty/inbox/\`，零权威、只作证）：回复三态枚举——**OK**（读数照卡面）、**BLOCKED**（附卡面格号与原样红文，不自行改判）、**NEED_REPLAN**（块拆错了，退回领班重拆，执行手不自行扩面）。执行手也可主动投信求助。信箱话不作判据：领班收信必做**盘上交叉验证**（信中读数 vs git/todo/queue/检查本现算），对不上的信按外部账记名呈报。`

2. **新工具 `docs_meta/src/tools/duty_probe.py`**（心跳 deadman 探针，谓词命令形态）。头注含：定位句（todo 5.29，PROMPT_088；谓词载体——红即断点呈人）、用法行、**查不到什么照写**（monitor 耳现活查不到——耳死只能由消费缺口在 SESSION/git 活动侧暴露，不归本探针）。逻辑三面：
   - **载体**：`schtasks /query /tn DossierQueueWake /fo LIST` → `Status:`（Ready/Running）、`Last Result:`（0）、`Scheduled Task State:`（Enabled）三项全过才绿；
   - **心跳**：`.tmp/queue-runner/wake.md` 末条 `wake <ISO>` 时戳距今 ≤15 分钟（任务周期 10 分钟，容睡醒赶点余量）；
   - **锁**：`.tmp/locks/*.lock` 的 `taken=` 距今 >240 分钟即滞留红（阈同 cut_lock stale）。
   输出：三行读数＋一行总判（`DEADMAN 总判：健康（载体/心跳/锁三面绿）` 或点名红面）；任一面红退出码 1。纯标准库；不修不写任何盘件，只读＋打印。
3. **不建独立第二调度器**（刀内取舍，记档）：codex 挂死病理在案（退出挂死需杀残留）；现有唤醒回路已供周期，再建一个 schtasks→codex 直驱任务只加故障面不加能力。codex 上值日走既有派单路由（工牌实例），不走独立调度。
4. **记录件**：`todo.md` `5.29` 行挂本卡指针；`SESSION.md` 覆盖；`queue.md` #46 状态列。

## 验收命令（bash 用 Git Bash；python 直接跑）

| 格 | 命令 | 应当读到 |
|---|---|---|
| 1 | `bash docs_meta/tests/run.sh` | `21 本`；无 FAIL |
| 2 | `rg -n '值日手＝常设工牌' docs_meta/src/roles.md` | 恰 1 |
| 3 | `rg -n 'NEED_REPLAN' docs_meta/src/roles.md` | 恰 1 |
| 4 | `python -X utf8 docs_meta/src/tools/duty_probe.py` | 退出码 0；末行 `DEADMAN 总判：健康`（领班亲跑） |
| 5 | `bash docs_meta/tests/check-done.sh` | ALL PASS；PROMPT_088 恰 1 |
| 6 | `git status --porcelain` | ⊆ {roles.md, duty_probe.py(新), todo.md, SESSION.md, queue.md, PROMPT_088.md(新)} |

## 不交什么

- 不动 17 标记节（代理席节未标记）；不动 .claude/agents 四件与 E 段期值（值日手不是新 agent 文件）；不动 schtasks 现役任务与 monitor（载体不重装）；不建信箱目录于盘（协议是约定，实例由领班按周期现造）；不动 check-env/check-skel 期值（duty_probe 是母本工具，不入骨架）。

## 禁令

- 两段行文逐字照裁定 1；「不自行判断断点」「信箱话不作判据」两处硬措辞不得软化；探针只读不写，退出码语义不得反接。

## 闸一请示

（无。行判据在行内；谓词是收权不是放权（红即停呈）；双向巡查是流程件，不添授权。）
