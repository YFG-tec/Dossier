#!/usr/bin/env bash
# check-sync.sh —— 状态一致性对账（cmd/PROMPT_059.md，todo 5.10）
# 用法：bash docs_meta/tests/check-sync.sh
#
# 四段口径：
#   A 有刀态判定 —— 只看 SESSION.md 横线以上：取「点的行」格首个 X.Y 行号
#     （沿用 check-verdict 的行号形状，容字母尾），并取唯一 cmd/PROMPT_NNN 卡号。
#     两者取不齐就是刀间歇：四段跳过，退出 0（空场不假红）。
#   B SESSION↔todo —— 行未勾时，SESSION 状态格不得含结案字样；
#     行已勾时，todo「已办」区必须有本卡指针，且 SESSION 状态格必须含结案态。
#   C SESSION↔queue —— 找 queue 表内行号（或 todo 行文字）所在行：
#     已结要求 SESSION 含结案态；在办要求 queue 卡号与 SESSION 卡号一致；
#     挂起/断点/排队而 SESSION 正指着它，则红。
#   D queue 单在办 —— 全表「在办」行数 ≤1，多于一处就点名。
#
# 根目录开关：SYNC_ROOT 指向夹具树时，三份运行件都从那棵树读；
#   形状照 check-link.sh 的 LINK_ROOT。本本只红不修，修复归 close_cut 与人。
set -u
cd "$(dirname "$0")/../.."

fail=0
ROOT="${SYNC_ROOT:-}"
ROOT="${ROOT%/}"
S="${ROOT:+$ROOT/}docs_meta/docs/SESSION.md"
TODO="${ROOT:+$ROOT/}docs_meta/docs/todo.md"
QUEUE="${ROOT:+$ROOT/}docs_meta/docs/queue.md"

for f in "$S" "$TODO" "$QUEUE"; do
  [ -f "$f" ] || { echo "FAIL: $f 不存在"; exit 1; }
done

TOP=$(mktemp)
QHITS=$(mktemp)
ONGOING=$(mktemp)
trap 'rm -f "$TOP" "$QHITS" "$ONGOING"' EXIT

# SESSION 只取横线以上；没有横线就是全页（老格式）。
if grep -qn '^---$' "$S"; then
  awk '/^---$/{exit} {print}' "$S" > "$TOP"
else
  cp "$S" "$TOP"
fi

STATUS_TEXT=$(
  awk -F'|' '
    $2 ~ /^[[:space:]]*\*\*状态\*\*[[:space:]]*$/ {
      s=$3; gsub(/\*\*/, "", s); gsub(/^[[:space:]]+|[[:space:]]+$/, "", s); print s; exit
    }
  ' "$TOP"
)
case "$STATUS_TEXT" in
  *已结*|*结案*) SESSION_CLOSED=1 ;;
  *) SESSION_CLOSED=0 ;;
esac

echo "== A 有刀态判定 =="
ROW=$(grep -F '| **点的行** |' "$TOP" | grep -oE '[0-9]+\.[0-9]+[a-z]*' | head -n 1)
CARD_PTR_LIST=$(grep -oE 'cmd/PROMPT_[0-9]{3,}\.md' "$TOP" | sort -u)
NCARD=$(printf '%s\n' "$CARD_PTR_LIST" | grep -c .)
if [ -z "$ROW" ] || [ "$NCARD" -ne 1 ]; then
  echo "   刀间歇，四段跳过"
  exit 0
fi
CARD_PTR=$(printf '%s\n' "$CARD_PTR_LIST" | head -n 1)
CARD=${CARD_PTR#cmd/PROMPT_}
CARD=${CARD%.md}
ROW_ESC=$(printf '%s\n' "$ROW" | sed 's/\./\\./g')
echo "   PASS: 本刀 row=$ROW card=$CARD"

# B 段先抓 todo 行；C 段的“或其文字”也用它做备用匹配。
TODO_ROWS=$(grep -E "^- \[[ xX]\] \*\*$ROW_ESC\*\*" "$TODO")
TODO_ROW=$(printf '%s\n' "$TODO_ROWS" | head -n 1)
TODO_N=$(printf '%s\n' "$TODO_ROWS" | grep -c .)

echo
echo "== B SESSION↔todo =="
if [ -z "$TODO_ROW" ]; then
  echo "   FAIL: todo.md 找不到行 $ROW"
  fail=1
elif [ "$TODO_N" -ne 1 ]; then
  echo "   FAIL: todo.md 行 $ROW 有 $TODO 条，口径不唯一"
  printf '   %s\n' "$TODO_ROWS"
  fail=1
else
  DONE_PTR=$(awk -v p="$CARD_PTR" '/^## 已办$/{seen=1} seen && index($0,p){print; found=1} END{exit !found}' "$TODO")
  case "$TODO_ROW" in
    '- [ ]'*)
      if [ "$SESSION_CLOSED" -eq 1 ]; then
        echo "   FAIL: todo 行 $ROW 未勾，SESSION 状态却含结案字样：$STATUS_TEXT"
        fail=1
      else
        echo "   PASS: 未勾行没有结案态"
      fi
      ;;
    '- [x]'*|'- [X]'*)
      B_BAD=0
      [ -n "$DONE_PTR" ] || { echo "   FAIL: todo 行 $ROW 已勾，已办区没有 $CARD_PTR"; B_BAD=1; }
      [ "$SESSION_CLOSED" -eq 1 ] || { echo "   FAIL: todo 行 $ROW 已勾，SESSION 状态缺结案态：$STATUS_TEXT"; B_BAD=1; }
      if [ "$B_BAD" -eq 0 ]; then echo "   PASS: 已勾行、已办指针、结案态三面齐"; fi
      [ "$B_BAD" -eq 0 ] || fail=1
      ;;
  esac
