# 发布：首页帽子与门口五件

**权威：参考。草案。** 全文不带标记，**一条都不可引**。
2026-09-27 规划席按人当日的话整理，给 `todo.md` `6.24` 与 `7.1` 两行当材料。
判据写在那两行里，本页只把「怎么做到」摊开——摊到**能力不太够的模型也能照着放置**的粗细。

人的原话（2026-09-27，逐字）：
「readme从读者的角度，把原先准备好的补丁todo再细化，在大模型能力即使不太够的情况下，也能做到80分的水平」；
「再开一个todo，目标是出一个release版本，我准备发布到github上」；
「虽然这套东西还比较粗糙，但是如果我想发布到github，如果可能的话收集一些反馈，促进我这个东西的迭代，但是说实话，readme我不满意，一眼看上去不知道是干嘛的」。

---

## 0 「80 分」是什么意思

不是文笔分，是**放置分**。定义写死，免得改核的手临场发挥：

| 分数段 | 长什么样 |
|---|---|
| 60 | 帽子四件都在，位置对，锁句没动，`grep` 全过——但句子是改核的手自己想的，可能又长出术语 |
| **80** | 四件都在、位置对、锁句没动、`grep` 全过，**且每句都从本页 §1 的预写稿放置**，只许微调词序与标点，不许换意思、不许加新词 |
| 90+ | 80 的基础上，中英两稿彼此对得上，读者在 GitHub 第一屏之内（不滚动）看见①②③ |

80 分的做法只有一条路：**文本预写在这里，改核的手做的是搬运，不是构思。**
判据全是 `grep` 和行号，不是「读起来清楚不清楚」——那是人在结案时才判的事。

---

## 1 首页帽子（`6.24` 的材料）

### 1.1 读者是谁、他按什么顺序读

从 GitHub 搜索点进来、没读过任何上下文的人。他的阅读顺序是固定的，改不了：

1. 图标、标题、一行口号（现有第一屏，**保留**）
2. **接下来那一段** ← 帽子落在这里
3. 往下滚才看到「绘卷」

他在第 2 步要在**十秒内**回答三个问题：这是什么、跟我有没有关系、装上会怎样。
答不出就关页。现有首页在第 2 步给他的是一段带日期的范围说明和一张术语表——三个问题一个都没答。

### 1.2 位置：插在哪、不动哪

```text
readme.md
  :1–:10   <p> 图标 / <h1> / <p> 口号             ← 不动
  :12–:13  > 起稿日期 / 范围 / 本页只留…            ← 见 1.4「Quick Start 字面」
  :15      ---                                     ← 不动
           ┌──────────────────────────────────┐
           │ 帽子插在这里：横线之下、「## 绘卷」之上 │
           └──────────────────────────────────┘
  :17      ## 绘卷                                 ← 从这里起一字不动
```

**不动的清单**（`3.5` 通读按内容锁过四处，`6.24` 行里写明不借来改）：

- 口号：「一次一刀，盖章才算数。」及其下一行
- 「核心不是转化，是取信……」那一句（公信节）
- 「那枚爪印」整节
- 「先用目录把权威分开，再用一刀把范围锁死……」那一句及其下的框架图与 alt

绘卷 / 公信 / 建制三节**整节不动**。安装两步那一段（现 `:89`–`:97`）**原位保留**，帽子里另放一份两行版；地址由 `7.1` 换，本刀不碰。

### 1.3 预写稿（放置用；只许微调词序标点）

**第一件 · 是什么**（中文一段 + 英文一段，英文放中文之后，用引用块或斜体都可以）

> **Dossier 是一套给 AI 编程代理用的流程约束和 harness 配置。** 以 git submodule 挂进你的仓库，跑一次 `init`，它在你的仓库根上铺出 `docs/` 骨架、`CLAUDE.md` / `AGENTS.md` 和几份角色文件。从那以后代理按它的规矩干活：一次只做一张卡上的事；写卡和改代码是两个会话；验收判据先写下来再跑；说「通过」必须指得出能复现的证据。

