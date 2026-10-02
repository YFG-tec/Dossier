# Dossier 优化简评报告

| | |
|---|---|
| **日期** | 2026-10-02 |
| **作者** | codex-GLM5.3 |
| **类型** | 阶段简评 / 优化建议 |
| **写入授权** | 人 2026-10-02 原话：「写入即可，report 可以不用todo」 |
| **快照时间** | 2026-10-02 14:07:06 +08:00 |

## 1. 总判

Dossier 的核心主张已经清楚：它不是通用的 Agent 编排框架，而是一套把 **许可、状态、证据、审查、人予授权** 固化到磁盘上的开发治理范式。它最适合的对象仍是「判据内生、失败静默」的工作，例如数值求解器、数据管线、科学计算结论；对失败很响的普通应用，这套密度会是税。

当前主要矛盾已经从「范式是否想得清楚」转到「执行面是否稳定」：

> 制度文本已比较成熟，下一步的关键不是继续加规矩，而是先稳住自动化腿、跨平台运行时、状态同步和机械验证边界。

尤其是 `5.8` 已把 `close_cut.py` 固化为通用收口件。后续队列越依赖它，运行时兼容性和状态一致性问题就越不是小瑕疵，而是自动化流程的单点故障。

## 2. 当前盘面读数

本报告依据本轮只读检查，写入前盘面读数如下：

| 项 | 读数 | 简评 |
|---|---|---|
| Git | `feature/evolve` 领先 `origin/feature/evolve` 5 个提交 | 本地推进正常；push 永远归人，代理禁止 |
| HEAD | `2423ff8`，Codex 通道探针通过 | Codex 实测首刀已恢复 |
| 工作区 | `docs_meta/docs/queue.md` 已有并行改动 | 本报告只新增 reports 文件，不碰 queue |
| queue #9 | Codex 实测首刀：在办，通道已通 | 自动化主线的现场验证点 |
| queue #11 | `6.21` TODO 胖行瘦身：在办 | 已进入流程侧债务处理 |
| queue #12 | `6.23` 验不了什么总账：排队 | 建议紧随 #11，不应长期后置 |
| 5.8 | `close_cut.py` 已结案并自举收口 | 方向正确，但存在当前环境红点 |
| SESSION | 仍指向 5.8 且上半页写 builder 进行中 | 与 todo / queue 的推进面不同步 |
| 版本门面 | `CHANGELOG.md` 仍称 Codex 落点未实现，而盘上已有 `.codex/agents/` | 下一版发布前需收口叙事 |

**一个需要当场核对的状态点**：快照时 queue 里 #9 与 #11 同时标为「在办」。若这是「一刀施工、下一卡预备」的并行形态，应在断点格里写明路径不相交；若不是，则是队列推进误差。按现行「同一时刻只跑一刀」原则，这个读数不应无声存在。

## 3. 直接红点与优先处置

### 3.1 `close_cut.py` 的 Python 兼容性

在当前默认 Python 3.12.11 下执行：

```text
python docs_meta/src/tools/close_cut.py --selftest
```

结果失败：

```text
TypeError: Path.read_text() got an unexpected keyword argument 'newline'
```

原因是 `Path.read_text(..., newline=...)` 需要 Python 3.13。`PROMPT_055` 使用的是裸 `python`，没有声明版本下限，因此这不是环境无关的验收证据。

**建议**：

1. 立一刀处理运行时契约，或并入 `close_cut.py` 修补刀；
2. 二选一：改成 Python 3.12 兼容写法，或明确要求 Python >= 3.13；
3. 自测覆盖 Python 3.12 与 3.13；
4. 在该红点回绿前，不应把 `close_cut.py` 当作无风险默认收口腿。

### 3.2 整盘入口在当前 Windows 环境不可复现

`bash docs_meta/tests/run.sh` 在本会话无法启动：Windows alias 指向的 `bash.exe` 不可访问。这不是测试逻辑红，但 Dossier 的承诺是「证据可复现」，因此运行环境本身应进入合同。

**建议**：

- 写清支持的解释器与 shell；
- Windows 下明确 Git Bash / WSL / MSYS 的指定入口，或提供 PowerShell 入口；
- 固化 UTF-8 与 CRLF / LF 规则；
- 对 `init.py`、`close_cut.py`、`run.sh` 建最小跨平台矩阵。

### 3.3 状态落盘不等于状态同步

当前三个状态面出现滞后：

