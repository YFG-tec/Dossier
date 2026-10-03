# Dossier Runtime 技术选型简评：DeepSeek Harness 作为底座

| | |
|---|---|
| **日期** | 2026-10-02 |
| **作者** | codex-GLM5.3 |
| **状态** | 初步讨论稿 / 技术选型备忘，不是立项卡 |
| **对象** | Dossier 后续可安装 Agent App 的 runtime 底座选型 |
| **候选简称** | DSH = DeepSeek Harness |
| **写入授权** | 人 2026-10-02 原话：「现在在做技术选型，我有点倾向dsh去做runtime 的底座，不过也只是初步讨论，补一个新的独立report文档」 |
| **证据边界** | 本文基于当前对 DSH 的公开形态理解与 Dossier 自身需求做架构评估；本轮未对 DSH 源码逐行审计，结论不能读成已完成 due diligence。 |

## 1. 结论先行

**倾向合理，但建议采用“条件采用”而不是立即押独。**

推荐定位：

> DSH 可以作为 Dossier Agent App 的 **开源执行 runtime 底座候选**，但 Dossier 的法律层、状态层、模型池策略、角色权限与审计链不能交给 DSH 管理。

更具体地说：

```text
Dossier
  负责：许可面、三席、模型池、角色池、审批、证据、审计、结案

DSH
  负责：Agent 执行、工具调用、模型适配、运行循环、沙箱执行底座
```

第一阶段的正确采用方式不是“把 Dossier 迁到 DSH”，而是：

> 给 Dossier 做一个 DSH executor adapter，让 DSH 与 Codex / Claude Code / Shell 并列成为执行后端。

这样可以吃到开源 runtime 的优势，同时避免把 Dossier 的核心价值绑死在另一个 harness 的内部抽象上。

## 2. 为什么 DSH 有吸引力

### 2.1 开源可审计

相比封闭 Code App，开源 harness 最大的优势不是“免费”，而是可以检查：

- system prompt 如何组装；
- tool call 如何解析；
-上下文如何压缩；
-命令如何执行；
-权限如何判断；
-失败如何重试；
-状态是否落盘；
-是否上传不必要的数据；
-是否对某家模型有隐性依赖。

Dossier 的核心承诺是可审计的开发过程；runtime 自身可审计是自然需求。

### 2.2 自托管与本地部署

如果 DSH 能私有部署，Dossier App 可以覆盖：

- 内网代码；
-科研代码；
-涉敏项目；
-离线环境；
-长期可复现运行。

这对科研 / 数值类项目尤其重要。闭源 SaaS Code App 在这些场景中天然受限。

### 2.3 开放权重带来版本锚定

DeepSeek 系模型的开放权重对 Dossier 有特殊价值：

- reviewer 可以固定模型版本；
-回归集可以长期复跑；
-历史审查结论可解释；
-离线场景可运行；
-模型行为漂移风险低于纯 API 型模型。

Dossier 已有“模型下限表”的思想。开放权重让“固定 reviewer / 固定断点判断模型”更容易落地。

### 2.4 更可能贴近开放协议

DeepSeek 生态通常与 OpenAI-compatible API、vLLM、SGLang 等开源栈亲和。如果 DSH 的 provider 层足够干净，它比封闭 Code App 更容易接入：

```text
DeepSeek API
本地 DeepSeek 权重
OpenAI-compatible endpoint
LiteLLM / Portkey
OpenRouter
其他开源模型
```

这符合 Dossier App 的模型池构想。

## 3. 核心风险：开源不等于模型中立

DSH 需要被检验的第一问题不是“功能强不强”，而是：

> 它是一个模型无关的 Agent runtime，还是一个支持其他模型的 DeepSeek Agent？

这两者差别很大。

### 3.1 隐性 DeepSeek 绑定

常见绑定方式包括：

| 绑定点 | 症状 |
|---|---|
| prompt 模板 | system prompt 只针对 DeepSeek 对话风格调优 |
| tool call 解析 | 函数调用解析只对 DeepSeek 输出稳定 |
| reasoning 通道 | 核心流程依赖 DeepSeek 特有推理输出 |
| context 压缩 | tokenizer、窗口、摘要策略按 DeepSeek 优化 |
| 默认模型 | 所有角色默认走 DeepSeek endpoint |
| CI | 只测 DeepSeek provider |
| 登录 / 计费 | 与 DeepSeek 服务强耦合 |
|评测集 | 只证明 DeepSeek 模型上的效果 |

如果这些逻辑写进核心，而不是 provider adapter，那么 DSH 只是锁得更透明的供应商 harness。

### 3.2 最低公分母问题