> *Dossier is a process harness for AI coding agents. Add it as a git submodule, run `init`, and it lays a `docs/` skeleton, `CLAUDE.md` / `AGENTS.md`, and role files into your repo. From then on the agent works one card at a time, planning and implementation live in two separate sessions, acceptance criteria are declared before the run, and "passed" must point at reproducible evidence.*

**第二件 · 给谁用、不给谁用**

> **给谁用**：你让代理写的代码，测试全绿也不等于对——数值求解器、数据管线、任何交付物是「一个结论」而不是「一个能跑的东西」的项目。
> **不给谁用**：失败很响的项目。编译不过、页面白屏、用户当场就能发现——这套密度在那里是税，不是保险。

> *For work where green tests do not mean correct: numerical solvers, data pipelines, anything whose deliverable is a claim rather than a running thing. Not for projects whose failures are loud.*

**第三件 · 装上得到什么**（代码块，`text`）

```text
your-repo/
  CLAUDE.md  AGENTS.md        代理每次开工先读的约定
  .claude/   .cursor/         角色文件、开关
  docs/
    TODO.md  SESSION.md       待办；本刀的运行态
    cmd/  design/  reports/   每刀的卡；合同层；阶段交付
  dossier/                    子模块。母本本身，你不改它
```

这棵树照 `docs_meta/src/init.py` 的 `structure` 与 `.mirror/` 现算，改核前再对一次；对不上以脚本为准。

**第四件 · 安装两行**

```text
git submodule add <母本仓库地址> dossier
python dossier/docs_meta/src/init.py
```

地址字面在本刀**保持占位**，`7.1` 换真的——两刀各只动一处，免得抢同一行。
帽子末尾加一句：「细则往下读；只想装，看这两行就够。」

### 1.4 「Quick Start」字面

现 `:13` 写着「本页只留设计思维和 Quick Start」，页上没有这个标题。两条出口，卡上选一条：

- 甲：把那半句改成「本页只留设计思维和安装两步」——不再许诺一个不存在的标题；
- 乙：帽子那一段就叫 `## Quick Start`，让字面兑现。

乙会在「绘卷」之前多出一个 `##`，`6.24` 行判据里「第一个 `##` 之前出现 git submodule」要跟着改成「第一个 `##` **是** Quick Start 且其下出现 git submodule」。
**推荐甲**：少一个标题，帽子不与三节争层级。

### 1.5 验收怎么写成 grep

| 查什么 | 命令形状 | 应当读到 |
|---|---|---|
| 帽子在绘卷之前 | `grep -n 'git submodule' readme.md` 首个行号 < `grep -n '^## 绘卷' readme.md` 行号 | 真 |
| 四处锁句没动 | 四条 `grep -cF '<锁句原文>' readme.md` | 各 `1` |
| 英文对照在 | `grep -c 'process harness for AI coding agents' readme.md` | `1` |
| 给谁 / 不给谁都在 | `grep -c '不给谁用' readme.md` | `1` |
| 树在 | `grep -c 'your-repo/' readme.md` | `1` |
| Quick Start 字面 | 甲：`grep -c 'Quick Start' readme.md` 为 `0`；乙：`grep -c '^## Quick Start' readme.md` 为 `1` | 二选一 |
| 三节没动 | 「绘卷」「公信」「建制」三节各自 `git diff` 为空（按行范围） | 空 |
| 把关 | `bash docs_meta/tests/check-word.sh; echo $?` | `0` |

「读起来清楚不清楚」不在表里——那是人在结案那一爪判的。

### 1.6 已知的坑

- 首页别的桌也在读（`6.2`、`6.3` 两行都提过）：帽子里不要新造术语，只用页上已有的词。
- 图标 `alt` 是整段叙述，别动它，也别在帽子里重复。
- `check-word` 扫 `readme.md`，词表在脚本头；帽子若撞红，改帽子不改词表。

---

## 2 门口五件（`7.1` 的材料）

发布不是把仓库设成 public 就完了。外人 clone 下来第一眼看的是根目录，第一个要判断的是「我能不能用」。

### 2.1 LICENSE — 选哪种归人

现在根目录没有许可证。GitHub 上无许可证等于「保留所有权利」，别人拿去当子模块在法律上都站不住。