- `todo.md` 已把 5.8 收进已办；
- `queue.md` 已推进到后续队列；
- `SESSION.md` 上半页仍停留在 5.8 builder 进行中。

这正是「状态在磁盘」范式最怕的形状：不是没有状态，而是多个状态面对同一刀给出不同读数。

**建议增加机械对账**，至少覆盖：

- SESSION 指向的卡、todo 行、queue 状态是否一致；
- 已结刀是否仍停留在施工态；
- queue 在办项与当前许可面是否匹配；
- 收口是否产生半推进状态。

## 4. 未实现 TODO 的优先级建议

### P0：先修可信度，不扩大自动化面

| 项 | 对应事项 | 理由 |
|---|---|---|
| P0 | 运行时契约 + `close_cut.py` 兼容 | 收口件已成关键路径 |
| P0 | 收口后状态一致性检查 | 防止 todo / SESSION / queue 分叉 |
| P0 | queue 双「在办」核对 | 避免并行写盘越过「一刀」边界 |

### P1：队列既定内债

#### `6.21` TODO 胖行瘦身（queue #11）

这条排得对。TODO 胖行的根因不在结案，而在写卡阶段没有把细则从行里搬进卡。若不在写卡处瘦身，结案只会把代理写出的长行永久冻进已办区。

建议动作：

- 全程图第②步增加「行瘦身、细则进卡」箭头；
- 明确「原措辞不动」冻结的是人立案句，不是整块代理细则；
- 已办区保持两行式，不把胖块搬进历史。

#### `6.23`「验不了什么」总账（queue #12）

这条应紧随 #11。机械验收的可信度取决于是否明确说出绿灯证明不了什么。

建议在 `verify.md` 收拢八行边界，并回链 `todo.md` 对应行。总账的目标不是自贬，而是让使用者知道：

- 结构绿不等于判据真；
- 出处存在不等于语义一致；
- 权限名单存在不等于机械生效；
- 测试入口存在不等于跨平台可复现。

### P2：治理一致性

| TODO | 问题 | 建议 |
|---|---|---|
| `6.10` | 领班写不了报告，但报告内容只有领班有 | 明确报告内容归领班、通过结论归人；补 reports 权限格 |
| `6.13` | 定义层 × 手的表有多张，但权威关系不清 | 指定唯一权威表，其余标为视图或投影 |
| `6.19` | 权限名单不等于机械生效 | 先写清失效模式，再决定守卫是否产品化进 `.mirror/` |
| `4.7` | 卡片与运行态读不动 | 闸一是拒超售的门，卡片可读性是许可面可用性，不是文风偏好 |
| `4.4` | 记录层只追加未成通则 | 明确「原话 + 追记」成对搬运，禁止只搬正文丢回应 |

### P3：新能力后置

#### `5.6` 微信告警通道

有价值，但不应抢在 P0 前。通道选型、扫码绑定、首次发送、账号配置都属重大决断；若队列本体仍不稳定，告警只会把不稳定更快送给人。

#### `5.2` 言官对动摇根基决定谏一次

方向有价值，但「动摇根基」必须先写成硬判据，例如：

- 是否修改通则条款；
- 是否松判据；
- 是否改变两席、两闸、卡片唯一许可面；
- 是否影响记录不可变性。

判据未死之前不应落地，否则容易退化成模型主观「我觉得不妥」。

## 5. 仍应保留的未办项

以下事项仍应留在 TODO 中，不宜顺手合并：

- `4.2`：`naming.md` / `directory.md` 的 `docs_meta/` 旧平铺描述同步；
- `4.3`：卡号新规与历史引用悬空；
- `4.4`：记录层一律只追加；
- `4.5`：Xenia 合同层表述不准；
- `4.7`：卡片与运行态可读性；
- `5.2`：言官一次性谏言；
- `5.6`：微信告警通道；
- `6.2`：首页「三」的口径；
- `6.3`：首页「边界是物理的」是否保留；
- `6.4`：`check-ask.sh` 只认行首短横；
- `6.5`：`check-ask.sh` B 段触发不了；
- `6.6`：卡上现算值与表格预测值双写漂移；
- `6.7`：SESSION 过期家具句；
- `6.9`：通读页行号无固定动作；
- `6.10`：报告权限与内容归属；
- `6.13`：三张定义表的权威关系；
- `6.16`：SESSION 寿命规则待外部桌复验；
- `6.19`：权限名单不是机械边界；
- `6.21`：TODO 胖行瘦身；
- `6.22`：转译层机械保护；
- `6.23`：机械验证边界总账。

