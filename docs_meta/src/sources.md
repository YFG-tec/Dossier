# 来源与外部对照

不铺进宿主工作区。原则见仓库根 `readme.md`。

三桌是**来源**，用来对照「哪一条是踩坑之后留下的」，不是本规范的合规实现。
各桌有各自的实现方式和探索路径。Dossier 做的不是汇编，是提取、统合、抽象、升级：
单桌没考虑到的缺口要补，不利于管理的冗余要丢掉。三桌里有的，不自动进公共层。

早期项目**没有义务回改**。新开的数值桌按母本；旧桌按各自 `CLAUDE.md` 继续跑。
文中写「三桌都有 / 三桌对照」，意思是溯源，不是说它们已经长成 `directory.md` 那张公共顶层。

今天拍板、旧桌尚未跟的，目前就两条：`tests/` 在仓库根上；阶段报告在 `docs/reports/`。

## 三桌

| # | 路径 | 大约处在哪一段 | 和今天这张图不一致的地方（举例） |
|---|---|---|---|
| 1 | `D:\01_Pyjobs\Xenia_Multi_Fluid`（`hd/` / `mhd/`） | 最早长出双席、指令卡、`.tmp/` | 交付散在 `docs/reports/` 与 `examples/*/REPORT.md`；文档地图仍带课题锁 |
| 2 | `D:\01_Pyjobs\31_operator_split` | 验证诚信和探索/验证分界收得最干净 | `TODO.md` 在根上；阶段报告在根 `reports/`；测试在 `src/tests/`；**无** `.claude/agents/` |
| 3 | `D:\01_Pyjobs\29_slow_mhd` | 最接近后来的科研桌 | 阶段报告叫 `docs/report/`（单数）；其余已大体同构 |

## 外部对照（只补特性，不换范式）

2026-09-06 扫过 git 上几类近亲。结论先写：

**没有又短又强到值得换掉这一套的。** 外面要么是更重的软件 SDLC（Spec Kit / BMAD / Anatomia 引擎），要么是科研 cookiecutter（SMAIRT），要么是目录脚手架但不懂代理。Dossier 已经更贴数值：权威分层、一刀、角色写权限、`.tmp/` 零权威。下面只偷能贴上去的薄特性。

