> 新框架已提升到仓库根，未接入自用稳定版A、未发布tag。无参init/baseline的目标为本框架自身；位于submodules/dossier时默认该依赖的宿主，也可显式指定目标。旧壳由新版替代，残余私件原样保存在本机`.zwork/legacy-shell-2026-10-17/`，不作运行来源；接管见[根迁移交接](docs/reports/molt-handoff-2026-10-17.md)。

[中文](readme.md) ｜ [English](readme_en.md)

<p align="center">
  <img src="rules/figures/dossier-icon.png" width="168" alt="绘卷 Dossier：一叠卷宗里抽出一份，背上贴签，盖了朱爪印才算结">
</p>

<h1 align="center">Dossier</h1>

<p align="center">
  <b>一次一刀，盖章才算数。</b><br>
  装两行命令，你的代理从「聊着写」变成「按卷宗办事」——你只管点行、认账、拍板。
</p>

<p align="center">
  <img src="rules/figures/paradigm-shift.png" width="560" alt="碎裂消散的聊天窗＋粒子流、箭头、摊开账本上的红对勾与爪印">
</p>
<p align="center"><small>聊天气泡里的对勾会蒸发；卷宗里盖了章的对勾，立得住。</small></p>

窗口关闭，过程随之消失——设计取舍、验证经过、开发轨迹，皆不可查。Dossier 将过程留在盘上：每步有记录，每项结论有证据，是否完成，可自行查证。单次脚本无需如此；长程项目由此有迹可循——数周演进、数十轮变更，皆可追溯、可审计，因而可驾驭。

> 写给会用 AI 编程代理、但没折腾过 harness 的人。本页分三层读：安装与自转是五分钟层，地图与桌间信箱是按需层，绘卷、公信、建制是深读层。

---

## 安装与自转（五分钟层）

**Dossier 是一套给 AI 编程代理用的流程约束和 harness 配置。** 以 git submodule 挂进你的仓库，跑一次 `init`，它在你的仓库根上铺出 `docs/` 骨架、`CLAUDE.md` / `AGENTS.md` 和几份角色文件。从那以后代理按它的规矩干活：一次只做一张卡上的事；写卡和改代码是两个会话；验收判据先写下来再跑；说「通过」必须指得出能复现的证据。

**给谁用**：你让代理写的代码，测试全绿也不等于对——数值求解器、数据管线、任何交付物是「一个结论」而不是「一个能跑的东西」的项目。
**不给谁用**：失败很响的项目。编译不过、页面白屏、用户当场就能发现——这套密度在那里是税，不是保险。

```text
your-repo/
  CLAUDE.md  AGENTS.md        代理每次开工先读的约定
  .claude/   .cursor/  .codex/   角色文件、开关、执行席落点
  docs/
    TODO.md  SESSION.md       待办；本刀的运行态
    queue.md                  序列单：授权一批刀排队自己往下走
    SETUP.md                  装桌检查单（init 铺出，五步）
    archives/                 归档页：旧代待办；只追加，永不清
    cmd/  design/  reports/   每刀的卡；合同层；阶段交付
  dossier/                    子模块。母本本身，你不改它
```

### 安装两步

```text
# 从可信正式 tag 或维护者 Release 附件取得 bootstrap.py
python bootstrap.py --repository https://github.com/YFG-tec/Dossier --host-root .
```

装完它自己体检：`docs/SETUP.md` 的五步收在两个问题上——语义上，桌上的骨架和角色文件齐不齐；行为上，起步闸、基线比对是否全绿。基线落在 `.dossier/baseline.json`，一条命令 `python submodules/dossier/dossier.py baseline --here` 就能比对当前指纹。

### 这台机器自己会转

早先，这些规矩全靠你一句一句盯着。现在分三层，各归各。

