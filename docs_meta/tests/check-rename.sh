#!/usr/bin/env bash
# 改名验收：冲刺 -> 在办。零权威，只作证，不算「通过」。
# 用法：bash docs_meta/tests/check-rename.sh    工作目录随意，脚本自己回到项目根
#
# 为什么不是「全库零命中」：grep 分不出「用」和「提」。
#   设计层要留着旧名当决议记录（§10 论证「冲刺」为什么被换掉）；
#   在办层这一刀的卡片和 TODO 那一行也必然写着旧名。
# 所以查的是产品面必须干净。
#
# 第 3、4 条指针改向（2026-09-21，`cmd/PROMPT_034.md` 第 7 步）。原来钉在那份已弃的 SVG 蓝本上，
# 现在改指 make_frame.py。断言不松，只换钉在哪份文件上。
# 第 4 条换尺（2026-09-24，6.11，`cmd/PROMPT_041.md` 闸一裁 A）：从 `-nt` 比 mtime 换成比 git 内容戳（dossier-frame.render-stamp）。理由两条：mtime 不进 git（36 桌反馈 #2，新 clone 必红）；裸字节哈希也不跟 git 旅行（core.autocrlf 的 EOL 归一化，本刀施工实测）。尺子取 `git hash-object`，检查端零 python 依赖——新桌必有 git。
#
# 第 2 条退役（2026-09-11，`cmd/PROMPT_013.md` 第 10 件）。原来查的是：
#   `paradigm.md` 里的旧名必须全部落在 §10 之内，§10 之前一处都不许有。
#   **退役理由**：那一刀把 `design/` 从红绿判定里剥出去，`paradigm.md` 整份降成思路层。
#   在思路层的文件上划一条「这一行以前不许出现某个词」的机械界线，正是这一刀要废掉的用法。
#   **人 2026-09-11 落槌**「字面退役」。退役是放宽，不是收紧，不能由测试这只手自己做
#   （同 check-mark.sh A / B 两段的先例）。
#
#   **代价照写**：旧名要是漏回 `paradigm.md` §10 之前，现在没有东西会红。
#   产品面还有第 1 条守着——那才是旧名真正要紧的地方。设计层漏了只能靠人读。
#   **是少了一格，不是换了地方。**
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
echo "== 2. 退役（2026-09-11） =="
echo "   原来查：paradigm.md 里的旧名必须全落在 §10 决议记录之内。"
echo "   退役理由见脚本头。1 / 3 / 4 三条照旧。"

echo
echo "== 3. 新层名已就位（正文与出图脚本各查一处） =="
for f in docs_meta/src/directory.md docs_meta/src/figures/make_frame.py; do
  n=$(grep -c "$NEW" "$f")
  echo "   $f  ->  $n"
  if [ "$n" -lt 1 ]; then echo "   FAIL: $f 没有新层名"; fail=1; fi
done

echo
echo "== 4. 帧图脚本改了必须重渲（git 内容戳，不比 mtime——2026-09-24，6.11/反馈#2，闸一退卡裁 A） =="
source=docs_meta/src/figures/make_frame.py
stamp=docs_meta/src/figures/dossier-frame.render-stamp
if [ ! -f "$stamp" ]; then
  echo "   FAIL: 戳不在 —— 先跑 .venv/Scripts/python.exe docs_meta/src/figures/make_frame.py"; fail=1
else
  now=$(git hash-object "$source")
  want=$(tr -d '\r' < "$stamp")
  if [ "$now" = "$want" ]; then
    echo "   PASS: 脚本的 git 眼中哈希与戳一致，图出自当前版脚本"
  else
    echo "   FAIL: 脚本改过而图未重渲（现算与戳不符）——跑 .venv/Scripts/python.exe docs_meta/src/figures/make_frame.py，戳与图一起提交"; fail=1
  fi
fi

echo
if [ "$fail" -eq 0 ]; then echo "ALL PASS"; else echo "FAILED"; fi
exit $fail
