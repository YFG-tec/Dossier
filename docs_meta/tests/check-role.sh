#!/usr/bin/env bash
# 源码 ↔ harness 的对账线。零权威，只作证，不算「通过」。
# 用法：bash docs_meta/tests/check-role.sh
#
# 谁加的：2026-09-12 由 cmd/PROMPT_015.md 新增，实现席这只手写的。
# **这是收紧，不是放宽**，所以不另发一次授权（同 check-lock.sh 脚本头那条理由：
# 松判据才是人的那一爪，收紧是测试这只手的本职）。
#
# 为什么要有第十本：2.6a 把七份角色文件落到盘上，**至今没有任何一本看着它们**。
#   check-seat 扫 roles.md 的措辞，check-lock 扫根上那两份，两本都不过问 .claude/ 里有没有东西。
#   具体后果：源码那张表加一只手而产物没落，没有东西会红；
#   落在盘上的那几份被删掉一份，也没有东西会红。
#
# 钉的是哪几裁：
#   **角色表是那几只手的源代码**（人 2026-09-12 原话：「乙是对的，本来 role 就是生成各个角色的源代码」）。
#   **手够得着什么落在角色文件里**（claude-code.md 32-33）——角色文件是那张表的产物，不是第二处定义。
#   **工具面写白名单**（claude-code.md 35-36）——所以 D 段查的是那一行里有没有多出来的东西。
#   **要查就现算，不存覆盖表**（根 CLAUDE.md 禁令那一块）——本本一张名单都不写死，全从两张源码表 join。
#
# 口径（脚本和文档必须同一套）：
#
#   A 角色表结构在 —— roles.md「公共角色」那张表：表头四格齐、表体至少一行。
#     **不查行数。** 盘上现在七行，但写死成「恰好七」的话，源码那张表加一只手就假红,
#     那和「名单不许写死」是同一个病。新来的那一行该不该有产物，由 C 段去红。
#     **它挡的是表整个没了或者被抽象掉，挡不住表被削瘦**——七行削成两行，A 段是绿的。
#     两头都有代价，本本取了不假红那一头，代价就是这一格。
#
#   B 目标文件清单结构在，且逐份在盘上 —— claude-code.md「目标文件」那个 code block。
#     **按清单里写的那条整路径逐条各查一次，不许按文件名去找产物。**
#     按文件名找会假绿：清单里有几份是同名的，找到任意一份就算命中，
#     删掉其中一份、另外几份还在，这一段照样绿——**一本查漏的检查自己漏了。**
#     「逐条各查一次」也是口径的一部分，不是实现细节：
#     某个目录下有一份同名文件就算命中，同样是上面那个假绿。
#     **要的是清单那一行对那一条路径，一对一。**
#     路径全部从清单现算，脚本里不写死任何一条。
#
#   C join 对得上 —— 角色表每一行反引号里的 id，拿去清单里现算落点。两问分开：
#     **带 id 且在清单里的**，产物文件必须在；
#     **落在 agent 那个目录下的**，另外还要有 tools: 那一行；
#     落在 skill 那个目录下的只查文件在——那一类是一个目录加一份说明文件，本来就没有 tools: 行。
#     **落哪个目录是清单自己写的，脚本现算**，不在脚本里写一张「这几个是 agent」的名单。
#     **带 id 不在清单里的不红**——那是源码在说「这只手不落这张桌」，不是产物漏了。
#     **不带 id 的也不红**——主会话本来就不该落成文件。
#     这两条都是源码自己在说话，不是脚本在裁。
#     **它挡不住「角色表加了新 id、清单没跟上」**：那一类和「不落这张桌」同形,
#     两者都是「带 id、不在清单里」。要分开这两种，得先有一处源码说清哪几只手必须落这张桌。
#     本本解不了，照记不补。
#
#   D 零写权限兑现了 —— 角色表里「只许动」那一格写着「无」的那几只手，
#     产物的 tools: 行里不许有 Write、不许有 Edit。
#     **哪一只手是零权限，现算**，不写死成某个 id：将来另一只手也被设成「只许动：无」，这一段自动盖住它。
#     **只扫 tools: 那一行，不扫全文。** 扫全文会误伤正文里「不给 Write / Edit」那句话,
#     那是 2.6a 已经踩过一次的坑。
#     **方向不对称：松了要红，收紧不红。** 白名单里少一样工具是收紧，不是本本要拦的。
#
# **不设放行词。** 四段一条都没留「同一行还出现某某就放过」的口子——同 check-lock.sh、check-link.sh A。
#
# 副本内容检查用的根目录开关：环境变量 ROLE_ROOT，默认仓库根（不设时路径不前缀）。
#   **它是给副本用的：对副本做内容检查时，产物在副本，源码仍是母本那一份。**
#   所以只把产物那一侧的路径接上根；ROLES / LIST 两行指的是母本那两张源码表，两行一个字不动。
#   造红也走这一路，破的是副本那一份，母本一个字不动——这是纪律，不是方便。
#   **run.sh 走默认那一路，不带参数、不设这个变量。**
#
# **设了 ROLE_ROOT 那一路，B 段整段不跑。** 原因：副本里那几份按设计不落这张桌，
#   B 段「目标文件清单逐条都在盘上」逐条查必假红。**代价照写，不假装没损失：**
#   副本上「清单逐条都在」这一格没有了——清单里每条的落点由 C 段按 id 兜住，
#   不落这张桌的那几条两段都不逐条查。
#   跳的依据是「设了开关」，**脚本里不写死是哪一份**（同本本「要查就现算」那条口径）。
#
# 查不到什么，照写不吹：
#   查不到 src/ 里那几十行带禁止词的句子有没有落点。**本本只盖角色这一块**,
#     那一头至今没有可枚举的边界，缺口归 todo.md 2.6d，本本不假装盖住了。
#   查不到角色文件正文写得对不对。**只看 frontmatter 和文件在不在**，正文写歪了不会红。
#   查不到有没有把这张桌的合同抄进角色文件。那一条仍然只能人读。
#   查不到哪一边先动的。产物和源码对不上时，本本只说对不上，**谁先动要翻 git**。
#   查不到 .claude/ 里别的东西。settings.json、几份 SKILL.md 的正文，都不在射程。
#   查不到清单里那份文件是不是「对的那一份」。**只查那条路径上有文件**——
#     清单里有几份同名，本本靠整路径区分它们，靠的不是内容。
#   查不到副本那一路「目标文件清单逐条都在盘上」。设了 ROLE_ROOT 时 B 段整段不跑，
#     那一格就是空的——只有 C 段按 id 兜住有落点的那几条，不落这张桌的那几条两段都不查。
cd "$(dirname "$0")/../.."
fail=0
ROOT="${ROLE_ROOT:-}"
ROOT="${ROOT%/}"
ROLES=docs_meta/src/roles.md
LIST=docs_meta/src/claude-code.md
# 字段分隔符用 US（\037），不用制表符：制表符是 IFS 空白字符，read 会剥掉前导的、
# 折叠中间连着的，空字段一被吃掉整行就错位——**而且错位了不会红**。第一版就是这么漏查了两条路径。
SEP=$(printf '\037')

