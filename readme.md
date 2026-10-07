<p align="center">
  <img src="docs_meta/src/figures/dossier-icon.png" width="168" alt="绘卷 Dossier：一叠卷宗里抽出一份，背上贴签，盖了朱爪印才算结">
</p>

<h1 align="center">Dossier</h1>

<p align="center">
  <b>一次一刀，盖章才算数。</b><br>
  装两行命令，你的代理从「聊着写」变成「按卷宗办事」——你只管点行、认账、拍板。
</p>

> 写给会用 AI 编程代理、但没折腾过 harness 的人。五分钟读完知道它替你管什么；只想装，往下翻到安装两步。细则在 `docs_meta/src/`。

---

**Dossier 是一套给 AI 编程代理用的流程约束和 harness 配置。** 以 git submodule 挂进你的仓库，跑一次 `init`，它在你的仓库根上铺出 `docs/` 骨架、`CLAUDE.md` / `AGENTS.md` 和几份角色文件。从那以后代理按它的规矩干活：一次只做一张卡上的事；写卡和改代码是两个会话；验收判据先写下来再跑；说「通过」必须指得出能复现的证据。

*Dossier is a process harness for AI coding agents. Add it as a git submodule, run `init`, and it lays a `docs/` skeleton, `CLAUDE.md` / `AGENTS.md`, and role files into your repo. From then on the agent works one card at a time, planning and implementation live in two separate sessions, acceptance criteria are declared before the run, and "passed" must point at reproducible evidence.*

**给谁用**：你让代理写的代码，测试全绿也不等于对——数值求解器、数据管线、任何交付物是「一个结论」而不是「一个能跑的东西」的项目。
**不给谁用**：失败很响的项目。编译不过、页面白屏、用户当场就能发现——这套密度在那里是税，不是保险。

*For work where green tests do not mean correct: numerical solvers, data pipelines, anything whose deliverable is a claim rather than a running thing. Not for projects whose failures are loud.*

```text
your-repo/
  CLAUDE.md  AGENTS.md        代理每次开工先读的约定
  .claude/   .cursor/  .codex/   角色文件、开关、执行席落点
  docs/
    TODO.md  SESSION.md       待办；本刀的运行态
    queue.md                  序列单：授权一批刀排队自己往下走
    SETUP.md                  装桌检查单（init 铺出，五步）
    cmd/  design/  reports/   每刀的卡；合同层；阶段交付
  dossier/                    子模块。母本本身，你不改它
```

安装两步：

```text
git submodule add https://github.com/YFG-tec/Dossier dossier
python dossier/docs_meta/src/init.py
```

装完跟着 `docs/SETUP.md` 的五步走一遍（拉子模块 → 铺桌 → 起步闸自检 → 首刀先跑一遍检查看红绿 → 配置基线回执）。细则往下读；只想装，看这两行就够。

## 这台机器自己会转

早先，这些规矩全靠你一句一句盯着。现在分三层，各归各。

先答两个进门问题。**它不带服务、不连账号**：就是一叠文件和检查脚本，跑在你自己的会话里。**两席＝两个会话**：默认规划席 Cursor、实现席 Claude Code，Codex CLI 也能坐实现席；用哪家可以换，两个会话合不成一个。

**你每天只做四件事。** 点一行待办、说一声开工、结案时认账、遇到断点拍板。就这四样，别的都有人代笔。

**代理自己会跑一批。** 把一串待办授权进 `docs/queue.md`，代理席就按序列自己往下走：代点行、写卡、派手施工、独立审查、跑验收、结案、提交到本地分支——每刀一报。它的章是**蓝印**，效力与人印相同，只标明是代理落的。七样它永远不碰，撞上就停下、把待裁的事写进队列等你一句话（你回了就续跑）：**松判据**（放宽验收标准）、**发授权**（给自己扩权）、**改序列**（动你排的队）、**动根基条款**（改这套规矩的地基）、**胖行**（把待办行写肥）、**做不到的卡**、**审查返工**。**push 对代理永远禁止**，远端同步是你的动作。