为了兼容所有模型，开源 runtime 可能只支持最基础的 chat completion 和简单工具调用，导致对每个模型的深度能力都用不好。

正确架构应该是：

```text
核心协议小
能力扩展可插拔
模型声明能力
工作流按能力选择
```

而不是：

```text
所有模型都被当成同一个聊天补全器
```

### 3.3 安全边界可能晚于功能成熟

开源 Agent 项目常见演进顺序是：

```text
工具调用 → 多 Agent → UI → 插件生态 → 最后才补沙箱
```

但 Dossier 的顺序必须相反：

```text
许可面 → 写权限 → 沙箱 → 审查 → 证据 → 再谈多 Agent 扩展
```

如果 DSH 的沙箱、worktree、权限事件还不成熟，它不能直接成为 Dossier 的唯一底座。

## 4. Dossier 需要从 runtime 得到什么

Dossier App 的分层目标应当是：

```text
Dossier Governance Layer
  卡片、三席、queue、人闸、模型下限、角色权限、审计、结案

Role / Model / Workflow Registry
  模型能力卡、角色卡、模型路由、工作流模板

Executor Layer
  Codex adapter
  Claude Code adapter
  DSH adapter
  Shell / Python adapter

Sandbox / Git Layer
  writable roots
  read-only review
  worktree
  diff / log / artifact
```

DSH 应竞争的是 Executor Layer，而不是 Governance Layer。

### 4.1 必需能力

| 能力 | Dossier 用途 |
|---|---|
| 独立进程执行 | 三席 / 三上下文隔离 |
| 模型 provider 抽象 | 模型池与角色池解耦 |
| tool call 事件协议 | 统一证据与审计 |
| 文件写边界 | builder / tester / review 权限落地 |
| 只读执行 | review 零写 |
| worktree 支持 | 一刀一工作区 |
| 命令执行 | 跑测试与验收 |
| artifact 输出 | diff、日志、结果表 |
| 中断恢复 | 长任务与 crash recovery |
| 成本 / token 读数 | 模型路由与预算 |
| 可关闭遥测 | 内网与隐私场景 |

### 4.2 非必需但加分

| 能力 | 价值 |
|---|---|
| 多 Agent 图执行 | 未来实时工作流 |
| checkpoint | 长刀内部恢复 |
| provider mock | CI 中无网络测试 |
| 本地模型支持 | 离线与版本锚定 |
| 插件系统 | Dossier adapter 不用 fork 核心 |
| trace 导出 | 与 Langfuse / OpenTelemetry 对接 |
| 沙箱后端 | OS 级隔离 |
| 多平台 | Windows / macOS / Linux |

## 5. 推荐架构：DSH 作为 adapter，不是真相源

第一阶段不要让 DSH 直接管理 Dossier 的 queue、卡片或结案。推荐边界如下：

```text
Dossier Core
  读 todo / SESSION / card / queue
  计算许可面
  选择角色与模型
  生成 DSH TaskSpec

DSH Adapter
  启动 DSH runtime
  传入角色指令
  传入模型配置
  传入 writable roots
  采集事件与 artifact

DSH Runtime
  执行 Agent
  调工具
  跑命令
  产生 trace / diff / log

Dossier Evidence Layer
  验证输出
  判断是否越权
  贴审查页
  更新 queue / SESSION
  结案或断点
```

关键原则：

1. DSH 可以执行，不盖章；
2. DSH 可以建议，不改许可面；
3. DSH 可以产出证据，不定义判据；
4. DSH 可以调度模型，不拥有角色权限；
5. Dossier 的 Markdown / git 状态仍是唯一真相。

## 6. DSH TaskSpec 应该长什么样

为了防止 Dossier 被 DSH 内部对象污染，两者之间应有稳定的任务契约。

示例：

```yaml
task_id: PROMPT_057-builder
role: builder
dossier_card: docs/cmd/PROMPT_057.md
objective: >
  Implement only the paths declared by the card.

model_policy:
  mode: policy-binding
  min_class: coding-strong
  preferred:
    - deepseek-coder
  fallback:
    - openai-compatible-coding-model

permissions:
  writable_roots:
    - docs_meta/src/tools/
  readable_roots:
    - .tmp/
  forbidden_roots:
    - docs_meta/tests/
  network: false
  git_commit: false
  git_push: false

tools:
  - read_file
  - write_file
  - run_tests

output_contract:
  - changed_files
  - diff
  - run_log
  - completion_report

stop_conditions:
  - card_infeasible
  - test_red_after_fix
  - permission_denied
  - budget_exceeded
  - ambiguous_scope

evidence:
  artifact_dir: .tmp/dsh/PROMPT_057/
  trace: required
  model_version: required
  selection_reason: required
```

