#!/usr/bin/env bash
# cmd/ 定位验收：它是在办层唯一只增不删的历史。零权威，只作证，不算「通过」。
# 用法：bash docs_meta/tests/check-cmd.sh
#
# 这三条查的是**词的共现，不是意思**。能抓「cmd 和覆盖出现在同一行而没说清区别」，
# 抓不到「整段读下来仍然把 cmd 说成会被覆盖」。边界写在这里，别拿它当把关层。
#
# A 段的扫描名单 2026-09-11 去掉了 `paradigm.md`（`cmd/PROMPT_013.md` 第 11 件）：
#   那一刀把 `design/` 从红绿判定里剥出去，不在思路层的文件上做机械断言。
#   **人 2026-09-11 落槌**「字面退役」。减扫描目标是放宽，不由测试这只手自己做。
#   **代价照写**：`paradigm.md` 里以后写出含混的行不会红。去掉它的那一刻盘上命中 0 处，
#   所以这一减没有掩盖任何现存问题；但往后漏了就只能靠人读。
cd "$(dirname "$0")/../.."
fail=0
SRC="docs_meta/src/directory.md docs_meta/src/workflow.md \
     docs_meta/src/roles.md docs_meta/src/cursor.md"

echo "== A lint：一行里既提 cmd/PROMPT 又提「覆盖」，就必须说清 cmd 不被覆盖 =="
echo "   （放行条件：同一行还出现「只增」或「新增」）"
bad=$(grep -nE 'cmd|PROMPT' $SRC | grep $'覆盖' | grep -v $'只增' | grep -v $'新增')
if [ -n "$bad" ]; then
  echo "$bad"
  echo "   FAIL: 上面这些行把 cmd 和「覆盖」摆在一起，没区分"
  fail=1
else
  echo "   PASS: 没有含混的行"
fi

echo
echo "== B directory.md 六块表「在办」那一行须写全三种寿命 =="
row=$(grep -n '^| 在办 |' docs_meta/src/directory.md)
echo "   $row"
if echo "$row" | grep -q $'只增' && echo "$row" | grep -q $'覆盖'; then
  echo "   PASS: 「只增」和「覆盖」都在"
else
  echo "   FAIL: 寿命栏没写全（须同时出现「只增」和「覆盖」）"
  fail=1
fi

echo
echo "== C 三份主文档里「只增不删」各至少一次 =="
for f in docs_meta/src/directory.md docs_meta/src/workflow.md docs_meta/src/roles.md; do
  n=$(grep -c $'只增不删' "$f")
  echo "   $f  ->  $n"
  if [ "$n" -lt 1 ]; then echo "   FAIL: $f 没写"; fail=1; fi
done

echo
if [ "$fail" -eq 0 ]; then echo "ALL PASS"; else echo "FAILED"; fi
exit $fail
