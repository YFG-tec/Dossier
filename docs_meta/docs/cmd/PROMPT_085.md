# PROMPT_085 · 5.25 6.20 四格补齐——判据与证据各归其格

| | |
|---|---|
| **本刀是 TODO 哪一行** | `todo.md` `5.25`：6.20 四格补齐：卡面「本刀之外的改动」声明行、只读外部树判据、子模块指针句、`.tmp/` 证据升格去处（反馈建议 15） |
| **状态** | 第 1 稿 |
| **落槌来源** | 队列 #42（硬化批授权）；反馈建议 15（四格全无锚，处置节裁：立行） |
| **前置，满足了** | `design/hardening.md` §五 6.20 条目亲读；四落点现状亲读（卡模板表 :258–268、git 状态节 :403–410、naming 两堆表 :84–92、directory 草稿行 :35）；section_stamp 现算——四个落点均不在 17 标记节内，无计数连带 |
| **档位** | 重——动条文（workflow/naming/directory 三件）。本刀不改档位的值 |
| **谁来建造** | subagent builder（工牌 b1） |
| **独立审查** | 派两只并行手（表面／语义） |
| **写到哪几处** | ①`docs_meta/src/workflow.md`（卡模板一行＋git 判据节一条）；②`docs_meta/src/naming.md`（指针句）；③`docs_meta/src/directory.md`（草稿行升格去处）；④记录件 |

## 裁定（卡上定死）

1. **卡模板补一行**（workflow.md「卡片最低字段」表内、「不交什么」行之后、「禁令」行之前），行文逐字：
   `| **本刀之外的改动** | 开工声明一次；验收整段排除——格面 ⊆ 声明行 ∪ 卡内路径 |`
2. **只读外部树判据一条**（workflow.md「git 状态作判据」节内、「判据锚内容哈希」bullet 之后、「本节不改谁按 commit」bullet 之前），行文逐字：
   `- **只读外部树不进判据。** 对照材料、子模块上游、任何本刀只读的树——判据不许依赖它的 sha，也不许依赖它的工作区干净；它随时被上游或人动，锚它＝替别人守红绿（反馈建议 15）。`
3. **子模块指针句**（naming.md「留在子模块里／init 铺到宿主上」两堆表之后、「\`docs/\` 是运行时的数据布局」段之前，独立一段），行文逐字：
   `子模块指针跟上游：本地不改母本文件；宿主提交前重新暂存指针（\`git add <子模块路径>\`）——指针漂着不暂存，等于宿主对母本的私改悬在账外（反馈建议 15）。`
4. **`.tmp/` 证据升格去处**（directory.md 寿命表「草稿」行，行内追加句），在现行「……收口即焚（证据摘录进审查页后整目录删）」之后追加，追加句逐字：
   `；被验收格点名引用过的证据不许只留 \`.tmp/\`——收口前升格进 \`docs/reports/\`（宿主形状；母本现址 \`docs_meta/docs/reports/\`）随刀 commit，摘录进审查页的既有做法保留`
5. **记录件**：`todo.md` `5.25` 行挂本卡指针；`SESSION.md` 覆盖；`queue.md` #42 状态列。

## 验收命令（bash 用 Git Bash）

| 格 | 命令 | 应当读到 |
|---|---|---|
| 1 | `bash docs_meta/tests/run.sh` | `21 本`；无 FAIL |
| 2 | `rg -n '本刀之外的改动' docs_meta/src/workflow.md` | 恰 1（模板行） |
| 3 | `rg -n '只读外部树' docs_meta/src/workflow.md` | ≥1（判据条） |
| 4 | `rg -n '子模块指针' docs_meta/src/naming.md` | ≥1 |
| 5 | `rg -n '升格' docs_meta/src/directory.md` | ≥1（草稿行） |
| 6 | `bash docs_meta/tests/check-done.sh` | ALL PASS；PROMPT_085 恰 1 |
| 7 | `git status --porcelain` | ⊆ {workflow.md, naming.md, directory.md, todo.md, SESSION.md, queue.md, PROMPT_085.md(新)} |

## 不交什么

- 不动 17 标记节任何 span 内文（四落点均不在标记节内，section_stamp 现算在案）；不动任何检查本；不动 `.mirror/` 与根 harness 件；不动权限表（5.24 刚落的那行不碰）；不改既有计数行的 N（本刀无计数连带）。

## 禁令

- 四处行文逐字照裁定，不润色不加段；「只读外部树」条不改变谁按 commit 的授权（那是节内既有末条管的）。

## 闸一请示

（无。行判据在行内；四格都是把既有口径落成格子，不松判据、不添授权。）