echo "（射程：roles.md 公共角色表 × claude-code.md 目标文件清单，两张源码表 join → 盘上）"
echo

# ---- 现算一：清单块 → 目录前缀 / 条目 / 条目 id / 整路径 ----
list_rows=$(awk '/^## 目标文件/{f=1} f&&/^```text/{g=1;next} g&&/^```/{exit} g' "$LIST" | awk -v sep="$SEP" '
  /^[^ ]/ && /\/$/ { dir=$1; next }
  /^  [^ ]/ {
    e=$1; split(e, s, "/"); id=s[1]; sub(/\.md$/, "", id)
    printf "%s%s%s%s%s%s%s%s\n", dir, sep, e, sep, id, sep, dir, e
    next
  }
  /^[^ ]/ {
    e=$1; split(e, s, "/"); id=s[1]; sub(/\.md$/, "", id)
    printf "%s%s%s%s%s%s\n", sep, e, sep, id, sep, e
  }
')

# ---- 现算二：角色表表体 → id / 只许动那一格 ----
role_rows=$(awk -F'|' -v sep="$SEP" '
  /^## 公共角色/ { sec=1; next }
  sec && /^\|/ {
    n++
    if (n <= 2) next
    id=""
    if (match($2, /`[a-zA-Z_-]+`/)) id=substr($2, RSTART+1, RLENGTH-2)
    who=$2; only=$3
    gsub(/^ +| +$/, "", who); gsub(/^ +| +$/, "", only)
    printf "%s%s%s%s%s\n", id, sep, who, sep, only
    next
  }
  sec && !/^\|/ && n > 2 { exit }
' "$ROLES")

echo "== A 角色表结构在：表头四格齐，表体至少一行 =="
echo "   （不查行数——写死成「恰好七行」的话，源码那张表加一只手就假红）"
hdr=$(awk '/^## 公共角色/{s=1} s&&/^\|/{print; exit}' "$ROLES")
a=0
if [ -z "$hdr" ]; then
  echo "   BAD  那张表整个不见了"
  a=1
else
  echo "   表头：$hdr"
  nf=$(printf '%s' "$hdr" | awk -F'|' '{print NF}')
  for w in 角色 只许动 不许动 失败时; do
    if printf '%s' "$hdr" | grep -Fq "$w"; then
      echo "   OK   表头有「$w」这一格"
    else
      echo "   BAD  表头少了「$w」那一格"
      a=1
    fi
  done
  [ "$nf" -eq 6 ] || { echo "   BAD  表头不是四格（awk 数到 $nf 段）"; a=1; }
fi
body=$(printf '%s\n' "$role_rows" | grep -c . )
echo "   表体 $body 行"
[ "$body" -ge 1 ] || { echo "   BAD  表体一行都没有——表被抽空了"; a=1; }
if [ "$a" -eq 0 ]; then
  echo "   PASS: 表还在，结构没被抽象掉"
else
  echo "   FAIL: 角色表的结构塌了——那是静默降档，先看 roles.md 公共角色那一节"
  fail=1
fi

echo
echo "== B 目标文件清单：结构在，且逐条按整路径各查一次 =="
echo "   （路径从清单现算；不按文件名找——清单里有同名的，按名字找会假绿）"
if [ -n "$ROOT" ]; then
  echo "   设了 ROLE_ROOT：本段整段不跑 —— 副本那一路，清单里有几份按设计不落这张桌，逐条查必假红（代价见脚本头，落点由 C 段兜住）"
else
  b=0
  nlist=$(printf '%s\n' "$list_rows" | grep -c . )
  echo "   清单现算出 $nlist 条整路径"
  if [ "$nlist" -eq 0 ]; then
    echo "   BAD  清单块解析不出东西——「目标文件」那一节的 code block 没了或换了形状"
    b=1
  fi
  nchecked=0
  while IFS="$SEP" read -r dir entry id path; do
    [ -n "$path" ] || continue
    path="${ROOT:+$ROOT/}$path"
    nchecked=$((nchecked + 1))
    if [ -f "$path" ]; then
      echo "   OK   $path"
    else
      echo "   BAD  $path —— 清单写了，盘上没有"
      b=1
    fi
  done <<EOF
$list_rows
EOF
  echo "   逐条查过 $nchecked 条"
  if [ "$nchecked" -ne "$nlist" ]; then
    echo "   BAD  现算出 $nlist 条，只逐条查了 $nchecked 条——有条目在解析这一步就掉了"
    echo "        这一格是本段自己的哨兵：查漏的检查自己漏查，静默得很，第一版就是这么掉了两条"
    b=1
  fi
  if [ "$b" -eq 0 ]; then
    echo "   PASS: 清单里每一条路径上都有文件，一条不落"
  else
    echo "   FAIL: 上面 BAD 那几条，源码清单写了而产物没落"
    fail=1
  fi
fi

echo
echo "== C join 对得上：角色表的 id × 清单的落点 =="
echo "   （带 id 且在清单里的才查；不带 id、或带 id 不在清单里的都不红——那是源码在说话）"
echo "   （落哪个目录从清单现算，脚本里不写「这几个是 agent」那种名单）"
c=0
while IFS="$SEP" read -r id who only; do
  [ -n "$who" ] || continue
  if [ -z "$id" ]; then
    echo "   跳过 $who —— 不带 id，源码没说它落这张桌"
    continue
  fi
  hit=$(printf '%s\n' "$list_rows" | awk -F"$SEP" -v id="$id" '$3 == id {print $4}')
  dir=$(printf '%s\n' "$list_rows" | awk -F"$SEP" -v id="$id" '$3 == id {print $1}')
  if [ -z "$hit" ]; then
    echo "   跳过 \`$id\` —— 清单里 0 处，源码在说它不落这张桌"
    continue
  fi
  hit="${ROOT:+$ROOT/}$hit"
  if [ ! -f "$hit" ]; then
    echo "   BAD  \`$id\` → $hit 不在（B 段已经报过一次）"
    c=1
    continue
  fi
  case "$dir" in
    *agents/)
      nt=$(grep -c '^tools:' "$hit")
      if [ "$nt" -ge 1 ]; then
        echo "   OK   \`$id\` → $hit，清单写的是 agent 那个目录，tools: 行在"
      else
        echo "   BAD  \`$id\` → $hit 落在 agent 那个目录下，却没有 tools: 那一行"
        c=1
      fi
      ;;
    *)
      echo "   OK   \`$id\` → $hit，清单写的不是 agent 那个目录，只查文件在"
      ;;
  esac
