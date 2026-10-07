# PROMPT_092 · 5.36 门面焕然一新＋架构图重画——解冻 3.2，图为用户重绘

| | |
|---|---|
| **本刀是 TODO 哪一行** | `todo.md` `5.36`：门面焕然一新（人解冻原话逐字在行内）；`5.35` 中英两稿对齐随刀吸收 |
| **状态** | 第 1 稿 |
| **落槌来源** | 人 2026-10-07「3.2的冻结面的确改了…可以写焕然一新的一版，尤其是架构图，需要重新用matplotlib画一个对用户更友好的版本」；5.31/5.34 教训与 v0.1.0 启示全部在案 |
| **前置，满足了** | PROMPT_033 冻结清单亲读（页首四件：图标三行/h1/口号块/head note）；make_frame.py 现状亲读（matplotlib 3.11.2 在 venv，无需装库）；release.md 门面规范（:22 两稿对得上/:66 段式）亲读 |
| **档位** | 重（门面＋图，双产品件）。本刀不改档位的值 |
| **谁来建造** | 领班亲笔（刀内取舍：图像设计＋散文需判断力，记档；图由领班渲染并亲目验收） |
| **独立审查** | 读者扮演手第一顺位（含图的可读性判读）；事实与结构手第二顺位 |
| **写到哪几处** | ①`readme.md`（第一屏焕新＋图与图注更换＋EN 镜像补全〔吸收 5.35〕）；②`docs_meta/src/figures/make_frame.py`（重写，用户版架构图）；③`docs_meta/src/figures/dossier-frame.png`（重渲染）；④记录件（含 queue #50） |

## 裁定（卡上定死）

1. **第一屏焕新**（图标与 `<h1>Dossier</h1>` 保留——品牌识别；口号与 head note 重写，逐字）：
   - 口号块：
     `<b>一次一刀，盖章才算数。</b><br>\n  装两行命令，你的代理从「聊着写」变成「按卷宗办事」——你只管点行、认账、拍板。`
   - head note：
     `> 写给会用 AI 编程代理、但没折腾过 harness 的人。五分钟读完知道它替你管什么；只想装，往下翻到安装两步。细则在 \`docs_meta/src/\`。`
2. **架构图重画（用户版）**：重写 `make_frame.py`，画**「Dossier 的一天」横向三栏流程图**（替换现权限矩阵图；矩阵图归档于 git 历史）：
   - 左栏「**你**」（朱红描边）：四件事竖排——点一行待办／说开工／结案认账／断点拍板；
   - 中栏「**代理席**」（蓝印蓝 #2F6FED 描边）：闭环流程——取队列 → 写卡 → 派手施工 → 独立审查 → 跑验收 → 蓝印记档 → 刀报；角注两枚：「蓝印＝你的章，只标是谁落的」「永不 push——远端归你」；
   - 右下横带「**机器验真**」（墨色细框）：二十一本检查一条入口 · 起步闸 · 配置指纹；
   - 箭头：你→（点行）→代理闭环→（每刀一报）→你；闭环内「撞断点」出口→「停下等你」；
   - 风格：白底、YaHei、大框少字、朱红只给你那一栏（naming.md 色律）；输出仍 1760×1024 @2x，文件名不变 `dossier-frame.png`；
   - 图注（alt）重写为一段白话描述（≤120 字），与图实况一致。
3. **EN 镜像补全（吸收 5.35）**：自转章 EN 段补两句——进门两问（no service, no account; two seats means two sessions）与尾段义（wake by scheduled task, deadman probe, dead account + human ignition when the host cannot schedule）；改后中英两稿逐段对得上。
4. **不变的**：5.34 问题序节构（六章节序不动）；树图/安装两步/读表/爪印句；`run.sh` 相关的 readme 义务（运行时行仍提 `check-env`）；CHANGELOG 不动。
5. **5.35 吸收结案**：todo 5.35 行按吸收式落已办（原措辞＋吸收注记点名 5.36＋日期，不点卡）。
6. **记录件**：`todo.md` 5.36 挂卡指针；`SESSION.md` 覆盖；`queue.md` 新增 #50 行（在办，批外直令刀）。

## 验收命令（bash 用 Git Bash）

| 格 | 命令 | 应当读到 |
|---|---|---|
| 1 | `bash docs_meta/tests/run.sh` | `21 本`；无 FAIL |
| 2 | `& .venv/Scripts/python.exe docs_meta/src/figures/make_frame.py` 后 `dossier-frame.png` mtime 晚于卡落盘；领班亲目读图（read 工具） | 图＝裁定 2 三栏流程，文字无溢出无乱码 |
| 3 | `rg -n '^## ' readme.md` | 节序与 5.34 相同（自转章仍在绘卷前） |
| 4 | `rg -c 'v0\.2 起\|Since v0\|转译\|课题锁' readme.md` | 各 0 |
| 5 | `bash docs_meta/tests/check-done.sh` | ALL PASS；PROMPT_092 恰 1；5.35 吸收注记在案 |
| 6 | `git status --porcelain` | ⊆ {readme.md, make_frame.py, dossier-frame.png, todo.md, SESSION.md, queue.md, PROMPT_092.md(新)} |

## 不交什么

- 不动六章节序与树图；不动 CHANGELOG 与 `docs_meta/src/` 条文；不删旧图脚本历史（git 留档）；不动 `.mirror/`；不建 requirements.txt（matplotlib 已在，无需走 5.32 流程）。

## 禁令

- 朱红只给你的元素；图内不出现未在正文定义的术语；EN 与中文逐段对得上；第一屏新句不含快事实（价格/战绩/版本锚）。

## 闸一请示

（无。解冻系人原话；图与文案皆为门面件，不松任何判据。）
