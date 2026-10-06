#!/usr/bin/env bash
# 内容戳验收：标记节元数据位、豁免声明形状、section_stamp.py 现算对账。
# 零权威，只作证，不算「通过」。
# 用法：bash docs_meta/tests/check-stamp.sh    工作目录随意，脚本自己回到项目根
#
# 谁加的：2026-10-06 由 cmd/PROMPT_082.md 新增（todo 5.19，工牌 b1 施工）。
# 取法三样（span／元数据排除／EOL）以该卡裁定 1 为正身，本本注释只指不抄。
#
# 三查：
#   A 元数据位在 —— 六文件 `（→ harness）` 行合计 17，`^本节共` 计数行合计 17。
#     红了指：标记节被增删，或节在而计数行缺位——section_stamp.py 的 span 依赖断了。
#   B 豁免声明形状 —— 含字面「按桌改写，不配戳」的行分两类：计数行邻位的是声明位，
#     在声明位的必须整行恰为该字面（邻位而形状不恰＝红）；不在邻位的是正文提及
#     （如 workflow.md 丁块那句立法文），作证列出，不红。
#     v1 零豁免：期望 0 行声明；非 0 只要求形状合法（卡裁定 3）。枚举现算，不存清单。
#   C 现算对账 —— section_stamp.py 实跑 17 行，(文件名, 节名) 集合与 grep 现算的
#     标记节集合全等；--selftest 达 SELFTEST PASS。
#
# 查不到什么，照写不吹：
#   查不到「哈希值对不对」——哈希没有第二真相，本本只对 join 与 selftest 作证；
#     宿主侧比对（戳偏移要不要重译）归 todo 5.20（卡裁定 7），本本不裁。
#   查不到「哪节该豁免」——那是人裁（卡裁定 3），本本只验已写声明的形状与摆位。
#   查不到计数行的 N 对不对——「本节共 N 条」是 6.22 续块的口径，不归本本。
cd "$(dirname "$0")/../.."
fail=0
SUF='（→ harness）'
EXEMPT='按桌改写，不配戳'
TOOL='docs_meta/src/tools/section_stamp.py'
TAB=$(printf '\t')
SIX=(docs_meta/src/claude-code.md docs_meta/src/cursor.md docs_meta/src/directory.md
     docs_meta/src/roles.md docs_meta/src/verify.md docs_meta/src/workflow.md)

echo "== A 元数据位在：标记行合计 17，计数行合计 17 =="
n_suf=0
n_cnt=0
for f in "${SIX[@]}"; do
  a=$(grep -Ec "$SUF" "$f")
  b=$(grep -Ec '^本节共' "$f")
  echo "   $f  标记 $a ／ 计数 $b"
  n_suf=$((n_suf + a))
  n_cnt=$((n_cnt + b))
done
echo "   合计：标记 $n_suf ／ 计数 $n_cnt（期望各 17）"
if [ "$n_suf" -eq 17 ] && [ "$n_cnt" -eq 17 ]; then
  echo "   PASS: 17 节与各自计数行都在"
else
  echo "   FAIL: 标记节被增删，或节在而计数行缺位——span 依赖断了"
  fail=1
fi

echo
echo "== B 豁免声明形状：声明位的「$EXEMPT」必为独立行且字面恰（v1 期望 0 行）=="
b_out=$(for f in "${SIX[@]}"; do
  awk -v ex="$EXEMPT" -v fn="$f" -v tab="$TAB" '
    { sub(/\r$/, ""); L[NR] = $0 }
    END {
      for (i = 1; i <= NR; i++) {
        if (index(L[i], ex) == 0) continue
        whole = (L[i] == ex)
        near = (i > 1 && L[i-1] ~ /^本节共/) || (i < NR && L[i+1] ~ /^本节共/)
        if (near)      print (whole ? "DECL_OK" : "DECL_BAD") tab fn tab i tab L[i]
        else           print "MENTION" tab fn tab i
      }
    }
  ' "$f"
done)
n_decl=0
n_mention=0
bad_b=0
while IFS="$TAB" read -r kind fn ln rest; do
  [ -n "$kind" ] || continue
  case "$kind" in
    DECL_OK)
      n_decl=$((n_decl + 1))
      echo "   声明  $fn:$ln 形状合法"
      ;;
    DECL_BAD)
      echo "   FAIL  $fn:$ln 在计数行邻位但不是独立整行的豁免字面：$rest"
      bad_b=1
      ;;
    MENTION)
      n_mention=$((n_mention + 1))
      echo "   提及  $fn:$ln 正文提及，不算声明行（如丁块立法句），作证不红"
      ;;
  esac
done <<EOF
$b_out
EOF
echo "   豁免声明 $n_decl 行（v1 期望 0，非 0 只要求形状合法）；正文提及 $n_mention 行"
if [ "$bad_b" -eq 0 ]; then
  echo "   PASS: 声明位上没有形状不合法的豁免行"
else
  echo "   FAIL: 声明只能长成整行「$EXEMPT」，改字请走卡——那是声明形状唯一的意思"
  fail=1
fi

echo
echo "== C section_stamp.py 现算对账：17 行 TSV；节名集合与 grep 现算全等；selftest 绿 =="
if python "$TOOL" --selftest | tr -d '\r' | grep -q '^SELFTEST PASS$'; then
  echo "   PASS: --selftest 达 SELFTEST PASS"
else
  echo "   FAIL: --selftest 未达 SELFTEST PASS"
  fail=1
fi
tsv=$(python "$TOOL")
n_tsv=$(printf '%s' "$tsv" | tr -d '\r' | grep -c .)
if [ "$n_tsv" -eq 17 ]; then
  echo "   PASS: 实跑 $n_tsv 行 TSV"
else
  echo "   FAIL: 实跑 $n_tsv 行（期望 17）"
  fail=1
fi
gset=$(for f in "${SIX[@]}"; do
  b=$(basename "$f")
  grep -E "^## .*$SUF" "$f" | tr -d '\r' \
    | sed -e 's/^## //' -e "s/$SUF\$//" | sed "s/^/${b}${TAB}/"
done | sort)
tset=$(printf '%s' "$tsv" | tr -d '\r' | awk -F'\t' '{ print $1 "\t" $2 }' | sort)
if [ "$gset" = "$tset" ]; then
  echo "   PASS: (文件, 节名) 集合与 grep 现算全等（$n_tsv/$n_tsv）"
else
  echo "   FAIL: 集合不全等——左 grep 现算，右工具实跑："
  diff <(printf '%s\n' "$gset") <(printf '%s\n' "$tset") | sed 's/^/     /'
  fail=1
fi

echo
if [ "$fail" -eq 0 ]; then echo "ALL PASS"; else echo "FAILED"; fi
exit "$fail"