done <<EOF
$role_rows
EOF
if [ "$c" -eq 0 ]; then
  echo "   PASS: 两张源码表 join 对得上，产物一份不缺"
else
  echo "   FAIL: 上面 BAD 那几格——两张源码表自己对不上，或者手加了而文件没落"
  fail=1
fi

echo
echo "== D 零写权限兑现了：「只许动：无」那几只手，tools: 行里没有 Write、没有 Edit =="
echo "   （哪一只手零权限，从表里现算，不写死某个 id；只扫 tools: 那一行，不扫全文）"
d=0
found=0
while IFS="$SEP" read -r id who only; do
  [ -n "$id" ] || continue
  case "$only" in
    无*) ;;
    *) continue ;;
  esac
  found=$((found + 1))
  hit=$(printf '%s\n' "$list_rows" | awk -F"$SEP" -v id="$id" '$3 == id {print $4}')
  hit="${ROOT:+$ROOT/}$hit"
  if [ -z "$hit" ] || [ ! -f "$hit" ]; then
    echo "   BAD  \`$id\` 写着「$only」，但产物查不到（B / C 段已经报过）"
    d=1
    continue
  fi
  tl=$(grep '^tools:' "$hit")
  echo "   \`$id\` 表里写「$only」"
  echo "      $hit  ->  $tl"
  for w in Write Edit; do
    if printf '%s' "$tl" | grep -Fq "$w"; then
      echo "      BAD  tools: 行里有 $w —— 零写权限被松掉了"
      d=1
    else
      echo "      OK   tools: 行里没有 $w"
    fi
  done
done <<EOF
$role_rows
EOF
if [ "$found" -eq 0 ]; then
  echo "   BAD  表里一只「只许动：无」的手都没有了——那一格是被松掉了，不是本来就没有"
  d=1
fi
if [ "$d" -eq 0 ]; then
  echo "   PASS: 零写权限在 frontmatter 上兑现了"
  echo "   （方向不对称：松了红，收紧不红——白名单里少一样工具是收紧）"
else
  echo "   FAIL: 零写权限没兑现——查 roles.md 那一行和产物的 tools: 行，改产物不改源码"
  fail=1
fi

echo
if [ "$fail" -eq 0 ]; then
  echo "ALL PASS"
else
  echo "FAILED"
fi
exit "$fail"
