# EXPECTED · ok 档终态断言清单

`drive_smoke.py` 第 9 步逐条比对本页。**判定由机器做，人不参与比对**（todo 4.8 行内原文）。

- src 有 def add：`add_task/src/plus.py` 内含 `def add(a, b)`
- tests 在场：`add_task/tests/test_plus.py` 存在
- red-once 在档：`add_task/.tmp/red-once.md` 存在（1.2 红测真的红过一次）
- todo 四行全勾：`docs/todo.md` 待办区无 `- [ ] **1.` 残行
- 已办带指针：四条已办行各含 `cmd/PROMPT_0001.md` 与结案日期
- SESSION 已结案：`docs/SESSION.md` 状态格为「已结案」
- lock 档输出含撞锁：第二次 take 输出「撞锁」且退出 2（撞锁被拦＝档通过）
- release 后该行号无锁文件：`.tmp/locks/1.1.lock` 不在场