另有三行虽仍带未勾选框，但已被其他刀吸收，应通过正式动作清账，而不是继续当独立待办：

- `4.1` 已由 `3.3` 吸收；
- `6.17` 已由 `6.15` 吸收；
- `6.18` 已由 `6.15` 吸收。

## 6. 建议路线

```text
P0  运行时契约 + close_cut.py Python 兼容
P0  收口后状态一致性检查
P0  核对 queue 双「在办」是否为合法并行预备
P1  queue #11：6.21 TODO 胖行瘦身
P1  queue #12：6.23 验不了什么总账
P2  6.10 报告权限、6.13 权威表、6.19 机械权限
P2  4.7 卡片可读性、4.4 记录层只追加
P3  5.6 微信告警、5.2 言官谏言
```

## 7. 结语

Dossier 当前最大的风险不是规矩不够多，而是：

1. 自动化工具刚成为关键路径，兼容性却未稳定；
2. 多个状态面已经出现滞后；
3. 机械验证的证明边界尚未总账化；
4. 一部分权限仍停留在文本自律，而非机械边界。

因此下一阶段的优化方向应是：

> 先修运行时、状态同步和验证边界；再做报告权限与 TODO 瘦身；最后扩展告警、谏言等新能力。

## 8. 追记：Agent 开发的市场对照与定位补章

**追记时间**：2026-10-02  
**背景修正**：当前项目本身就是开发进行时；autocode / 三席运作正在推进，并用沙箱完成隔离。因此本补章不把「尚未完全产品化」当成运行受阻，而是把它读成现阶段的实跑验证。

### 8.1 问题重述

这里比较的不是普通软件开发的文档留痕，而是：

> **AI Agent 自身的开发过程，如何对 prompt、工具、角色、评测、运行轨迹、失败案例、版本、授权与发布做系统性留痕。**

从这个限定看，市场上有大量相邻物，但成熟品多集中在 runtime、observability、workflow 与 SDD，缺少一个专门的 **Agent Development Governance Layer**。

### 8.2 市场分层

| 层 | 代表产品 / 框架 | 它们解决的问题 | 与 Dossier 的差异 |
|---|---|---|---|
| Agent runtime / orchestration | LangGraph、OpenAI Agents SDK、Google ADK、CrewAI、AutoGen / AG2、Microsoft Agent Framework、LlamaIndex Workflows、Pydantic AI | Agent 状态机、工具调用、多角色协作、human-in-the-loop、checkpoint | 它们回答「Agent 怎么跑」，不回答「这版 Agent 为什么被允许这样跑」 |
| Observability / evaluation | LangSmith、Langfuse、Arize Phoenix、W&B Weave、Braintrust、AgentOps、Helicone | trace、成本、延迟、prompt 版本、数据集、评分、回归评测 | 它们回答「运行时发生了什么、效果如何」，不承载许可面、审批链、写权限与结案治理 |
| Spec-driven development | GitHub Spec Kit、OpenSpec、BMAD、Kiro、tiny-spec、Anatomia | 规格先行、任务拆解、实施、审查、converge | 多数是通用软件流程，不理解 Agent 特有资产：tool contract、prompt policy、memory policy、red-team set、release gate |
| 低代码 / 工作流平台 | Dify、Langflow、Flowise、n8n、Voiceflow、Botpress | 可视化编排、发布、运行日志、workflow 版本 | 留的是配置与运行记录，不是工程治理链；难以回答谁批准扩大工具权限、哪些失败案例锁入回归 |
| Memory / knowledge | Letta、Zep、Mem0、Graphiti | 长期记忆、用户状态、知识检索 | 留的是使用过程记忆演化，不是开发决策与授权历史 |

### 8.3 真正的市场空位

现有产品常覆盖其中一环，但很少同时回答：

1. 这个 Agent 的行为边界是谁批准的；
2. 这版 prompt 为什么修改；
3. 工具权限为什么扩大；
4. 哪些 golden cases 必须通过；
5. 哪些 red-team / safety cases 必须失败；
6. 成本与延迟预算是否过门；
7. 审查结论是否原文送达；
8. 失败案例是否沉淀为永久回归；
9. 发布是否可回滚；
10. 「为什么这一版被允许上线」能否从盘上重建。

