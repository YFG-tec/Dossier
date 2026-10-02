#!/usr/bin/env bash
# 源码划的节 ↔ 根锁的落点，两侧对账。零权威，只作证，不算「通过」。
# 用法：bash docs_meta/tests/check-sect.sh
#
# 谁加的：2026-09-12 由 cmd/PROMPT_018.md 新增，契约测试这只手写的。
# **这是收紧，不是放宽**，所以不另发一次授权（同 check-role.sh、check-trace.sh 脚本头那条理由：
# 松判据才是人的那一爪，收紧是测试这只手的本职）。
#
# 为什么要有第十二本：2.6d 之前，**源码侧一个字都没说「哪几节的条款要落进 harness」**。
#   check-role 盯的是角色表 × 目标文件清单那一个 join，check-lock 盯根上那两份的存在和措辞，
#   两本都不过问「根锁那条出处指的节，源码里还在不在」。
#   具体后果有两个方向，都没有东西会红：
#     源码那一节被改名或删掉，根锁的 `→ 出处` 指向空气；
#     源码声明「这一节要落 harness」而产物里一处出处都没有。
#   本本补的就是这两个方向，各一段（A、B）。
#
# 钉的是哪几裁：
#   **划节，不标行**（人 2026-09-12 裁：「1.1 乙，一刀处理完」）。复活逐行标记 = 人要点 84 次。
#   **取乙：划节 + 检查认「节在 src/ 且 harness 有对应落点」，仍不数条款。**
#   **节名表必须现算**（根 CLAUDE.md 禁令那一块：要查就现算，不存覆盖表）。
#     本本一个节名都不写死，两侧全从盘上现算。
#   **join 两侧不是第二真相**：标记是源码自己声明，引用是产物自己声明，本本只 join 它们。
#     今天两侧对齐所以绿；任何一侧后来动了就红——删一条出处红 B，加一个标记红 A。
#   **quotes.md 豁免**（卡上第一条量到它零个二级节）。所以本本不写「每一份都至少要有一个带标记的节」，
#     那会逼人去改一份没有节的文件。D 段只查总数 ≥ 1。
#
# 口径（脚本和文档必须同一套）：
#
#   A 源码 → 产物 —— 每一个带后缀的 `## ` 节，根 CLAUDE.md 里至少有一处
#     `<该文件名>.md「<该节名>」`。红了指：**划了节但产物没落点，该落没落。**
#     **只要「至少一处」。** 根锁里 workflow.md「全程」引了两次，重复引不红也不合并——
#     去重是产物侧的整理，不是本本的活。
#
#   B 产物 → 源码 —— 根 CLAUDE.md 里每一处紧邻文件名的 `.md「<节名>」`，
#     那份文件里必须有一行恰好等于 `## <节名>` 加后缀。红了指：
#     **产物引了一个源码没划进射程的节，或者引了一个不存在的节。**
#     文件名按 basename 落到 docs_meta/src/ 里找：根锁两种写法都有（带 src/ 整路径的、光文件名的），
#     两种指的是同一份。basename 在 src/ 里没有对应文件也是红——射程就是 src/，
#     引到射程外面的东西，本本答不了它对不对，**答不了就红，不假绿**。
#
#   C 短锁不长出第二个 join 面 —— AGENTS.md 里紧邻文件名的 `.md「节名」` 引用**恰好 0 处**。
#     红了指：有人开始往短锁里复述，根锁那句「短锁 AGENTS.md 只写一行指回来，不复述」被破了。
#     **这个 0 是钉住不许长，不是证明短锁现在对。**
#
#   D 防恒真 + 防标记漂到正文 —— 两问：
#     带后缀的节总数 ≥ 1（标记被清光的话 A 段会变成恒绿，这一格挡的是那个）；
#     后缀在 docs_meta/src/ 里**只许出现在 `^## ` 行，且必须在行尾，且一行只许一处**。
#     红了指：标记被清光（检查变恒绿），或者后缀被当成正文写法用。
#     「一行只许一处」不是新断言，是「每一处都必须在行尾」的机械式：
#     一行两处，前一处必然不在行尾。
#     **这一段成立的唯一前提是那个字面在正文里写不出来。** 卡 PROMPT_018 第六条 (c) 量过了：
#     src/ 里「夹注开头带箭头」这种形状 0 处，这仓从不这么写。
#     **施工时不许换字面。** 换了就得回头重量那一条，那是新的一张卡。
#     （PROMPT_017 整张退卡就死在这一格：它选的字面本来就被一句正文占着。）
#
# 取法写死，不许自选（卡上原话）：
#   用 awk -F'「|」' 按字段取；偶数字段是引号里的名，前一个字段判断是不是以 .md 或 .md` 收尾。
#   **字节取反禁用**，在 CJK 上挂，实测 17 处只抓到 3 处——所以本本一处取反类都不写，
#     引用全靠 awk 按「」切字段拿，节名全靠 index / substr 按字面拿。
#   节名逐字比对：反引号、全角标点、空格一律原样，不做 normalize。
#     **带反引号的两节要特别盯**（`docs/` 内部怎么切、`.tmp/` 是目录设计…）——逐字就能过，normalize 反而红。
#   后缀按字面剥：知道前缀是三个字符、后缀多长，就按长度切，不写正则通配。
#   抽取器自检：每行「和」的数目必须相等。不等说明「偶数字段就是引号里的名」这条在那一行上不成立，
#     取法不可信——记在用它的那一段里（根锁记 B 段，短锁记 C 段），不另开一段。
#
# 造红用的根目录开关：环境变量 SECT_ROOT，默认仓库根。
#   **它只为卡 PROMPT_018 第 3 件在 .tmp/ 的副本上造红用，不是射程可调。**
#   造红必须造在副本上，源码和产物一个字不动——这是纪律，不是方便。
#   **run.sh 走默认那一路，不带参数、不设这个变量。**
#
# 副本内容检查用的源码根开关：环境变量 SECT_SRC，默认仓库根下的 docs_meta/src。
#   **副本那一路，产物在副本、源码仍在母本，两侧根不同。**
#   所以 SECT_ROOT 指副本时，SECT_SRC 照旧指母本 src——两个根分设、不共根，SECT_SRC 不跟着 SECT_ROOT 走。
#   **run.sh 走默认那一路，不带参数、不设这个变量。**
#
# 查不到什么，照写不吹：
#   查不到「根锁引的那句话和节里写的是不是一回事」。A 段只答「根锁引了这个节名」，
#     引的那句和节里的条款对不对得上，**意思机器读不了**（design/paradigm.md 第 6 节：
#     机检是词的共现，不是意思）。这是本本最大的一条。
#   查不到条款级。2.6b 那句「src/ 里每条禁令」，本本把「每条」收成「每节」——
#     节里有几条、哪一条落了哪一条没落，仍然不可枚举。这是形状的代价，裁的时候就知道。
#   查不到「下界以外该不该划」。某一节根锁现在没引、而它本来就该落进 harness——
#     那是判断，不是断言。下界之内多划红 A、少划红 B，两个方向机器都看得见；这一格没人看着。
#   查不到那三类不紧邻文件名的引用有没有落点：节内短语、没有节名的位置、纯口令词。
#     取法按构造把它们排除在 join 之外——**排除不等于解决**，它们引的那几句话谁看着，没人看着。
#   查不到抽取器自己抽漏了没有。A 段和 B 段读的是同一个抽取器：抽漏一条引用，
#     A 不会为它红、B 也不会去查它，**两侧一起静默变小，全绿**。
#     这是本本唯一一处红不出来的漏，只能靠人照卡上那句判据手工再数一次兜，兜不硬。
#   查不到 quotes.md 有没有落点。它 9 条裸引号原句、零个二级节，无处挂标记，本本不给它造节。
#   查不到 AGENTS.md 到底有没有复述根锁。C 段只答「有没有 join 面」，
#     复述可以不带 `.md「」` 这种形状，那样复述了 C 段照样绿。
#   查不到哪一边先动的。两侧对不上时本本只说对不上，**谁先动要翻 git**。
cd "$(dirname "$0")/../.."
fail=0
ROOT="${SECT_ROOT:-.}"
LOCK="$ROOT/CLAUDE.md"
SHORT="$ROOT/AGENTS.md"
SRC="${SECT_SRC:-$ROOT/docs_meta/src}"
SUF='（→ harness）'
# 字段分隔符用 US（\037），不用制表符：制表符是 IFS 空白字符，read 会剥前导的、折叠中间的，
# 空字段一被吃掉整行就错位——**而且错位了不会红**。这条是 check-role.sh 第一版踩出来的。
SEP=$(printf '\037')

