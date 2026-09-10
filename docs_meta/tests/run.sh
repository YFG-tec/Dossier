#!/usr/bin/env bash
# 母本验收入口。零权威，只作证，不算「通过」——「怎么才算错」未定，见 design/paradigm.md 第 6 节。
# 用法：bash docs_meta/tests/run.sh    工作目录随意，脚本自己回到项目根
#
# 这是 todo.md 2.5 说的「命令只保一份」的那一份（cmd/PROMPT_012.md，2026-09-10）。
# 在此之前八本检查住 .tmp/，那一层在 .gitignore 里，清一次机械保证就归零。
#
# 干三件事，按顺序：
#   1. 绊线 —— .tmp/ 下不许再有 check-*.sh。有就红，直接退出，不往下跑。
#      钉的是本刀落成的那个位置事实（检查不再住零权威层），
#      **不是「怎么才算错」**——那是第 5 章的活，本入口一个字不裁。
#      放在这里不新开第九本：添的是既有设施的一条，不是新起炉灶。
#   2. 依次跑 docs_meta/tests/check-*.sh，每本 stdout 原样透出，不加工不吞。
#   3. 汇总。全绿 ALL PASS，任一红 FAILED，exit 非零。
#
# 查不到什么：
#   - 查不到「每本自己对不对」。它们各查各的，本入口只负责把它们跑全、把红透出来。
#   - 查不到 .tmp/ 里别的东西。icon/ 和历次日志照旧住那儿（4.1 / naming.md 46 行）。
#     绊线只认 check-*.sh 这一个模式。
#   - 查不到「有没有落盘举证」。举证仍落 .tmp/，本行禁的是入口住 .tmp/，不是证据住 .tmp/。
cd "$(dirname "$0")/../.."
fail=0

echo "== 绊线：.tmp/ 下不许再有 check-*.sh =="
stray=$(find .tmp -maxdepth 1 -name 'check-*.sh' 2>/dev/null | sort)
if [ -n "$stray" ]; then
  echo "$stray" | sed 's/^/   /'
  echo "   FAIL: 上面这些还住零权威层。搬进 docs_meta/tests/，源要删干净"
  echo "         留两份就是下一个人不知道该跑哪一份——正是 2.5 要治的病"
  echo
  echo "FAILED"
  exit 1
fi
echo "   PASS: 零命中"

echo
echo "== 各本检查 =="
n=0
for f in docs_meta/tests/check-*.sh; do
  [ -e "$f" ] || continue
  n=$((n + 1))
  echo
  echo "---- $f ----"
  bash "$f"
  rc=$?
  if [ "$rc" -ne 0 ]; then fail=1; fi
  echo "---- $f 退出码 $rc ----"
done

echo
if [ "$n" -eq 0 ]; then
  echo "   FAIL: docs_meta/tests/ 下一本 check-*.sh 都没有"
  fail=1
else
  echo "   跑了 $n 本"
fi

echo
if [ "$fail" -eq 0 ]; then echo "ALL PASS"; else echo "FAILED"; fi
exit $fail