先答三个进门问题。**它不带服务、不连账号**：就是一叠文件和检查脚本，跑在你自己的会话里。**两席＝两个会话**：默认规划席 Cursor、实现席 Claude Code，Codex CLI 也能坐实现席；用哪家可以换，两个会话合不成一个。**我有好几个项目呢？** 用 git 邮局：一桌一地址，领班当邮差，信箱话不作判据。它是可选适配器；不装零影响，装上也不带服务、不连账号，原先的承诺不破。

**你每天只做四件事。** 点一行待办、说一声开工、结案时认账、遇到断点拍板。就这四样，别的都有人代笔。

**代理自己会跑一批。** 把一串待办授权进 `docs/queue.md`，代理席就按序列自己往下走：代点行、写卡、派手施工、独立审查、跑验收、结案、提交到本地分支——每刀一报。它的章是**蓝印**，效力与人印相同，只标明是代理落的。七样它永远不碰，撞上就停下、把待裁的事写进队列等你一句话（你回了就续跑）：**松判据**（放宽验收标准）、**发授权**（给自己扩权）、**改序列**（动你排的队）、**动根基条款**（改这套规矩的地基）、**胖行**（把待办行写肥）、**做不到的卡**、**审查返工**。**母本仓 push 对代理永远禁止；唯一的特许是桌间邮局仓（专用凭据、只限 `.mail`），三钉之外不开口。**

**机器替你把话验真。** 二十二本机械检查一条入口全量跑；开工先过起步闸——执行架构缺了半边（有 agents 没 skills 这类「半身不遂」）当场红，不等活了半天才发现配置早丢了。**宿主**就是你用的那款代理程序（Claude Code、Cursor、Codex 这类）；母本会把角色文件翻成各宿主要的样子铺给你。换宿主不静默失灵：进 `templates/` 的配置随子模块一起旅行，宿主私有的件有清单点名，配置偏没偏有指纹可对——「宿主那份偏了没有」是一条命令的问答，`CHANGELOG` 会告诉宿主哪半边要重译。

这套自转不是变出来的。**值日手**就是定时唤醒的值班机制：系统计划任务每十分钟碰一下文件，代理的「耳朵」听见就醒来干活；一个 deadman 探针随时做三面体检——定时任务还在不在、心跳按节律跳没跳、有没有卡死的在办锁——任何一面不对就停下报告，不装没事。宿主没有定时能力也不阻塞开发：记一笔死账，等你点火。装法与拆法都在 `docs/design/loop.md`。

## 地图与桌间信箱（按需层）

### 要干什么读什么

细则按需要打开，不必先读完：

| 要干什么 | 读 |
|---|---|
| 目录长什么样、图放哪 | `rules/directory.md` |
| 一刀、卡片、收口 | `rules/workflow.md` |
| 验证、排障、这套验不了什么 | `rules/verify.md` |
| 角色、档位、模型下限 | `rules/roles.md` |
| Claude Code / Codex CLI 怎么落 | `rules/claude-code.md` |
| Cursor 怎么落 | `rules/cursor.md` |
| 队列与自动化怎么转 | `docs/design/loop.md` |
| 模型分档与派单路由 | `docs/design/model-routing.md` |
| 外面有什么、为什么不那样做 | `rules/sources.md` |
| 还没对齐的问题 | `docs/design/open.md` |
| 运行时 | Python ≥ 3.13（解释器优先 `.venv`，未建则系统，首次需要时建）、Windows 用 Git Bash 跑检查——环境自检 `bash checks/check-env.sh` |

### 桌间信箱

桌间信箱是 git 邮局：一桌一地址，领班当邮差，信箱话不作判据。它是可选适配器；不装零影响，装上也不带服务、不连账号，原先的承诺不破。

---

## 绘卷（深读层）

一叠卷宗，一次抽一份出来办。背上贴着签，不翻开就知道是哪一件。
办完盖章，盖了才算数；章不是自己盖给自己的。抽走一份，叠还在。

