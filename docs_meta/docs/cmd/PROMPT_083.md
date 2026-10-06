# PROMPT_083 · 5.20 宿主无关层清单＋会话起步闸——宪法要能发现警察没上班

| | |
|---|---|
| **本刀是 TODO 哪一行** | `todo.md` `5.20`：宿主无关层清单＋会话起步闸（架构执行自检开工即红，量程跟档位） |
| **状态** | 第 1 稿 |
| **落槌来源** | 队列 #40（硬化批授权）；反馈建议 4（后补九换宿主静默失效为标本）；侦察在案（run a695b498） |
| **前置，满足了** | check-env 四段现状在案（架构执行零检查）；.mirror 16 文件与宿主对账表在案 |
| **档位** | 重——动条文＋检查本＋init。本刀不改档位的值 |
| **谁来建造** | subagent builder（工牌 b1；混合件，codex 不派） |
| **独立审查** | 派三只并行手 |
| **写到哪几处** | ①`tests/check-env.sh`（新 E 段）；②`src/directory.md`（宿主无关层清单小表）；③根 `CLAUDE.md`＋`.mirror/CLAUDE.md`（起步闸句，双落同步）；④`src/workflow.md`（全程图 ⓪/① 间一句）；⑤`src/init.py`（structure 铺 `docs/SETUP.md`）＋`.mirror/` 无新件；⑥记录件 |

## 裁定（卡上定死）

1. **check-env 新 E 段（架构执行，量程跟档位）**：查宿主根「执行架构在场性」——`.claude/agents/`（四件）、`.claude/skills/`（三件）、`.cursor/rules/switches.mdc`。三档：**全无 → WARN**（轻档无架构，起步闸不适用）；**部分在场（有 agents 无 skills、或缺 switches 而桌有 .cursor/）→ FAIL**（半身不遂，开工即红——这是后补九的病灶形状）；**配对齐 → PASS**（在场性 v1；「生效性」深检留待 hooks 等实件出现，条文照写）。既有 A–D 段零改动。
2. **宿主无关层清单落 `directory.md`**（工具配置层定义处 :139 附近，小表六行）：进 mirror 的（agents 四/skills 三/.codex 四/switches/settings）＋**宿主私有、换宿主即丢**的（`host.md`、`settings.local.json`、text-to-image 命令与 skill——刀外件在案）＋**尚无实件的**（hooks——「出现时必须入 mirror」）。表头一句：「执行架构类设置不得只存宿主特有文件——换宿主等于静默丢配置（后补九标本）」。这是立场声明不是覆盖表，缺口由 check-mirror 现算。
3. **起步闸句双落**：根 `CLAUDE.md` 与 `.mirror/CLAUDE.md`（先读顺序段头、同措辞）：「**会话起步闸**：本桌执行架构在场时，第一段先跑 `check-env` 的 E 段——半身不遂即红，不准静默跑；全无（轻档）则明记不适用。量程跟档位走：桌用什么，验什么。」
4. **workflow 全程图 ⓪/① 之间**加一句摘要＋指针（照「全程图那格只写一句」的自家规矩）：「⓪½ 起步闸：执行架构在场则 check-env E 段绿才开（正身住 CLAUDE.md 起步闸句）」。
5. **装桌检查单载体（6.22 分解件）**：`init.py` 的 `structure` 列表加 `docs/SETUP.md`——短检查单（submodule update → init → 起步闸 E 段 → 首刀红绿自检 → 基线回执见后续刀）；workflow 开桌一次性那行（:449 附近）加半句指针「装桌清单见 `docs/SETUP.md`（init 铺出）」。
6. **再分解两件（不在本刀）**：宿主侧基线种子＋比对脚本 → 立行 5.30（5.19 分解件，动 init 铺后逻辑独立验收）；`.claude/settings.json` 会话漂移治理 → 记 hardening 追记候选（与 5.11 守卫同族）。

## 验收命令（bash 用 Git Bash）

| 格 | 命令 | 应当读到 |
|---|---|---|
| 1 | `bash docs_meta/tests/run.sh` | `21 本`；无 FAIL |
| 2 | `bash docs_meta/tests/check-env.sh` | ALL PASS（本机 E 段应 PASS：agents/skills 在场配对） |
| 3 | `rg -n '起步闸' CLAUDE.md .mirror/CLAUDE.md docs_meta/src/workflow.md` | 三处各恰 1 |
| 4 | `rg -n '宿主无关' docs_meta/src/directory.md` | ≥1（清单表头句） |
| 5 | `rg -n 'SETUP' docs_meta/src/init.py` | ≥1（structure 行） |
| 6 | `bash docs_meta/tests/check-done.sh` | ALL PASS；PROMPT_083 恰 1 |
| 7 | `git status --porcelain` | ⊆ {check-env.sh, directory.md, workflow.md, CLAUDE.md, .mirror/CLAUDE.md, init.py, todo.md, SESSION.md, PROMPT_083.md(新), queue.md} |

## 不交什么

- 不动 check-env A–D 段一字；不动权限表（5.24 的活）；不写基线种子/比对脚本（5.30）；不治理 settings 漂移；`.mirror/` 只动 CLAUDE.md 一件；不动 17 节任何 span。

## 禁令

- E 段只查「在场性配对」，不发明「生效性」深检（无实件可查的东西不许写死）；WARN/FAIL 两档语义不得混。
- 起步闸句两处措辞逐字一致（mirror 与根锁漂移即假红）。

## 闸一请示

（无。行判据在行内；本刀是给换宿主静默失效装报警器，不松任何判据；两分解件已立行/记档。）
