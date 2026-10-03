# PROMPT_070 · 在办锁落地——「同一时刻只一刀」从纪律变机械事实

| | |
|---|---|
| **本刀是 TODO 哪一行** | `todo.md` `5.13`（本刀新立，代理席日常裁定；`design/parallel-research.md` 二节 v0 细形） |
| **状态** | 第 1 稿 |
| **落槌来源** | 人 2026-10-02 常备令（并行三件套）＋「继续」恢复令（2026-10-03） |
| **前置，满足了** | v0 细形四规则已备；冒烟样例（4.8）是试验场；close_cut 是放锁挂点 |
| **档位** | 重（新工具件＋冒烟样例加档＋close_cut 挂点）。本刀不改档位的值 |
| **谁来建造** | `codex exec`（执行席常态第十四刀）；**领班**写卡、跑格、审查、收口 |
| **独立审查** | 派——动 src 工具族 |
| **写到哪几处** | ①新 `docs_meta/src/tools/cut_lock.py`（锁三件：取/查/放＋泄漏报告）；②`docs_meta/src/tools/close_cut.py`（末步放锁）；③`example_meta/drive_smoke.py`（加 `lock` 档）；④`example_meta/EXPECTED.md` 补 lock 断言；⑤记录件 |

## 裁定（卡上定死，照 research v0）

1. **锁文件**：`.tmp/locks/<行号>.lock`，三行 `agent=<派单对象>` / `taken=<ISO 时戳>` / `cut=<卡号>`；原子写（临时文件＋`os.replace`）。
2. **cut_lock.py 三命令**：
   - `take <行号> <卡号> <agent>`——锁在→打印「撞锁：…」退出 2（**不覆盖**）；不在→原子取锁退出 0；
   - `check <行号>`——在→打三行内容退出 0；不在→「无锁」退出 1；
   - `release <行号>`——删锁（幂等：不在也算成功）；
   - `stale [<分钟>]`——列锁龄超阈值（默认 240 分钟）的锁，泄漏报告用；退出 0/1（有泄漏 1）。
3. **四规则入 `--help` 文档串**：派单前查锁（撞锁即断点呈报）；取锁即写；收口放锁（close_cut 末步自动）；锁零权威（丢了不废刀只报警——git 才是事实）。
4. **close_cut 末步放锁**：三件收口后若 `.tmp/locks/<行号>.lock` 在场则删（打印一行「LOCK RELEASED」；不在则静默）。
5. **冒烟 lock 档**：`drive_smoke.py --scenario lock`——取锁成功→第二次取同锁→必须打印「撞锁」且冒烟判 FAIL 即 PASS（**撞锁被拦＝档通过**，退出 0）；锁残留（release 后 check 无锁）也验。
6. **EXPECTED.md 补两行**：lock 档输出含「撞锁」；release 后 `.tmp/locks/` 该行号无文件。

## 验收命令（bash 用 `D:\Tools\Git\bin\bash.exe`；python 直接用）

| 格 | 命令 | 应当读到 |
|---|---|---|
| 1 | `python docs_meta/src/tools/cut_lock.py take 9.9 099 test-agent` → 再 take 同锁 | 首次退出 `0`；第二次输出含「撞锁」退出 `2` |
| 2 | `python docs_meta/src/tools/cut_lock.py check 9.9` → `release 9.9` → `check 9.9` | 三行内容 `0`；RELEASED `0`；「无锁」`1` |
| 3 | `python docs_meta/src/tools/cut_lock.py stale 0`（刚取的锁阈值 0 分钟即泄漏形） | 列出该锁退出 `1`；清理后退出 `0` |
| 4 | `python docs_meta/src/tools/cut_lock.py --selftest` | `SELFTEST PASS`；退出 `0` |
| 5 | `python example_meta/drive_smoke.py --scenario lock` | 输出含「撞锁」；`SMOKE PASS`（撞锁被拦＝通过）；退出 `0` |
| 6 | `bash docs_meta/tests/run.sh` | `20 本`；`ALL PASS`；`0` |
| 7 | `git status --porcelain` | ⊆ {cut_lock.py(新), close_cut.py, drive_smoke.py, EXPECTED.md, todo.md, SESSION.md, PROMPT_070.md(新), queue.md} |
| 8 | `grep -c 'cmd/PROMPT_070.md' docs_meta/docs/todo.md` | `1` |

## 不交什么

- 不改 queue.md 表结构（锁住 `.tmp/` 不住表——sync 管表、锁管进程，分工已立）；不锁 subagent（v1 议）；不动 20 本口径；不做自动强拆锁（泄漏只报告，拆归人/领班判断）。

## 禁令

- 撞锁**永不覆盖**既有锁；锁内容三行固定，不加字段；`.tmp/` 零权威——锁文件不进 git。

## 闸一请示

（无。常备令在案；判据全命令形。）