| 东西 | 它在干什么 | 和 Dossier 的关系 |
|---|---|---|
| [AGENTS.md](https://agents.md) 标准 | 给代理的短 README；Always / Ask / Never | 已有 `AGENTS.md`。可偷三栏边界，保持短锁 |
| [GitHub Spec Kit](https://github.com/github/spec-kit) | constitution → specify → plan → tasks → implement → **converge** | 一刀已经把 specify/plan/tasks 压进卡片。可偷收口对账，不要整条 SDLC |
| [Anatomia](https://github.com/anatomia-dev/anatomia) | Think / Plan / Build / **Verify 不读 Build 自评**；测试绿要封存跑出来的日志 | 角色拆法同构。可偷「审查盲评」和「绿必须落盘」。不要 CLI 引擎和 proof chain |
| [SMAIRT](https://github.com/PNNL-CompBio/smairt-template)（PNNL cookiecutter） | 假说 → 实验 → 分析；`CONTEXT_INDEX`；`KNOWN_PATTERNS` | 最近的科研近亲。目录是 `experiments/01_synthetic`，和 `src/` / `.tmp/` 打架。树就是索引，不另写 `docs/README` |
| BMAD + Spec-Kit 控制面 | npm 安装、审计环、证据链 TRACE/EVD | 太重。证据链 = 卡片 + 测试输出 + `docs/reports/` |
| cookiecutter / GitHub Template | 生成新仓库 | 一次性生成新仓库，和子模块 + `init` 不是一路。旧桌要对齐走 `init`，不必另起一个仓库 |
| 各类 `agentic-dev-template` | 12 个 slash、SPEC.md 开场 | 写卡已经覆盖。agent 数量是税 |

没有看到专门为**数值离散 + 验证门 + 探索/验证分界**写的公共范式。

**1 和 2 不做。** 「三栏边界」「审查盲评」是外面的叫法；短锁和收口里已经有。
**3、4** 是领班收口，见 `workflow.md`。
不补：constitution 五段流水线、16 个 agent、cookiecutter 问卷、假说目录替代 `.tmp/`、论文草稿树、hashed proof chain。

公开工具里，最接近「拿一份现成的开新仓库」的是 **GitHub Template Repository**。
Spec Kit 的 `specify init` **也**拿它管新建和已有仓库两档——`init` 是各家脚手架通用的那个词，母本跟的是业内习惯，不是从某一家抄的。旧桌要对齐，走的是同一个 `init`。

## 补录 2026-09-07：贴着骨架长的那几个

上一轮扫的是范式级远亲。这一轮几个是同构的，差异更值得读。

| 东西 | 它在干什么 | 和 Dossier 的关系 |
|---|---|---|
| [tiny-spec](https://github.com/GrayMa77er/tiny-spec) | 7 skills + 2 agents；ticket → design → tasks → **一次一个**；每个 task 一只手实现，**独立 reviewer 跑真实测试打分**，过了才 commit | 目前最像的一个。③④⑤ + 收口几乎同构。**分歧：它的 reviewer 是闸** |
| [CCFlow](https://github.com/ScaleLabs-Dev/CCFlow) | `codeImplementer` / `testEngineer` / `Reviewer`；TDD 100% GREEN gate；memory bank | 角色切法一字不差，但**按人设分工，不按写路径分工** |
| [claude-code-my-workflow](https://github.com/pedrohcgs/claude-code-my-workflow) | 学术仓库模板（LaTeX + R）；multi-agent review、adversarial QA、replication protocol；**种缺陷测 reviewer 的 recall 与误报** | 最近的科研近亲。种缺陷那条要偷 |
| [GitHub Agentic Workflows](https://github.github.com/gh-aw/reference/permissions/)（gh-aw） | agent 的 job **只读**；写操作走 safe outputs，由**不跑 agent 的独立 job** 落地 | 唯一把权限当一等公民的。**它的隔离比 Dossier 硬一层** |
| [Dive-into-Claude-Code](https://github.com/VILA-Lab/Dive-into-Claude-Code) | 六个编排模式：adversarial verification、generate-and-filter、loop-until-done；把协调状态从模型上下文搬进脚本 | 「状态在磁盘，不在聊天」的学术表述 |

**外面的 reviewer 全是闸，Dossier 的审查不是。** tiny-spec 的 reviewer 能挡 commit，CCFlow 有 GREEN gate。
Dossier 把否决权留给人，审查只有「不被改写地送达」的权利（`roles.md`）。
这是取向分歧，不是谁做得糙：交给一个也是模型的东西去拍板，等于把那一爪让出去。

**两条值得偷：**

1. **种缺陷测审查。** 往干净的控制组里种一个缺陷，看审查抓不抓得到，报 recall 和误报率。
   这是 `verify.md`「写测试先问：什么样的实现 bug 会让它报错」的**可测量版本**——把自问变成实测。
   也是审查改成「动了 `src/` 就派」之后唯一能验的事：抓不到，这只手就是仪式。
2. **进程隔离**（长期方向）。gh-aw 的结论：能在 prompt injection 下真扛住的是 job 隔离；
   tool denylist 和 bounded write directory 只是纵深防御。**Dossier 现在全部靠后两层**——
   审查禁写靠 `disallowedTools`，路径隔离靠约定，同一个进程、同一份凭证。本地交互式开发用不起 CI 那套，但这是真实边界。

## 正面冲击：Anthropic 自己那篇

[Long-running Claude for scientific computing](https://www.anthropic.com/research/long-running-Claude)。
不是某个 repo，是官方，而且**用例完全重合**：重写数值求解器、Fortran 迁移、对着参考实现调试大代码库。
它的做法和这套正相反——本地把 plan 迭代好、编进 `CLAUDE.md`、在计算节点的 tmux 里开一个会话、detach、几小时后上 GitHub 看一眼。

**长跑 + 稀疏监督** vs **短刀 + 密集闸门**。它没说这套错，它说的是不需要这么细。这一节摆出来是为了讨论，不是为了驳倒。

**两边赌的是同一个变量：判据能不能预先说清。**

它自己的句子里就写着适配条件——「well-scoped, success criteria are clear」。
重写求解器有参考实现，Fortran 迁移有原码：**判据是外生的、现成的**，对齐参考输出就行。这种情况下密集闸门确实是税。
Dossier 的场景没有参考实现。新离散格式、新物理耦合，判据要自己造，而且常常做到一半才知道该怎么判。
判据内生，就必须有人在每一刀开工前把它写下来——那就是卡片。

所以这可以直接当**分档判据**，不是立场：

| | 判据外生（有参考实现 / 金标准） | 判据内生（自己造） |
|---|---|---|
| 该怎么跑 | 长跑，稀疏监督 | 短刀，密集闸门 |
| Dossier | 是税 | 是本体 |

**第二个分野：失败响不响。**
它举的三个用例失败都很响——编译不过、对不上参考输出、测试红。
数值研发的失败是**静默**的：Xenia 那堆补丁的根因是枚举声明了 `plm`/`weno3`、内核静默当 PCM，契约测试全绿。
静默失败下，「偶尔上 GitHub 看一眼」看不到东西。**密集闸门买的不是速度，是让静默失败在一刀之内暴露。**

**它对的地方要认：**

- tmux + 计算节点 + detach 这套长跑工程，Dossier 一个字没写，该补。
  长跑和一刀本来不冲突——**一刀内部可以跑几小时，闸在刀的两端，不在中间**。
- 「把 plan 迭代好再编进 `CLAUDE.md`」= 先议事、先立合同层，和 `workflow.md`「开桌」是同一个动作。
  分歧只在 plan 之后要不要一刀刀切。（差别在于它假设 plan 一次能定完——判据外生时确实能。）

**留一条存疑，别自欺：** 模型长程能力再涨，密集闸门的性价比会掉。
这套的辩护**不能**是「模型还不够好」——只能是「判据内生 + 失败静默」这两条。
哪天这两条不成立了，就该往长跑退。见 `../docs/design/open.md`。

顺带一个对偶：`readme` 说「这份管理密度人类负担不起，让人执行一天做不完两件事」；
那篇说的是让代理自己跑几小时。两边都承认人做不动，分歧在于**省下的那份精力给谁**——
Dossier 给了闸门密度，Anthropic 给了任务长度。

## 仍然没人做的

搜到这里为止是空的：

- **目录 = 权威等级**作为范式核心。gh-aw 有 bounded write area，但那是安全机制，不是项目结构学。没人把「谁说了算」摆成层 × 手的一个面。
- **审查不被改写地送达**。外面要么 reviewer 是闸，要么结论被 orchestrator 汇总；领班当抄手那条没见到第二家。
- **退卡 / 封驳**。所有框架都假定卡片是对的，没有一个处理「卡片本身不合理」。
- **`.tmp/` 零权威层**。
- 数值专用的验证门（收敛阶 / MMS / 网格细化）。

结论没变：**没有值得换掉的；有两条值得偷。**
