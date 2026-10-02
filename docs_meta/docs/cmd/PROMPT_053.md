# PROMPT_053 · 4.8 冒烟样例——十步驱动器与机器判定

| | |
|---|---|
| **本刀是 TODO 哪一行** | `todo.md` `4.8`：`example_meta/` 里做一份跑得通全流程的冒烟样例（行内判据 2026-09-24 已死） |
| **状态** | 第 1 稿 |
| **落槌来源** | 人 2026-10-02 序列授权＋日常裁定（`queue.md` 头） |
| **前置，满足了** | 零件半齐：`init_add_task.py`（干净起点）、`human_fake/`（dumb/reason）在库；缺驱动器与判定器——本刀主体 |
| **档位** | 重（动 `src/` 族——example_meta 是产品样例层）。本刀不改档位的值 |
| **谁来建造** | `builder` 写两件新文件＋改一件；**领班**跑格、派审查、收口。**假人档 dumb（零模型）跑主线；reason 档的轻模型派单另测一格** |
| **独立审查** | 派——产品层新增两件可执行件 |
| **写到哪几处** | ①新 `example_meta/drive_smoke.py`（十步驱动器）；②新 `example_meta/EXPECTED.md`（期望终态）；③改 `example_meta/README.md`（入口说明）；④记录件 |

## 现状（builder 会踩的）

1. **十步**（行内原文）：立项、点行、写卡、停、审卡、闸一红印、改核、红转绿、验收、结案。其中「停」是要点——写完卡直接往下改核就是跳过了唯一一条真规矩，驱动器必须在此步断言停下等假人发令。
2. **两条都要跑**：白名单那条（全程走通）；**禁令那条才是本体**——让 builder 在 1.2 之前先写 `src/plus.py`（无卡改核），驱动器必须判 FAIL。
3. **每趟从干净起点开始**：驱动器首步调 `init_add_task.py` 复原；跑完可重置（同一条命令）。
4. **判定由机器做**：驱动器比对 `EXPECTED.md` 声明的终态断言（todo 勾选、已办内容、SESSION 状态、src/tests 在场、退出码），不合退非零；日志落 `add_task/.tmp/`（样例夹内零权威层）。**人不参与比对**。
5. **假人 v1 只会通过**（dumb 硬编码），是槽位不是责任人；收紧仍归 contract-tester（样例内即红测步）。
6. **两处明写缺口**：审卡步无第二会话（驱动器内以「读卡＋固定检查单」代形，README 标注与真流程的差异）；`add_task/` 生成物不入库（.gitignore 已有）。
7. 驱动器本身不进 `docs_meta/tests/run.sh`（行内原文：进去了每刀验收都被绑上几分钟的拉代理跑流程）。

## 交什么（要点冻结；实现细节 builder 定，Expected 断言逐条列）

`drive_smoke.py`：`python example_meta/drive_smoke.py [--scenario ok|ban]`，退出码 0/1。
- `ok` 档：十步顺序走。每步一个函数，步前打印步名；第 4 步「停」处断言：盘上无 `src/plus.py`（写卡后不许改核），假人发令后才继续；第 7 步写入 `add`；第 8 步跑 `pytest`（红转绿断言：先确认 1.2 的红测真的红过——落地为「1.2 步后记录 pytest 退出码非零」）；第 10 步假人 `判断：是` 后勾行搬已办。终态逐条比对 `EXPECTED.md`。
- `ban` 档：走到写卡后，直接让 builder 写 `src/plus.py`，驱动器在下一检查点判 FAIL（无卡改核未被拦截即样例失败），退非零。
- 全程日志追加 `add_task/.tmp/smoke.log`；判定输出「SMOKE PASS/FAIL: <原因>」单行结论。

`EXPECTED.md`：ok 档终态断言清单（todo 四行全勾进已办带日期占位、SESSION 状态「已结案」、`src/plus.py` 含 `def add`、`tests/test_plus.py` 在场、`.tmp` 有红过一次的记录）。

`README.md` 增改：一条命令入口（`python drive_smoke.py` 默认两档连跑）、两处缺口说明、不进 run.sh 的原因（引行内原文）。

## 验收命令（bash 用 `D:\Tools\Git\bin\bash.exe`；python 直接用）

| 格 | 命令 | 应当读到 |
|---|---|---|
| 1 | `python example_meta/drive_smoke.py --scenario ok; echo $?` | 末行 `SMOKE PASS`; 退出码 `0` |
| 2 | `python example_meta/drive_smoke.py --scenario ban; echo $?` | 末行 `SMOKE FAIL: ...无卡改核...`; 退出码非 `0` |
| 3 | 连跑两遍 ok 档 | 两遍都 `SMOKE PASS`（可重置验证） |
| 4 | `python example_meta/init_add_task.py` 后 `Test-Path example_meta/add_task/src/plus.py` | `False`（干净起点） |
| 5 | `bash docs_meta/tests/run.sh` | `18 本`；`ALL PASS`；`0`（驱动器不进整盘） |
| 6 | `git status --porcelain` | ⊆ {drive_smoke.py(新), EXPECTED.md(新), README.md, todo.md, SESSION.md, PROMPT_053.md(新)} |
| 7 | `grep -c 'cmd/PROMPT_053.md' docs_meta/docs/todo.md` | `1` |

## 不交什么

- 不改 `init_add_task.py` 与 `human_fake/`（零件已合格）；不动 `docs_meta/`；不给假人加判断力（v1 只会通过，行内原文）。
- 不做低阶模型假人（行内「另立一行」）；不裁「这算不算真的测」（5.1 已作废，实践已答）。

## 禁令

- 禁令档（格 2）是本体，不得只交白名单档；两档都在卡上，缺一即 FAIL。
- 判定不得请人读；「人不参与比对」是行内原文。
- 不 commit、不 push。

## 闸一请示

（无。判据全在行内；日常裁定授权在案。）