fi

# queue 只认表行：| # | 行 | 卡 | 状态 | 断点 |。
# 输出：物理行号、#、行格、卡格、状态格（去空白与粗体）。
awk -F'|' '
  function clean(s) {
    gsub(/^[[:space:]]+|[[:space:]]+$/, "", s)
    gsub(/\*\*/, "", s)
    return s
  }
  $2 ~ /^[[:space:]]*[0-9]+[[:space:]]*$/ && NF >= 6 {
    printf "%s\t%s\t%s\t%s\t%s\t%s\n", NR, clean($2), clean($3), clean($4), clean($5), $0
  }
' "$QUEUE" > "$QHITS"

# 从 todo 行提一个短标题，供 queue 行格只写文字、不写行号时兜底。
TODO_LABEL=""
if [ -n "$TODO_ROW" ]; then
  TODO_LABEL=$(printf '%s\n' "$TODO_ROW" |
    sed -E "s/^- \[[ xX]\] \*\*$ROW_ESC\*\*[[:space:]]*//" |
    sed 's/`//g; s/ →.*//; s/[：:，,（(———].*//; s/^[[:space:]]*//; s/[[:space:]]*$//')
fi

echo
echo "== C SESSION↔queue =="
CMATCH=0
C_FAIL=0
while IFS=$'\t' read -r QLINE_NO QN QROW QCARD QSTATUS QLINE; do
  ROW_HIT=0
  for token in $(printf '%s\n' "$QROW" | grep -oE '[0-9]+\.[0-9]+[a-z]*'); do
    [ "$token" = "$ROW" ] && ROW_HIT=1
  done
  if [ "$ROW_HIT" -eq 0 ] && [ -n "$TODO_LABEL" ]; then
    case "$QROW" in *"$TODO_LABEL"*) ROW_HIT=1 ;; esac
  fi
  [ "$ROW_HIT" -eq 1 ] || continue
  CMATCH=$((CMATCH + 1))
  QCARD_NUM=$(printf '%s\n' "$QCARD" | grep -oE 'PROMPT_[0-9]{3,}' | sed 's/^PROMPT_//' | head -n 1)
  case "$QSTATUS" in
    *已结*|*结案*)
      if [ "$SESSION_CLOSED" -eq 1 ]; then
        echo "   PASS: queue #$QN 已结，SESSION 有结案态"
      else
        echo "   FAIL: queue #$QN 已结，SESSION 状态缺结案态：$STATUS_TEXT"
        C_FAIL=1
      fi
      ;;
    *在办*)
      if [ "$QCARD_NUM" = "$CARD" ]; then
        echo "   PASS: queue #$QN 在办，卡号=$CARD"
      else
        echo "   FAIL: queue #$QN 在办，卡号格是「${QCARD:-空}」，SESSION 卡号是 $CARD"
        C_FAIL=1
      fi
      ;;
    *挂起*|*断点*|*排队*)
      echo "   FAIL: queue #$QN 是「$QSTATUS」，但 SESSION 正指着行 $ROW（挂着却占着 SESSION）"
      C_FAIL=1
      ;;
    *)
      echo "   FAIL: queue #$QN 状态「$QSTATUS」不在已结/在办/挂起/断点/排队口径内"
      C_FAIL=1
      ;;
  esac
done < "$QHITS"
if [ "$CMATCH" -eq 0 ]; then
  echo "   FAIL: queue.md 找不到行 $ROW${TODO_LABEL:+（或文字「$TODO_LABEL」）}"
  C_FAIL=1
fi
[ "$C_FAIL" -eq 0 ] || fail=1

echo
echo "== D queue 全表单在办 =="
: > "$ONGOING"
while IFS=$'\t' read -r QLINE_NO QN QROW QCARD QSTATUS QLINE; do
  case "$QSTATUS" in *在办*) printf '%s\n' "$QSTATUS|$QN|$QLINE_NO|$QLINE" >> "$ONGOING" ;; esac
done < "$QHITS"
ONGOING_N=$(grep -c . "$ONGOING")
if [ "$ONGOING_N" -le 1 ]; then
  echo "   PASS: 在办 $ONGOING_N 处（≤1）"
else
  echo "   FAIL: queue 在办 $ONGOING_N 处（>1）"
  while IFS='|' read -r st qn line_no line; do
    echo "   #$qn（queue.md:$line_no）：$line"
  done < "$ONGOING"
  fail=1
fi

echo
if [ "$fail" -eq 0 ]; then echo "ALL PASS"; else echo "FAILED"; fi
exit "$fail"