因此，Dossier 的差异化不应表述为「又一个 Agent 编排器」或「又一个 SDD 工具」，而应表述为：

> **repo-native 的 Agent 开发治理层：用文档承载许可、权力、证据、审查与历史，使 Agent 开发过程本身可审计。**

### 8.4 若面向 Agent 开发，应补的文档资产

| 资产 | 内容 | 作用 |
|---|---|---|
| Agent Charter | 目标、禁令、可用模型、可调用工具、数据边界、必须停下的人介入点 | Agent 的权力边界 |
| Tool Contract | 输入、输出、副作用、写权限、失败模式、幂等性、撤销方式 | 防止 tool permission 成为最大漏洞 |
| Prompt / Policy Record | prompt 版本、变更原因、适用场景、禁止行为、已知失败、关联评测 | 把 prompt 当合同而非字符串 |
| Eval Contract | golden set、red-team set、回归集、成本上限、延迟上限、禁止优化指标 | 防止局部案例变好、边缘案例变坏 |
| Failure Ledger | 输入、错误行为、根因、修复刀、新增回归、防再犯机制 | 把行为漂移变成可累积资产 |
| Release Gate | 功能、安全、成本、延迟、工具权限、回归、审批、回滚 | 明确上线条件 |
| Runtime Evidence Binding | 卡片 ↔ 评测运行 ↔ trace group ↔ 审查页 ↔ release note | 让文档指向可复现证据，而不是自述 |

一个可能的落点是：

```text
docs/design/agents/<agent-name>/
  charter.md
  model-policy.md
  memory-policy.md
  safety.md
  release-gate.md

docs/design/tools/
  search.md
  database-write.md
  code-execution.md

docs/design/prompts/
  system-prompt.md
  router-prompt.md

docs/design/evals/
  golden-set.md
  red-team-set.md
  regression-set.md

docs/reports/
  eval-report-YYYY-MM-DD.md
  incident-YYYY-MM-DD.md
```

### 8.5 对当前 Dossier / Codex 运行态的修正解读

当前 autocode 已经按三席运作：

```text
规划席
实现席
代理席
```

并用沙箱完成隔离。这个事实改变了前文的一个判断：

- 前文说「一部分权限仍停留在文本自律」；
- 现阶段更准确的读法是：**Codex 沙箱已经在实跑中承担机械隔离，剩余问题不是有没有隔离，而是隔离效果是否进入可复现验收。**

因此建议下一阶段的 Codex 实测不仅证明「通道 alive」，还应输出一张三席隔离读数表：

| 席 | 启动形态 | 可写面 | 沙箱 | 禁写是否被拦 | 证据 |
|---|---|---|---|---|---|
| 规划席 | 独立上下文 | docs / design / card / SESSION | workspace-write 或指定 roots | 是 / 否 | 日志 |
| 实现席 builder | 独立 Codex 会话 | 卡片点名 src 路径 + `.tmp/` | workspace-write / roots | 是 / 否 | diff |
| 实现席 tester | 独立会话 | tests + `.tmp/` | roots | 是 / 否 | diff |
| review | 独立会话 | 无 | read-only | 是 / 否 | status / log |
| 代理席 | 独立控制器 / 会话 | queue 状态与断点 | 受限写 | 是 / 否 | queue diff |

这张表不应成为新的第二真相，而应作为 `6.23`「验不了什么」的配套：说明沙箱证明了什么，也说明它证明不了什么。

### 8.6 战略结论

Dossier 不应与 LangGraph、OpenAI Agents SDK、LangSmith、Langfuse、Dify 竞争 runtime 或 observability；正确关系是互补：

```text
LangGraph / OpenAI Agents SDK / CrewAI
  负责 Agent 怎么运行

LangSmith / Langfuse / Phoenix / Braintrust
 负责 Agent 运行轨迹与评测证据

Dossier
  负责 Agent 开发过程中的许可、审批、审查、证据绑定、失败沉淀与发布治理
```

因此，面向 Agent 开发时的产品空位是明确的：

> 市面上已经有 Agent runtime 和 Agent observability，但缺少一套把 Agent 开发本身变成可审计治理流程的 repo-native 文档治理层。Dossier 可以占这一层。

这条追记不新增 TODO、不改变当前 autocode 三席运作，也不把进行中的沙箱实验视作外部风险；它只补充市场定位与后续产品化方向。
