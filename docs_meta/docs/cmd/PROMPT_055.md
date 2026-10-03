# PROMPT_055 · 内部债一：`close_cut.py` 通用收口件

| | |
|---|---|
| **本刀是 TODO 哪一行** | `todo.md` `5.8`（本刀新立，代理席日常裁定）：收口三件固化成一件通用工具 |
| **状态** | 第 1 稿 |
| **落槌来源** | 代理席巡查 #7 自记的债（三犯 CRLF/锚错）；人 2026-10-02 授权内部线继续 |
| **前置，满足了** | 五刀收口实践在案（048–054），形状稳定可抽象 |
| **档位** | 轻——工具件，不动条文。本刀不改档位的值 |
| **谁来建造** | `builder` 写 `docs_meta/src/tools/close_cut.py`＋测试；**领班**跑格、审查（轻档机械复核）、收口（本刀自己是第一个用户：用自己的收口件结案自己——自举检验） |
| **独立审查** | 派（轻档：跑测试＋比对行为） |
| **写到哪几处** | ①新 `docs_meta/src/tools/close_cut.py`；②新 `docs_meta/tests/` 不加本（工具件不进 18 本，测试内嵌 `--selftest`）；③记录件 |

## 交什么（要点冻结）

`close_cut.py`，用法：`python docs_meta/src/tools/close_cut.py <行号> <卡号> [--review <审查页文件>] [--queue <#> <状态>]`
1. **贴审查页**：`--review` 给的文件原样字节追加到 SESSION 横线以下（自动适配 `---` CRLF/LF 形状——5.7 撞过的坑内置）；
2. **搬行**：todo 里 `- [ ] **<行号>**` 起的块搬到已办区顶（原措辞首行＋`→ cmd/PROMPT_XX.md（日期 结案）` 两行式，5.3 先例）；块尾锚自动识别下一复选框行或空行段（容忍缩进——4.8/5.5 撞过的）；
3. **queue 推进**：`--queue` 把指定 `#` 行状态改「已结」、下一未结行改「在办」；
4. **干跑模式** `--dry-run`：只打印将做的字节操作不落盘；**幂等**：重复跑同一刀报「已结，无操作」；
5. `--selftest`：合成迷你 todo/SESSION/queue 夹具，验五件事——搬行两行式形状、横线以下追加、queue 两格推进、幂等、干跑零写。

## 验收命令

| 格 | 命令 | 应当读到 |
|---|---|---|
| 1 | `python docs_meta/src/tools/close_cut.py --selftest` | `SELFTEST PASS`；退出 `0` |
| 2 | `python docs_meta/src/tools/close_cut.py 5.7 PROMPT_054 --dry-run` | 打印「已结，无操作」（5.7 已结，幂等自证） |
| 3 | `bash docs_meta/tests/run.sh` | `18 本`；`ALL PASS`；`0`（不进整盘自证） |
| 4 | `git status --porcelain` | ⊆ {close_cut.py(新), todo.md, SESSION.md, PROMPT_055.md(新), queue.md} |

## 不交什么

- 不进 `run.sh`（工具件不是检查本）；不改 workflow 条文（收口纪律本身不动，这只是它的腿）；不动已有五刀的任何落盘产物。

## 禁令

- 搬行**只搬不改**：原措辞一字不动，只加指针与日期两行；审查页**原样字节**追加，不转码不改词。

## 闸一请示

（无。内部工具件，日常裁定在案。）