项目中文名是「绘卷」，英文名是 `Dossier`，名词是案卷。都是「卷」：案卷是背上贴着签的一捆（不翻开就知道是哪一件），绘卷是展开给你看的一幅（画的就是那一叠）。

| 词 | 指什么 |
|---|---|
| **Dossier** | 本仓库。这套规矩本身 |
| **桌** | 课题仓库 |
| **刀** | 桌上的一个工作单元 |

**母本只有一份，桌一张张从它出来。**

这套东西是几个数值项目里边做边收的。各桌有各自的实现和探索路径。Dossier 做的不是汇编，是**提取、统合、抽象、升级**：单桌没想到的缺口要补，不利于管理的冗余要丢掉。三桌里有的，不自动进公共层。旧桌没有义务回改。对照表见 `rules/sources.md`。

---

## 公信（深读层）

分档判据是「判据外生还是内生」，不是「项目大小」。判据外生的（有参考实现、金标准）该长跑、稀疏监督；判据内生的（自己造）该短刀、密集闸门。这套东西在前一格是税，在后一格是本体。

第二条分野是失败响不响。编译不过、对不上参考输出是响的；数值上的静默降档（枚举声明三档、内核当默认档、契约测试全绿）是不响的。**密集闸门买的不是速度，是让静默失败在一刀之内暴露。** 这条辩护不能是「模型还不够好」，只能是「判据内生 + 失败静默」这两条；哪天这两条不成立了，就该往长跑退，而不是加规矩。

这份管理密度，人类项目负担不起。它在这里成立，是因为**执行规矩的边际成本降到了近乎为零**：写卡、落盘、逐条对账，对智能体是顺手；文档是它唯一稳定的记忆。规矩定得细不是因为聪明，是因为现在定得起。

判据先声明、证据能复现、盖章的手不是干活的手。核心不是转化，是取信——不是把原料变成产品，是让一个结论**可以被相信**。连「可以结案了」都收成了一条可机读的查询：谓词红，谁说情都不算。

偏离要逐条写明代价，藏起来的偏离自己就是一类失败。欠的账摊在 `docs/TODO.md` 第 5 章、第 6 章。怎么立的，见下一节。

---

## 建制（深读层）

这套东西的骨架是五条：**两席、两闸、卡、权威分层、状态在磁盘。**

三样挂进这五条：派专职的手、举证独立复跑，挂在「两席」底下；记录只追加、档案页永不清，挂在「状态在磁盘」底下；源码 → 产物单向，挂在「权威分层」底下——只准源码 → 产物，要改就去改源码那一头；两边不一致不是判据，方向才是。

**两席**不是两个 AI 一起写代码。分工是能力差异加上权限差异。选哪个 harness 坐哪一席可以换，**两席必须是两个会话**不能换。角色不是人设，是**写权限 + 失败时许做什么**。

- 写卡的手不接着改核
- 改核的手不改测试口径
- 写测试的手不把核修到绿
- 审查的手不写文件；只核对结果和预先声明的标准
- 卡点名的路径对写卡手封（回避）：自卡落盘起只读，到结案解封

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
  <img src="rules/figures/dossier-frame.png" width="880" alt="「Dossier 的一天」：左栏红框「你」列四件事（点行、开工、认账、拍板）；中栏蓝框「代理席」六步闭环（取队列、写卡、派手施工、独立审查、跑验收、蓝印记档），角注「蓝印＝你的章」「永不 push」，红字「撞断点：停下等你」；右侧中性墨框「桌间信箱（可选）」一桌一址、不装零影响；底部横带「机器验真」（二十二本检查、起步闸、配置指纹）；红虚线＝每刀一报折回「你」认账。">
</p>

从可信正式 tag 或维护者 Release 附件取得 bootstrap.py，再选正式成品安装：

```text
python bootstrap.py --repository https://github.com/YFG-tec/Dossier --host-root .
# 显式版本加 --version TAG_OR_COMMIT；不查询 latest
```