**机器替你把话验真。** 二十一本机械检查一条入口全量跑；开工先过起步闸——执行架构缺了半边（有 agents 没 skills 这类「半身不遂」）当场红，不等活了半天才发现配置早丢了。**宿主**就是你用的那款代理程序（Claude Code、Cursor、Codex 这类）；母本会把角色文件翻成各宿主要的样子铺给你。换宿主不静默失灵：进 `.mirror/` 的配置随子模块一起旅行，宿主私有的件有清单点名，配置偏没偏有指纹可对——「宿主那份偏了没有」是一条命令的问答，`CHANGELOG` 会告诉宿主哪半边要重译。



这套自转不是变出来的。**值日手**就是定时唤醒的值班机制：系统计划任务每十分钟碰一下文件，代理的「耳朵」听见就醒来干活；一个 deadman 探针随时做三面体检——定时任务还在不在、心跳按节律跳没跳、有没有卡死的在办锁——任何一面不对就停下报告，不装没事。宿主没有定时能力也不阻塞开发：记一笔死账，等你点火。装法与拆法都在 `docs_meta/docs/design/loop.md`。

*The machine runs itself in three layers. It ships no service and connects no account - just files and check scripts running in your own sessions; two seats simply means two sessions, whichever vendors. You do four things a day: pick a row, say go, acknowledge closes, rule at breakpoints. The agent seat walks an authorized queue on its own - every close commits to your local branch under a blue stamp with the same force as your own, one report per knife, hard stops at seven breakpoint kinds, never pushes. And the machinery verifies the talk: twenty-one checks behind one entry, a start gate that catches half-installed harnesses before work begins, a mirror that travels with the submodule, and content stamps that turn "has the host copy drifted" into a machine answer. The wake loop is a scheduled task touching one file every ten minutes, watched by a three-face deadman probe; where the host cannot schedule, the desk records a dead account and waits for your ignition - development never stalls.*

## 绘卷

一叠卷宗，一次抽一份出来办。背上贴着签，不翻开就知道是哪一件。
办完盖章，盖了才算数；章不是自己盖给自己的。抽走一份，叠还在。

项目中文名是「绘卷」，英文名是 `Dossier`，名词是案卷。都是「卷」：案卷是背上贴着签的一捆（不翻开就知道是哪一件），绘卷是展开给你看的一幅（画的就是那一叠）。

| 词 | 指什么 |
|---|---|
| **Dossier** | 本仓库。这套规矩本身 |
| **桌** | 课题仓库 |
| **刀** | 桌上的一个工作单元 |

**母本只有一份，桌一张张从它出来。**

这套东西是几个数值项目里边做边收的。各桌有各自的实现和探索路径。Dossier 做的不是汇编，是**提取、统合、抽象、升级**：单桌没想到的缺口要补，不利于管理的冗余要丢掉。三桌里有的，不自动进公共层。旧桌没有义务回改。对照表见 `docs_meta/src/sources.md`。

---

## 公信

分档判据是「判据外生还是内生」，不是「项目大小」。判据外生的（有参考实现、金标准）该长跑、稀疏监督；判据内生的（自己造）该短刀、密集闸门。这套东西在前一格是税，在后一格是本体。

第二条分野是失败响不响。编译不过、对不上参考输出是响的；数值上的静默降档（枚举声明三档、内核当默认档、契约测试全绿）是不响的。**密集闸门买的不是速度，是让静默失败在一刀之内暴露。** 这条辩护不能是「模型还不够好」，只能是「判据内生 + 失败静默」这两条；哪天这两条不成立了，就该往长跑退，而不是加规矩。

这份管理密度，人类项目负担不起。它在这里成立，是因为**执行规矩的边际成本降到了近乎为零**：写卡、落盘、逐条对账，对智能体是顺手；文档是它唯一稳定的记忆。规矩定得细不是因为聪明，是因为现在定得起。

判据先声明、证据能复现、盖章的手不是干活的手。核心不是转化，是取信——不是把原料变成产品，是让一个结论**可以被相信**。连「可以结案了」都收成了一条可机读的查询：谓词红，谁说情都不算。

偏离要逐条写明代价，藏起来的偏离自己就是一类失败。欠的账摊在 `docs_meta/docs/todo.md` 第 5 章、第 6 章。怎么立的，见下一节。

---

## 建制

这套东西的骨架是五条：**两席、两闸、卡、权威分层、状态在磁盘。**