| 候选 | 适合 | 代价 |
|---|---|---|
| **MIT** | 想让人随便用、随便改、随便挂进闭源桌 | 派生品可以不回流 |
| Apache-2.0 | 同上，另带专利授权与 NOTICE 机制 | 文本长；对纯文档仓库略重 |
| CC-BY-4.0 | 把它当「一份文档」而不是「一段代码」 | `init.py`、检查脚本是代码，CC 对代码不合身 |
| CC-BY-SA-4.0 | 想要派生品同许可证回流 | 挂进闭源桌的人会犹豫 |

规划席看法（不是裁）：仓库里既有 markdown 也有 `init.py` 和十七本 shell，**MIT** 最不添麻烦；若人在意「改了要回流」，Apache-2.0 也不会拦住子模块用法。
**这一格是发授权，卡上以〔爪〕请示，附本表。**

### 2.2 `.gitignore` 加一行

```text
.claude/settings.local.json
```

现状：那个文件装 Token Plan 的 `sk-sp-` 密钥，此刻没被跟踪，但挡它的是 `C:\Users\<user>\.config\git\ignore`，不是仓库自己的规则。换机器、或别人照 skill 配一份再 `git add .`，密钥就进库。
判据用 `git check-ignore -v`，看命中的是仓库 `.gitignore` 那一行。

### 2.3 真地址

`readme.md:91` 的 `<母本仓库地址>` 换成 GitHub 地址。只换这一处字面。
Codeup 那个地址是内网工作库，不上首页。

### 2.4 反馈入口：issue 模板

`todo.md` 第 6 章「怎么提」已经是一份模板：**现象 / 出处 / 该改的地方**。搬成 `.github/ISSUE_TEMPLATE/feedback.md`：

```markdown
---
name: 反馈 / Feedback
about: 说的和做的不一致、读不懂、装不上
---

**现象** — 你看到了什么。只写看到的，不写判断。
**出处** — 盘上哪一份的哪一行（`docs_meta/src/xxx.md:NN`）。
**该改的地方** — 可以只是一个问句。

三样凑不齐也照提，缺哪一样写明。
```

外人提进来的，形状就是第 6 章能直接收的。36 桌那份 1300 行的反馈报告可以在 `CHANGELOG` 里点名——它证明这套东西被别的桌用过、撞出过十二条、且回流了。

### 2.5 `CHANGELOG.md` / release notes

第一版只要三段：

1. **这一版有什么**：子模块 + `init` 的形态；两席、两闸、卡；十七本把关；`.mirror/` 那套 harness（Claude Code 一份，Cursor 一份开关）。
2. **没有什么**：英文全页；Codex 落点；自动盖章；`docs/reports/` 样例。写「未实现」，不写「待下一阶段」（`verify.md`）。
3. **已知的坑**：指向 `todo.md` 第 6 章，不复述。

版本号建议 `v0.1.0`——「粗糙」是人自己说的，0.x 就是这个意思。

### 2.6 不发的

- `.tmp/` 全部（已 ignore）
- `.claude/settings.local.json`（2.2）
- Codeup 地址
- `docs_meta/docs/SESSION.md` 横线以下的历史审阅——它本来就随刀覆盖，发布时不用特意清

### 2.7 顺序

`7.1` 依赖 `6.24`：帽子没戴好就发出去，收到的第一条反馈一定是「不知道这是干嘛的」，而这条我们已经知道了。
打 tag、push、在 GitHub 上点 release 三样归人，在 `7.1` 结案之后按。

---

## 3 和别处对不上的

- `paradigm.md` §4 占位「怎么发？GitHub Template、公开仓库、还是先私仓自用？」——本页按**公开仓库 + 子模块**写，Template 那条路没选：Template 会 fork 整棵树，和「母本只有一份，桌一张张从它出来」对不上。这是看法，那一格占位仍在。
- `todo.md` 第 3 章章级验收说「完结后整个 `readme.md` 是统一的状态」——加帽子会不会破这个「统一」，人在 `6.24` 结案时判；本页假定帽子是普通话、三节是原文，两层并存不算不统一。