这个 TaskSpec 是 Dossier → DSH 的单向输入。  
DSH 返回事件和 artifact，不直接改 Dossier 状态。

## 7. 与模型池 / 角色池的关系

用户的长期构想是：

```text
模型池：每个模型有能力说明
角色池：固定管理角色 + 动态执行角色
场景路由：不同问题实时组装工作流
```

DSH 在其中可以承担 runtime，但不应自动成为模型注册表。

### 7.1 Model Registry 应留在 Dossier

模型卡应包含：

```yaml
model: deepseek-coder-x
class: coding
strengths:
  - code_generation
  - refactoring
weaknesses:
  - long_horizon_planning
context: 128k
tool_calling: strong
json_output: strong
cost: medium
latency: medium
deployment:
  - deepseek-api
  - local-vllm
allowed_roles:
  - builder
forbidden_roles:
  - reviewer
```

### 7.2 Role Registry 也应留在 Dossier

```yaml
role: reviewer
requires:
  reasoning: high
  code_review: high
writable_roots: []
model_policy:
  mode: fixed-floor
  min_class: heavy-reasoning
```

### 7.3 DSH 只消费绑定结果

也就是说：

```text
Dossier 选择：角色 + 模型 + 权限 + 工作流
DSH 执行：这个已编译好的任务
```

如果 DSH 自带模型路由能力强，可以作为一个 routing backend，但不能成为唯一政策源。

## 8. 与现有三席 / autocode 的关系

当前项目已经是开发进行时，autocode / 三席运作中，并用沙箱完成隔离。DSH 选型不应打断这条线。

推荐关系：

```text
当前 autocode / Codex 实验
  继续作为第一实跑验证线

DSH 技术选型
  作为第二 runtime 候选线

Dossier App
  最终通过 adapter 支持两者
```

第一阶段不改当前三席。  
DSH 的 PoC 可以独立进行，路径只落在实验目录或外部队列，不抢当前刀的写面。

## 9. 技术选型评估矩阵

建议按以下权重评估：

| 维度 | 权重 | 关键问题 |
|---|---:|---|
| 治理兼容性 | 25% | 能否只做 executor，不拥有真相 |
| 沙箱与权限 | 20% | writable roots / read-only / 越权事件 |
| 模型中立性 | 15% | 非 DeepSeek provider 是否一等公民 |
| 工程成熟度 | 10% | 文档、测试、发布、API 稳定性 |
| 可自托管 | 10% | 内网、离线、私有部署 |
| 可观测性 | 8% | trace、artifact、token、模型版本 |
| 可恢复性 | 7% | crash 后能否从磁盘恢复 |
| 社区 / 生态 | 5% | 插件、贡献、维护节奏 |

候选比较：

| 方案 | 优势 | 劣势 | 初判 |
|---|---|---|---|
| DSH 作为 runtime 底座 | 开源、可自托管、开放权重生态、可能模型中立 | 需验证模型中立、沙箱、稳定性 | **优先 PoC** |
| Codex 作为主执行席 | 当前三席实验已在跑，能力强 | 商业 harness，供应商中心，不可完全掌控 | 继续作为主力 adapter |
| Claude Code 作为执行席 | Agent 能力成熟，角色文件已有 | 同样是商业 harness，绑定供应商 | 保留 adapter |
| LangGraph + LiteLLM 自研 | 抽象干净、可控 | runtime / 工具 / 沙箱都要自己补，工程量大 | 备选架构 |
| Dify / Flowise / n8n | 快速搭工作流 | 偏运营型 workflow，不适合 repo 治理核心 | 不适合底座 |
| 完全自研 runtime | 最符合 Dossier 语义 | 成本高，先重复造轮子 | 后置 |

## 10. DSH PoC 验收门

建议用 10 个小实验判断是否可采用。未过前，不宣布选型完成。

### G1 Provider mock

给 DSH 一个 OpenAI-compatible mock provider。

- 核心流程是否能跑；
- 是否隐性要求 DeepSeek endpoint；
- CI 是否可无网络测试。

**通过标准**：mock provider 下能完成一次 read → tool call → write artifact。

### G2 非 DeepSeek 模型

接入一个非 DeepSeek 模型，例如 OpenAI、Anthropic 或本地小模型。

- tool call 是否稳定；
- JSON / 参数解析是否可靠；
-失败是否可恢复。

**通过标准**：非 DeepSeek provider 不是 workaround，而是正常 adapter。

### G3 Writable roots

builder 只允许写指定目录。

**通过标准**：

- 写允许目录成功；
- 写禁区失败；
- 越权尝试进入事件日志。

