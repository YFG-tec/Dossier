# 本刀运行态

**本页不是卡片，是指向卡片的链接 + 本刀跑起来之后才产生的东西。**
细则一个字都不在这里，全在链接指的那份里——**本页每刀重写；那份闸一之后不许改，结案后只增不删。**
规矩见 `../src/workflow.md`「状态在磁盘，不在聊天」。

**本页两截**：横线以上由实现席（Claude Code）起草，随施工改；
横线以下只追加审阅，不改上面，不改卡。**形同审稿**：上面是稿的运行态，下面是审稿意见。

| | |
|---|---|
| **许可面** | [本刀卡片](cmd/PROMPT_100.md) ← 要看细则，点这里 |
| **点的行** | `todo.md` `5.44`：postman 工具（人 2026-10-10 原话逐字在行内） |
| **状态** | 已结案（2026-10-10；事实手复验终判 GREEN、实战手 GREEN；返工 1＝顶层 import 破零影响，修讫） |
| **落槌来源** | 邮箱批点火（#57 印文）；材料 mailbox-research（demo 16/16＋七坑）；5.43 纪律已法 |
| **前置，满足了** | mailbox-research 全篇；demo 脚本亲读；5.43 四件亲读；init/setup_probe 现文亲读 |
| **档位** | 重（动 `src/` 工具面＋init）。本刀不改档位的值 |
| **卡的稿次** | 第 1 稿 |
| **版次** | 第 1 版（印文见「闸一」节） |
| **谁来建造** | 独立 subagent（工牌制） |
| **独立审查** | 事实与结构手第一顺位；实战手第二顺位（独立跑 selftest 全周期） |
| **举证谁跑** | 建造手自跑＋领班终跑（日志树外） |

## 闸一

闸一红印 · 2026-10-10 · 第 1 版 批内顺承（邮箱批 #58）——批点火原话在 #57 印文（人 2026-10-10「开工」「启动代理」）；序列已授权，每刀一报、开发不停。代理席代落（--代理席落印）。刀级锁已取：`.tmp/locks/5.44.lock`。

## 现在停在哪一步

| 步 | 读数 |
|---|---|
| 1 基线 | `HEAD` `ab1ef0d`（5.43 已结）；两笔在册外部账＋调研卷待随刀入册 |
| 2 写卡 | PROMPT_100 第 1 稿落盘（百卡里程碑） |
| 3 施工 | Hubble 成件（postman.py 702 行＋init --with-mail）；返工 r2＝Jason 懒加载修讫（不带旗零导入零 pyc、带旗功能不回归，importtime 硬读数在案） |
| 4 审查 | 事实手 MUST-FIX 1→复验终判 GREEN；实战手 r2 GREEN（selftest 双跑、树外 init 全绿、恶意正文无执行路径、指纹三明治不变） |

## 收口读数

- 审查：事实手 MUST-FIX 1（init.py 顶层 import postman 破「不传旗零影响」＋再生 pyc）→ Jason 返工（懒加载进分支＋清残）→ Popper 复验终判 GREEN（importtime 0/1 双形硬读数；pyc 绝迹）；实战手 r2 GREEN 四问（含 rm -rf 恶意正文逐字留档无执行、源码无 shell=True/eval/exec/os.system）。
- 通道事故账：四手连续不应后自愈（修复手＋实战手 r2 恢复交卷）——挂起裁定未执行即失效，记录在案。
- 已知欠账（如实记档，不堵结案）：本机自定义 Git 的 submodule status 因 git-sh-setup 路径断——C 层 clone＋手工 gitlink/.gitmodules 登记兜底已实现并验证；submodule 形在真托管上的终验归期后正式测试。
- 期后项（人配合）：人开新远程＋专用 token（宿主私件，勿贴聊天）→ 正式测试按同流程实录追加；红则另立修刀。
- 举证途中一笔：卡头一字误「品→哪」（check-verdict G0 抓不到行 id）——5.19 一字卡误先例原样重演，当场修，复跑全绿；22 本终跑（领班，日志树外）；行 5.44 搬已办；queue #58 已结——邮箱批收官；commit 落分支不 push。

## 写卡阶段在盘上查了什么

- mailbox-research 全篇；demo 脚本与七坑；5.43 落法四件；init/setup_probe 现文；PROMPT_093–099 体例。

## 这只手没做的（写卡阶段）

- 没动 `src/`、根 harness（回避）；没勾行、没 commit、没 push。

---

## 横线以下 · 审阅（只追加）

- 2026-10-10 审查读数：**事实手** MUST-FIX 1→修讫→复验终判 GREEN——阻断项系 init.py 顶层 import postman（不传旗非零影响＋pyc 残留），返工后懒加载进 --with-mail 分支，importtime 双形硬读数（不带旗 0 命中/带旗 1 命中）、pycache 绝迹、gitlink/sparse/mail.json 全对；首跑 dubious ownership 红系审查沙箱 safe.directory 环境非功能回归，注记在案。**实战手 r2** GREEN——selftest 初终双跑 ALL PASS（防撞＋落后基线 rebase 重试）；树外 bare 邮局＋--with-mail 实装全绿（gitlink 160000 正常、sparse 只见 demo-x＋地址簿、自检 PASS）；人机工学三问过（五头字段、draft→sealed 规则、[RETRY] 读数教下一步）；恶意正文逐字留档无执行路径。验不了：真 https/token/跨环境安全——期后正式测试归人。
