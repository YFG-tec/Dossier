#!/usr/bin/env bash
# 改名验收：冲刺 -> 在办。零权威，只作证，不算「通过」。
# 用法：bash docs_meta/tests/check-rename.sh    工作目录随意，脚本自己回到项目根
#
# 为什么不是「全库零命中」：grep 分不出「用」和「提」。
#   合同层要留着旧名当决议记录（§10 论证「冲刺」为什么被换掉）；
#   在办层这一刀的卡片和 TODO 那一行也必然写着旧名。
# 所以查两件事：产品面必须干净；合同层的旧名必须全在 §10 里面。
cd "$(dirname "$0")/../.."
fail=0
OLD=$'冲刺'   # 冲刺
NEW=$'在办'   # 在办

echo "== 1. 产品面（readme + docs_meta/src/）不许再有旧层名 =="
if grep -rn "$OLD" readme.md docs_meta/src/ ; then
  echo "   FAIL: 上面这些还是旧名"
  fail=1
else
  echo "   PASS: 零命中"
fi

echo
echo "== 2. 合同层的旧名必须全部落在 §10（决议记录）之内 =="
P=docs_meta/docs/design/paradigm.md
sec=$(grep -n '^## 10 ' "$P" | cut -d: -f1)
early=$(grep -n "$OLD" "$P" | awk -F: -v s="$sec" '$1 < s')
if [ -n "$early" ]; then
  echo "$early"
  echo "   FAIL: §10 之前还有在用的旧名（第 $sec 行起才是决议记录）"
  fail=1
else
  echo "   PASS: §10（第 $sec 行）之前零命中"
fi

echo
echo "== 3. 新层名已就位（正文与图各查一处） =="
for f in docs_meta/src/directory.md docs_meta/src/figures/dossier-frame.svg; do
  n=$(grep -c "$NEW" "$f")
  echo "   $f  ->  $n"
  if [ "$n" -lt 1 ]; then echo "   FAIL: $f 没有新层名"; fail=1; fi
done

echo
echo "== 4. PNG 不比 SVG 旧（改了图必须重渲并回拷） =="
svg=docs_meta/src/figures/dossier-frame.svg
png=docs_meta/src/figures/dossier-frame.png
if [ "$png" -nt "$svg" ]; then
  echo "   PASS: PNG 新于 SVG"
else
  echo "   FAIL: PNG 旧于或同龄于 SVG —— 跑 .tmp/icon/frame.sh 再把 frame@2x.png 回拷"
  fail=1
fi

echo
if [ "$fail" -eq 0 ]; then echo "ALL PASS"; else echo "FAILED"; fi
exit $fail