### G4 Read-only review

reviewer 无写权限，但仍能读文件和跑指定命令。

**通过标准**：

- 文件写入被拦；
-命令不产生仓库写；
-事件日志可导出。

### G5 Worktree 隔离

每刀独立 worktree。

**通过标准**：

- 主工作区不被污染；
- diff 可限定在本刀；
- worktree 可清理或恢复。

### G6 状态恢复

进程中途 kill，重新启动。

**通过标准**：

- DSH 不依赖聊天上下文恢复；
-任务状态可从磁盘重建；
-不会重复执行破坏性写入。

### G7 Artifact 完整性

一次运行必须产出：

```text
trace
model version
tool calls
diff
stdout / stderr
exit code
cost / tokens
selection reason
```

**通过标准**：Dossier Evidence Layer 能直接消费。

### G8 模型路由注入

由 Dossier 指定模型，而不是 DSH 自动选择。

**通过标准**：

-外部 model policy 可注入；
-DSH 记录选择原因；
-不允许 DSH 因模型能力改变角色权限。

### G9 三席并发

规划席、实现席、代理席同时存在。

**通过标准**：

-上下文隔离；
-文件权限隔离；
-无共享可变状态；
-事件不串线。

### G10 Dossier smoke cut

用 DSH 跑一个极小的 Dossier 卡片。

**通过标准**：

- card → TaskSpec 可编译；
- builder 输出在许可面内；
- tester 可跑命令；
- review 只读；
- Dossier 可对账；
-不 push、不越权、不直接勾 TODO。

## 11. 分阶段路线

### Phase 0：纸面审计

不改代码，只读 DSH 源码与文档。

产出：

- provider 层架构图；
- tool call 协议；
-权限 / 沙箱实现；
-状态存储；
-插件边界；
-CI provider matrix；
-已知平台限制。

### Phase 1：DSH adapter spike

做一个最小 adapter：

```text
Dossier TaskSpec → DSH runtime → artifact
```

不接完整三席，只跑单角色。

### Phase 2：沙箱与权限 PoC

重点验证：

- writable roots；
- read-only review；
- worktree；
-越权事件；
-命令白名单。

### Phase 3：Dossier smoke cut

跑最小卡片：

```text
builder → tester → review → evidence
```

不自动结案，不自动 commit。

### Phase 4：与 Codex / CC 对照

同一张卡分别在：

```text
Codex adapter
Claude Code adapter
DSH adapter
```

执行，比较：

-成功率；
-越权率；
-成本；
-延迟；
-证据完整性；
-审查抓错率；
-恢复能力。

### Phase 5：决定底座层级

可能结论有三种：

1. **DSH 成为主 runtime**：多 executor 中优先；
2. **DSH 成为本地 / 开源 executor**：云端仍用 Codex / CC；
3. **DSH 不采用**：保留实验结论，回到 LangGraph / 自研轻量 runtime。

## 12. 需要防范的选型错误

### 错误一：把 runtime 当治理层

DSH 能执行 Agent，不代表它应该拥有 Dossier 的卡片、queue、审批或审计。

### 错误二：为了开源而牺牲能力

如果 DSH 在关键代码任务上明显弱于 Codex / CC，不应为了开放性强行全量迁移。

### 错误三：过早抛弃商业 executor

Dossier App 的价值是中立编排。第一阶段应保留 Codex / CC adapter，用 DSH 增加自主可控选项。

### 错误四：让 DSH 内部对象进入 Dossier 状态

Dossier 状态应继续使用：

```text
Markdown
git
card
queue
report
artifact path
```

不要依赖 DSH 内部 thread id / agent id 作为长期真相。

### 错误五：忽视 Windows

Dossier 当前已经在 Windows 上遇到 Python 版本、bash alias、CRLF 等现实问题。DSH 若作为底座，必须有 Windows 支持矩阵。

## 13. 最终建议

当前倾向可以表述为：

> DSH 是 Dossier Agent App runtime 底座的优先候选，但采用方式应是 executor adapter，而不是治理内核。

推荐决策：

```text
1. 继续 Codex / autocode 三席实验，不被选型打断
2. 对 DSH 做 Phase 0 源码审计
3. 做最小 DSH executor adapter
4. 用 10 个 PoC 验收门判定
5. 通过后定位为开源 runtime 底座
6. Codex / Claude Code 保留为并行 executor
7. Dossier Core 保留模型池、角色池、治理与审计
```

一句话：

> DSH 值得作为 runtime 底座优先试，但 Dossier 的护城河不在 runtime，而在许可、角色、证据和治理。runtime 应可替换，法律不可外包。
