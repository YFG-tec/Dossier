# PROMPT_101 · 5.45 postman 远端 scheme 补 SSH 两形——正式测试红的第一把修刀

| | |
|---|---|
| **本刀是 TODO 哪一行** | `todo.md` `5.45`（人 2026-10-10「1.开101刀小修」；红读数在行内） |
| **状态** | 第 1 稿（人点火即裁：微修刀，红即修） |
| **落槌来源** | 5.44 期后正式测试（卡裁定 5：红则另立修刀）：seed 已上 Codeup，init --with-mail 对 scp 形与 ssh:// 形均 exit 8 |
| **前置，满足了** | `postman.py` scheme 校验段亲读；正式测试两探针读数在 `.tmp`（probe/probe2）；seed 远程在案 |
| **档位** | 重（动 `src/` 工具）。本刀不改档位的值 |
| **谁来建造** | 独立 subagent（工牌制） |
| **独立审查** | 事实与结构手第一顺位；实战手第二顺位＝**正式测试续跑**（真 Codeup SSH 全周期） |
| **写到哪几处** | ①`docs_meta/src/postman.py` ②记录件 |

## 裁定（卡上定死）

1. **白名单扩四形**：`file://`、`https://`、`ssh://`、scp 形 `git@host:path`；**无 scheme 裸路径继续拒**（当初拦住错误形的闸不许拆）。
2. **三钉远端归属校验同步**：配置 URL 与实参归一化（四形同权）后比对——push 只进邮局仓这堵墙在 SSH 形下同样成立。
3. **selftest 加判表用例**：四形收、裸路径拒；file:// 全周期不回归。
4. **正式测试续跑＝实战审查**：真 Codeup SSH 挂载＋双桌（33-dossier↔echo-test）互寄一轮，读数追加 SESSION——这是本刀的格 3。
5. **不越界**：不动 init.py（透传即可）、不动条文、不动 22 本口径。

## 验收命令（日志树外）

| 格 | 命令 | 应当读到 |
|---|---|---|
| 1 | `bash docs_meta/tests/run.sh`（树外日志） | 22 本；ALL PASS（结案时） |
| 2 | `python -X utf8 docs_meta/src/postman.py selftest` | 判表绿＋file:// 全周期不回归 |
| 3 | 真 Codeup：`init.py --with-mail git@codeup.aliyun.com:fiatlux/Lab/Mail_dossier.git --desk <桌>` | 挂载过；双桌互寄全周期绿（读数追加 SESSION） |
| 4 | `git status --porcelain` | ⊆ {postman.py＋记录件} |

## 不交什么

- 不动 init.py／条文／22 本；不重铺 seed（远程已有）。

## 禁令

- 裸路径仍拒（闸不拆）；三钉墙四形同权；探针树外；新句循画风。

## 闸一请示

（无。人「1.开101刀小修」即点火；修法即红读数的对症。）
