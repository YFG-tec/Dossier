# PROMPT_100 · 5.44 postman 工具——七坑对策长成工具，邮差上岗

| | |
|---|---|
| **本刀是 TODO 哪一行** | `todo.md` `5.44`：postman 工具（人 2026-10-10 原话逐字在行内） |
| **状态** | 第 1 稿（批内顺承，红印随批代落） |
| **落槌来源** | 邮箱批点火（#57 印文）；材料 `design/mailbox-research.md`（demo 16/16＋七坑清单）；5.43 纪律已法（六条＋三钉＋地址制） |
| **前置，满足了** | mailbox-research 全篇亲读；`.tmp/mailbox-demo/run-demo.ps1` 亲读（七坑现场）；5.43 落法四件亲读；`init.py`／`setup_probe.py` 现文亲读 |
| **档位** | 重（动 `src/` 工具面＋init）。本刀不改档位的值 |
| **谁来建造** | 独立 subagent（工牌制） |
| **独立审查** | 事实与结构手第一顺位；实战手第二顺位（独立跑 selftest 夹具全周期＋draft/seal 人机工学） |
| **写到哪几处** | ①`docs_meta/src/postman.py`（新工具）②`docs_meta/src/init.py`（`--with-mail` 可选装）③若根 harness／镜像现算有对应行则同步（现算定有无）④记录件 |

## 裁定（卡上定死）

1. **`postman.py`（Python，避免 PS 两坑）**，子命令制：
   - `draft <to> <type> <subject>`：按类型模板在**自己 outbox** 落 `draft-*.md`（头字段 from/to/date/type/subject）；
   - `seal <draft>`：改名 `sealed-*`＝封缄（唯一入投递通道，5.43 法）；
   - `send`：邮差周期——`pull --rebase` → 逐封已封信以唯一文件名（`<序号>-<from>-<to>-<时戳>.md`）`add --sparse` 写收件人 inbox → commit → push（**失败重试 N 次，每次先 rebase**）→ 发件留底入自己 archive；
   - `receive`：`pull` → 清点 inbox → 陌生地址（不在人签地址簿）的信移**陌生件格** → 处理过的移 archive；
   - `selftest`：树外 `mktemp` 造 bare 邮局＋两桌夹具，全周期自证（draft→seal→send→receive→archive＋防撞＋落后基线被拒→rebase 重试成功）——**独立入口，不入 22 本套**。
2. **七坑对策固化**：rebase-后-push 重试；建仓/克隆显式 `-b main`；Python 运行时（编码坑×2 绕开）；`add --sparse` 后可选清理；file:// 与 https 两形远端都支持；cone 根文件＝地址簿全员可见（沿用）；唯一文件名防撞。
3. **凭据**：token 只从**宿主私有件**读（路径来自配置或环境变量，变量名进文档、值永不进仓进聊天）；三钉在工具侧再加一道：push 仅当远端 URL 属邮局仓配置时执行，否则拒绝。
4. **init `--with-mail <url> --desk <地址>`**：submodule 挂 `.mail/`＋sparse 配置＋postman 可用自检；不传旗零影响（5.43 法：可选适配器）。
5. **刀期末＝正式测试（人配合项，不堵结案）**：本刀以 selftest 夹具绿为准结案；人随后开新远程＋给 token，正式测试按同流程实录，结果**追加**记 SESSION/queue——红则另立修刀，不回撕本卡。
6. **不越界**：不动 5.43 已落条文；不动 22 本检查与口径；不替门铃实装（notify 仍是占位）。
7. **记录件**：todo 5.44 挂卡指针；SESSION 覆盖；queue #58 在办。

## 验收命令（bash 用 Git Bash；日志树外）

| 格 | 命令 | 应当读到 |
|---|---|---|
| 1 | `bash docs_meta/tests/run.sh`（树外日志） | 22 本；ALL PASS（结案时） |
| 2 | `python docs_meta/src/postman.py selftest` | 树外夹具全周期绿（含防撞＋重试两剧本），读数逐条在案 |
| 3 | 树外 bare 夹具＋`init.py --with-mail <file://…> --desk demo-a` | `.mail` 挂上、sparse 只见自己＋地址簿、postman 自检过 |
| 4 | `rg -n "postman" docs_meta/src/init.py docs_meta/src/postman.py` | 命中 |
| 5 | `git status --porcelain` | ⊆ 本卡点名处 |
| 6 | （期后项）真远程正式测试 | 人开仓给 token 后实录追加，不堵本刀 |

## 不交什么

- 不动条文、不动 22 本、不实装门铃、不动 5.30 基线件。

## 禁令

- 探针／夹具一律树外（红线）；selftest 失败大声红；凭据永不落仓落聊天；新句循中式公文画风；不动既有判据。

## 闸一请示

（无。工具系排序列令射程；三钉工具侧加固系 5.43 法的执行；期后正式测试系人原话。）