三样挂进这五条：派专职的手、举证独立复跑，挂在「两席」底下；记录只追加，挂在「状态在磁盘」底下；源码 → 产物单向，挂在「权威分层」底下——只准源码 → 产物，要改就去改源码那一头；两边不一致不是判据，方向才是。

**两席**不是两个 AI 一起写代码。分工是能力差异加上权限差异。选哪个 harness 坐哪一席可以换，**两席必须是两个会话**不能换。角色不是人设，是**写权限 + 失败时许做什么**。

- 写卡的手不接着改核
- 改核的手不改测试口径
- 写测试的手不把核修到绿
- 审查的手不写文件；只核对结果和预先声明的标准
- 规划席说「继续推进」打不开 `src/`

**两闸**是立案一道、结案一道。人只站两道闸。

**卡**是这一刀唯一的许可面。一刀一张卡，没有卡片不准动核。

**权威分层**：源码是规范正文，产物是编出来的 harness。

**状态在磁盘**：状态记录在版本控制里落盘，能复现，不在聊天里漂移。

防的是七类失败：

1. **超售。** 用户要一行验证，它顺手开下一阶段。
2. **状态在聊天里。** 换窗口，范围漂移。
3. **规划席和实现席抢同一份核。**
4. **探针对不上复现。** 报告引用 `.tmp/run_*.py`，交付第二天废。
5. **测试不能失败。** 期望值和计算值同源。
6. **散了先改数值旋钮。** 病状没了，合同被换掉。
7. **图没人看。** 真错误只在打开图时才露。

**先用目录把权威分开，再用一刀把范围锁死。范围、合同、证据、许可都落到磁盘上。**

<p align="center">
  <img src="docs_meta/src/figures/dossier-frame.png" width="880" alt="「Dossier 的一天」：左栏红框「你」列四件事（点行、开工、认账、拍板）；中栏蓝框「代理席」六步闭环（取队列、写卡、派手施工、独立审查、跑验收、蓝印记档），角注「蓝印＝你的章」「永不 push」，红字「撞断点：停下等你」；底部横带「机器验真」（二十一本检查、起步闸、配置指纹）；红虚线＝每刀一报折回「你」认账。">
</p>

装这套东西是两个动作：把母本挂成子模块，再跑一次 `init`。

```text
1. git submodule add https://github.com/YFG-tec/Dossier dossier
2. python dossier/docs_meta/src/init.py
```

子模块目录叫什么随你，`init` 按自己的位置现算路径。它默认铺到子模块外面一层，也就是你这个仓库的根上。铺出来的是一副空壳，不是样例——目录和落点都在，内容要你自己写。根上那几份 harness 是从母本 `.mirror/` 拷出来的。

重跑只补缺的那几件，已经有的一律不覆盖，所以升级也是这条路：`git submodule update --remote` 拉新版，再跑一次 `init`。边界是物理的——子模块目录里面归母本，外面全归你这张桌。

想先看一圈怎么转：`example_meta/` 里有一份跑得通全流程的冒烟样例（玩具核＋假人）。

细则按需要打开，不必先读完：

| 要干什么 | 读 |
|---|---|
| 目录长什么样、图放哪 | `docs_meta/src/directory.md` |
| 一刀、卡片、收口 | `docs_meta/src/workflow.md` |
| 验证、排障、这套验不了什么 | `docs_meta/src/verify.md` |
| 角色、档位、模型下限 | `docs_meta/src/roles.md` |
| Claude Code / Codex CLI 怎么落 | `docs_meta/src/claude-code.md` |
| Cursor 怎么落 | `docs_meta/src/cursor.md` |
| 队列与自动化怎么转 | `docs_meta/docs/design/loop.md` |
| 模型分档与派单路由 | `docs_meta/docs/design/model-routing.md` |
| 外面有什么、为什么不那样做 | `docs_meta/src/sources.md` |
| 还没对齐的问题 | `docs_meta/docs/design/open.md` |
| 运行时 | Python ≥ 3.13（解释器优先 `.venv`，未建则系统，首次需要时建）、Windows 用 Git Bash 跑检查——环境自检 `bash docs_meta/tests/check-env.sh` |

---

## 那枚爪印

写代码的速度，人早就追不上大模型了；但最后落下的那一爪，才是灵魂。