echo "（射程：$SRC/*.md × $LOCK × $SHORT，源码划的节 × 产物写的出处，两侧 join）"
if [ -n "$SECT_ROOT" ]; then
  echo "（SECT_ROOT 已设成 $SECT_ROOT —— 这一路既可造红，也对副本做内容检查；不是射程可调）"
fi
echo

# ---- 抽取器：一份文件里所有「紧邻文件名的 .md「节名」」引用 ----
# 输出 R 行：R<SEP>文件名<SEP>行号<SEP>节名
# 输出 W 行：W<SEP><SEP>行号<SEP>抽取器自检的告警
refs_of() {
  awk -F'「|」' -v sep="$SEP" '
    { sub(/\r$/, "") }
    {
      a = $0; n1 = gsub(/「/, "", a)
      b = $0; n2 = gsub(/」/, "", b)
      if (n1 != n2) {
        printf "W%s%s%s%d%s「%d 个，」%d 个，数目不等——偶数字段取法在这一行上不成立\n", \
               sep, "", sep, FNR, sep, n1, n2
      }
      for (i = 2; i <= NF; i += 2) {
        pre = $(i - 1)
        sub(/`$/, "", pre)
        if (match(pre, /[A-Za-z0-9._\/-]+\.md$/)) {
          p = substr(pre, RSTART, RLENGTH)
          k = split(p, seg, "/")
          printf "R%s%s%s%d%s%s\n", sep, seg[k], sep, FNR, sep, $i
        }
      }
    }
  ' "$1"
}

# ---- 现算一：src/ 里带后缀的 ## 节 → 文件名 / 行号 / 节名 ----
sects=""
if [ -d "$SRC" ]; then
  sects=$(for f in "$SRC"/*.md; do
    [ -e "$f" ] || continue
    awk -v sep="$SEP" -v suf="$SUF" -v fn="$(basename "$f")" '
      { sub(/\r$/, "") }
      index($0, "## ") == 1 {
        if (length($0) > length(suf) + 3 && substr($0, length($0) - length(suf) + 1) == suf) {
          printf "%s%s%d%s%s\n", fn, sep, FNR, sep, substr($0, 4, length($0) - 3 - length(suf))
        }
      }
    ' "$f"
  done)
fi
nsect=$(printf '%s\n' "$sects" | grep -c .)

# ---- 现算二：根锁 / 短锁的引用 ----
lock_refs=""
short_refs=""
[ -f "$LOCK" ] && lock_refs=$(refs_of "$LOCK")
[ -f "$SHORT" ] && short_refs=$(refs_of "$SHORT")
nlock=$(printf '%s\n' "$lock_refs" | awk -F"$SEP" '$1 == "R"' | grep -c .)
echo "现算：src/ 里带后缀的节 $nsect 个；根锁里紧邻文件名的引用 $nlock 处"
echo

echo "== A 源码 → 产物：每个带后缀的节，根锁里至少有一处 <该文件名>.md「<该节名>」 =="
echo "   （红了指：划了节但产物没落点，该落没落。只要「至少一处」，重复引不红）"
a=0
if [ ! -f "$LOCK" ]; then
  echo "   BAD  $LOCK 不在盘上——根锁没了，A 段无从 join"
  a=1
fi
while IFS="$SEP" read -r fn ln name; do
  [ -n "$fn" ] || continue
  hit=$(printf '%s\n' "$lock_refs" | awk -F"$SEP" -v fn="$fn" -v nm="$name" \
        '$1 == "R" && $2 == fn && $4 == nm { c++ } END { print c + 0 }')
  if [ "$hit" -ge 1 ]; then
    echo "   OK   $fn:$ln 「$name」 → 根锁 $hit 处"
  else
    echo "   BAD  $fn:$ln 「$name」 → 根锁 0 处：划了节，产物里一处出处都没有"
    a=1
  fi
done <<EOF
$sects
EOF
if [ "$a" -eq 0 ]; then
  echo "   PASS: 每一个划了的节，根锁里都有落点"
else
  echo "   FAIL: 上面 BAD 那几节划了而产物没落点。**方向只准源码 → 产物**——"
  echo "         要么那一节本来不该划（撤后缀），要么根锁该补一条出处（那是另一刀的许可面）"
  fail=1
fi

echo
echo "== B 产物 → 源码：根锁每一处 <文件名>.md「<节名>」，那份文件里必须有带后缀的同名节 =="
echo "   （红了指：产物引了一个源码没划进射程的节，或者引了一个不存在的节）"
echo "   （节名逐字比对，反引号、全角标点、空格一律原样，不做 normalize）"
b=0
if [ ! -f "$LOCK" ]; then
  echo "   BAD  $LOCK 不在盘上"
  b=1
fi
nb=0
while IFS="$SEP" read -r kind fn ln name; do
  case "$kind" in
    W)
      echo "   BAD  $LOCK:$ln 抽取器自检不过：$name"
      b=1
      continue
      ;;
    R) ;;
    *) continue ;;
  esac
  nb=$((nb + 1))
  tgt="$SRC/$fn"
  if [ ! -f "$tgt" ]; then
    echo "   BAD  根锁:$ln 引了 $fn「$name」，$tgt 查不到——引到射程外面去了"
    b=1
    continue
  fi
  n=$(awk -v want="## $name$SUF" '{ sub(/\r$/, "") } $0 == want { c++ } END { print c + 0 }' "$tgt")
  if [ "$n" -ge 1 ]; then
    echo "   OK   根锁:$ln  $fn「$name」 → 源码里带后缀的同名节 $n 处"
  else
    echo "   BAD  根锁:$ln  $fn「$name」 → 源码里 0 处：那一节没划进射程，或者节名对不上"
    b=1
  fi
done <<EOF
$lock_refs
EOF
echo "   逐处查过 $nb 处（现算 $nlock 处）"
if [ "$nb" -ne "$nlock" ]; then
  echo "   BAD  现算 $nlock 处，只逐处查了 $nb 处——有引用在解析这一步就掉了"
  echo "        这一格是本段自己的哨兵：抽漏一条，A 不为它红、B 不去查它，两侧一起静默变小"
  b=1
fi
if [ "$b" -eq 0 ]; then
  echo "   PASS: 根锁每一处出处，源码那一侧都有带后缀的节接着"
else
  echo "   FAIL: 上面 BAD 那几处。**对不上改产物，不改出处**——源码是先动的那一边就翻 git 确认"
  fail=1
fi

echo
echo "== C 短锁不长出第二个 join 面：AGENTS.md 里紧邻文件名的 .md「节名」引用恰好 0 处 =="
echo "   （红了指：有人开始往短锁里复述。根锁写死「短锁只写一行指回来，不复述」）"
c=0
if [ ! -f "$SHORT" ]; then
  echo "   BAD  $SHORT 不在盘上——短锁没了，这个 0 就不是本来那个 0"
  c=1
else
  nshort=$(printf '%s\n' "$short_refs" | awk -F"$SEP" '$1 == "R"' | grep -c .)
  echo "   $SHORT 里紧邻文件名的引用 $nshort 处"
  if [ "$nshort" -ne 0 ]; then
    printf '%s\n' "$short_refs" | awk -F"$SEP" '$1 == "R" { print "   BAD  第 " $3 " 行：" $2 "「" $4 "」" }'
    c=1
  fi
  printf '%s\n' "$short_refs" | awk -F"$SEP" '$1 == "W" { print "   BAD  第 " $3 " 行 抽取器自检不过：" $4 }'
  wshort=$(printf '%s\n' "$short_refs" | awk -F"$SEP" '$1 == "W"' | grep -c .)
  [ "$wshort" -eq 0 ] || c=1
fi
if [ "$c" -eq 0 ]; then
  echo "   PASS: 短锁上一个 join 面都没有，那个 0 还钉着"
  echo "   （这个 0 是钉住不许长，不是证明短锁现在对——复述不带这种形状，本段照样绿）"
else
  echo "   FAIL: 短锁长出 join 面了。要复述就先改根锁那句话，那不是本本能裁的"
  fail=1
fi

echo
echo "== D 防恒真 + 防标记漂到正文：带后缀的节 ≥ 1；后缀只许在 ^## 行、必须在行尾、一行一处 =="
echo "   （红了指：标记被清光让 A 段变恒绿，或者后缀被当成正文写法用）"
d=0
if [ ! -d "$SRC" ]; then
  echo "   BAD  $SRC 不是目录——射程整个不在"
  d=1
fi
echo "   带后缀的节总数 $nsect"
if [ "$nsect" -ge 1 ]; then
  echo "   OK   ≥ 1，A 段不是恒绿"
else
  echo "   BAD  一个都没有了——标记被清光，A 段变成永真话"
  d=1
fi
if [ -d "$SRC" ]; then
  for f in "$SRC"/*.md; do
    [ -e "$f" ] || continue
    out=$(awk -v sep="$SEP" -v suf="$SUF" -v fn="$f" '
      { sub(/\r$/, "") }
      {
        t = $0; c = 0
        p = index(t, suf)
        while (p > 0) { c++; t = substr(t, p + length(suf)); p = index(t, suf) }
        if (c > 0) {
          why = ""
          if (index($0, "## ") != 1) { why = why "不是 ^## 行；" }
          if (c != 1) { why = why "本行 " c " 处，只许 1 处；" }
          if (substr($0, length($0) - length(suf) + 1) != suf) { why = why "后缀不在行尾；" }
          printf "%s%s%s:%d%s%s\n", (why == "" ? "OK" : "BAD"), sep, fn, FNR, sep, why
        }
      }
    ' "$f")
    [ -n "$out" ] || continue
    while IFS="$SEP" read -r verdict where why; do
      [ -n "$verdict" ] || continue
      if [ "$verdict" = "OK" ]; then
        echo "   OK   $where 后缀在 ^## 行、在行尾、一处"
      else
        echo "   BAD  $where $why"
        d=1
      fi
    done <<INNER
$out
INNER
  done
fi
if [ "$d" -eq 0 ]; then
  echo "   PASS: 标记还在，而且一处都没漂到正文"
  echo "   （这一段成立的前提是那个字面正文写不出来——卡 PROMPT_018 第六条 (c) 量过，不许换字面）"
else
  echo "   FAIL: 上面 BAD 那几行。**不许改正文让它绿**，也不许收窄本段容下那一行——那是松判据"
  fail=1
fi

echo
if [ "$fail" -eq 0 ]; then
  echo "ALL PASS"
else
  echo "FAILED"
fi
exit "$fail"