工厂入口固定使用 `submodules/dossier`，安装实际选定成品自身的代码与模板。铺出来的是空骨架，业务内容由你写。普通已固定的 Git 子模块仍可运行 `init`；先确保 HEAD 与宿主 Gitlink 一致。

日常恢复固定版本用 `git submodule update --init -- submodules/dossier`；重跑 init 只补缺件，不升级。升级先用 factory plan，审阅计划后 factory apply；baseline refresh 只记读数。

想先看一圈怎么转：`examples/` 里有一份跑得通全流程的冒烟样例（玩具核＋假人）。

---

## 那枚爪印

写代码的速度，人早就追不上大模型了；但最后落下的那一爪，才是灵魂。
首屏插画：GLM-Image 生成，人工修裁。


### 成品与开发树

成品 tag 的根就是本安装包；手动选择已发布的正式成品 tag 后运行上述入口。开发仓根入口为 `src/dossier.py`，不能将开发分支检出误当成品。默认通过 bootstrap 选择 GitHub latest 正式 Release，显式版本不查询 latest。成品只随附起步 env 检查；本仓22项开发检查与邮箱开发夹具不随包交付。

本地 `release build` 输出可直接安装的独立Git工作目录，附带工具新建的 `.git`（无remote、无开发父历史）；版本化tree严格等于固定提交的src树。`.git`是本地元数据，不属于成品提交/tag的文件树。

## 显式更新母桌执行件

开发源码B与宿主在用的A可分开。`runtime plan`只读并向stdout输出JSON，不激活未发布源码。首次必须给出可核的旧来源与旧路径前缀：`--adopt-source REF:src@OLD_PREFIX`选择开发提交的src，`REF:.@OLD_PREFIX`选择成品根。例如旧生成件引用`src/rules/`时用`HEAD:src@src`。该来源仅为三方比较基础，不证明母桌原来由它生成。

```sh
python src/dossier.py runtime plan --ref HEAD --host-root HOST --adopt-source HEAD:src@src > plan.json
python src/dossier.py release tag vX.Y.Z --host-plan plan.json
python src/dossier.py runtime apply --tag vX.Y.Z --plan plan.json --host-root HOST
python src/dossier.py runtime status --host-root HOST
python src/dossier.py runtime rollback --host-root HOST
```

先审阅计划；冲突须人工处理后重新计划。发布成功后的宿主更新失败返回3，保留tag，用apply重试；普通未关联宿主发布保持原语义。已注册的本开发宿主正常发布会自动尝试更新，不寻找外部latest。A是`submodules/dossier`标准子模块，Gitlink固定成品P，执行件保留非冲突定制；台账、私件和其他索引不自动覆盖。仅保存最近一次有限恢复记录；回退拒绝覆盖升级后的人工编辑。成功后审阅宿主变化并在下一会话加载规则，工具不提交或push。

## Factory install and lifecycle

Obtain `bootstrap.py` from a trusted formal product tag or a maintainer-published Release attachment. Then:

```text
python bootstrap.py --repository https://github.com/YFG-tec/Dossier --host-root .
# Optional fixed tag or commit: --version TAG_OR_COMMIT
python submodules/dossier/dossier.py factory plan --repository https://github.com/YFG-tec/Dossier --host-root . > upgrade.json
python submodules/dossier/dossier.py factory apply --plan upgrade.json --host-root .
python submodules/dossier/dossier.py factory status --host-root .
python submodules/dossier/dossier.py factory rollback --host-root .
```

Non-GitHub repositories require an explicit version. Plans fix the canonical repository, selected tag/commit, product tree and host pre-state; apply never queries latest. Existing install runs preserve customizations and the fixed version. Inspect Gitlink/registration and generated changes before committing. Only the env check ships. Rollback retains one completed upgrade and refuses subsequent edits; load changed rules in a new session.

成品保留运行工具、图片与图戳；绘图生成脚本位于母本开发仓库的 `examples/figures/`。
