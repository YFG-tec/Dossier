#!/usr/bin/env bash
# 开关那一份真相，有没有长出第二份。五段对账。零权威，只作证，不算「通过」。
# 用法：bash docs_meta/tests/check-switch.sh
#
# 谁加的：2026-09-13 由 cmd/PROMPT_019.md 第 3 件新增，契约测试这只手写的。
# **这是收紧，不是放宽**，所以不另发一次授权。这一次射程收窄是人 2026-09-13 亲自裁的，逐字记下原话「1，放到f里」；
# 下一次要收别的射程，仍旧一处一裁（松判据才是人的那一爪，收紧是测试这只手的本职）。
#
# 为什么要有第十三本：2.6e 把开关从 .claude/ 下那份集中配置搬进 .cursor/rules/switches.mdc，
#   根 CLAUDE.md 写一行 @ 导入。一份真相，两条通道（@ 只有实现席展开，规划席靠 alwaysApply 读同一份）。
#   没有本本，下面这几样盘上一处都不会红：
#     那一份被删、或者自动读的标记掉了 —— 两席都读不到，五份 harness 指针全成悬空；
#     导入行没了、或者变成两行 —— 实现席读不到，或者拧档改一处漏一处；
#     有人把开关的现值抄进角色文件 / 锁 / skill —— 第二真相，正是这次搬家要根治的病；
#     旧入口被搬回来 —— 两处入口，人改一处另一处静默变陈。
#
# **先说本本不查什么，免得被当成那个被否掉的哨兵。**
#   alwaysApply 还认不认、@ 还展不展开，**本本一个字都摸不到**——那是外部产品某一天的行为，
#   静态检查看不见，做成探针又进不了 run.sh（同 4.8）。
#   人 2026-09-13 裁过：不配哨兵，**不是推后，是配不出来**。
#   本本查的是另一件事：**一份真相有没有长出第二份。** 这一件 grep 得动。
#
# 射程的定义和取法（改它等于改判据）：
#   扫 根 CLAUDE.md + 根 AGENTS.md + .claude/** + .cursor/**。
#   **不含 docs_meta/docs/** —— 卡、SESSION.md、todo.md 是**描述**这几个字面的地方，
#     它们本来就要把字面写出来，扫进来必假红。
#   **不含 docs_meta/tests/ 自己** —— D 段要断言某个文件名字面在射程内为 0，
#     而本脚本非把那个字面写出来不可（不写就没法拿它去 grep）。tests/ 若在射程里，
#     本脚本扫到自己，当场假红。PROMPT_017 整张退卡就死在这种自伤上。
#     **旧入口的文件名不是开关的现值**，写它不算在脚本里存第二真相；
#     **开关的现值仍然一个字都不许写进本脚本**，见 C 段那一条。
#
#   取法分两路，按 SWITCH_ROOT **有没有被设置**：
#     **SWITCH_ROOT 未设（主仓库，run.sh 走这一路）** 用新取法排掉被忽略层：
#       git ls-files --cached --others --exclude-standard -- .claude .cursor
#       两半都要（进库的加上还没进库、未被忽略的）；新 harness 文件忘了 git add 也照得出。
#       **这条路答不出就红，不许退回 find**——取法只许走这一条。
#     **SWITCH_ROOT 已设（造红副本，.tmp/ 以下被 gitignore）** 用 find 遍历：
#       find "$ROOT/.claude" "$ROOT/.cursor" -type f
#       新取法查不出被忽略那一层，用 find 保证射程非 0。这条路造红用，那一层都是临时。
#
# 口径（脚本和卡必须同一套）：
#
#   A 真相那一份在不在、带不带自动读的标记 —— .cursor/rules/switches.mdc 在盘上，
#     且 frontmatter（第一行 --- 起，到下一条 --- 为止）里 alwaysApply: true 恰好一行。
#     红了指：真相那一份没了，或者没带自动读的标记（规划席那条通道断了）。
#
#   B 实现席那条通道 —— 根 CLAUDE.md 里指向那一份的 @ 导入**恰好一处**，且独占一行。
#     红了指：0 处 = 实现席读不到；多处 = 两条导入，改一处漏一处。
#     **两个数一起要**：处数防「一行里写了两次」，独占一行防「被写进句子当描述」——
#     写进句子里那一行不是导入，宿主不展开，光数处数看不出来。
#
#   C 现值没被抄进射程 —— 开关表里「原话」那一整格的字面，**射程内（除那一份自己）0 处**。
#     红了指：有人把现态抄进了角色文件、锁或 skill，第二真相。
#     **字面现算，不写死在脚本里**——写死就是脚本里也存了一份现态，本本自己变成第二真相。
#     取法：认表格行 → 认出「原话」是第几列（表头那一行现算，不假定列序）→
#       取每一条数据行那一格 → 去掉首尾空白。
#     取「原话」整格，**不取「值」那一格**：那一格是个常用字，射程里到处是
#       （重写 / 重载 / 重走 …），拿它当判据必假红——正是「字面被占」那条通则治的病。
#     答不了就红，不假绿：认不出那一列、或者表里一条数据行都没有，本段当场红。
#       表被清空的话这一段会变成恒绿，那一格挡的就是这个。
#
#   D 旧入口没被搬回来 —— 射程内旧那份集中配置的文件名字面 0 处，且它不在 .claude/ 下。
#     红了指：有人把旧入口搬回来了，或者指针没改干净，两处入口。
#
#   E harness 指针一份不漏 —— .claude/agents/ 下每一份 .md **恰好一处**指向新住处；
#     .claude/skills/*/SKILL.md 每一份**至多一处**，且带指针的至少有一份。
#     红了指：漏改一份（那一份成了悬空指针），或者一份里写了两处。
#     **份数现算，不存数、不存名单**（根 CLAUDE.md 禁令那一块：要查就现算，不存覆盖表）。
#       agents 那一侧从盘上 glob 现数，数到 0 本段当场红（目录空了这一段会变恒绿）。
#       skills 那一侧不是每一份都跟开关有关（写法类的 skill 不牵扯派不派），
#       所以只钉「至多一处」加一个下界 1。**那个 1 是下界，不是「几份」那个数。**
#
# 造红用的根目录开关：环境变量 SWITCH_ROOT，默认仓库根。
#   **它只为卡 PROMPT_019 第 4 件在 .tmp/ 的副本上造红用，不是射程可调。**
#   造红必须造在副本上，源码和产物一个字不动——这是纪律，不是方便。
#   **run.sh 走默认那一路，不带参数、不设这个变量。**
#
# 查不到什么，照写不吹：
#   进了库、但会被别的程序改写的文件仍在射程。今天没有这种文件；有了还会再炸一次。
#     这一收治的是「被忽略的那一层」，不是治「机器会替你写」那个病根。
#   被忽略的那一层里若真有人抄了现值，本本照不出来。让出去的理由：那一层不进库，
#     也不构成两席读到的那一份真相。这是明着让的，不是漏的。
#   取法依赖 git。不在 git 工作树里跑（例如把仓库打包拷走）时它答不出；
#     答不了要红，不许假绿——同 C 段现行那一格的写法。
#
#   查不到「人有没有把档拧对」。本本只答「现态只有一处」，答不了那一处写的值对不对——
#     值是人拧的，没有源码出处可对。
#   查不到换个措辞泄现态。C 段盯的是「原话」那一整格的固定说法；有人若改口叙述同一件事，
#     C 段照不出来。**这是明着留的窄口，不追着堵**（人 2026-09-13：尽到应尽的义务就行）。
#   查不到外部产品还认不认 alwaysApply / @。见上面第二段，静态检查摸不到。
#   查不到「本该带指针的那一份 skill 被换成了另一份」。E 段 skills 那一侧只有一个下界，
#     哪一份该带，源码里没有清单，本本不现编一张。
#   查不到 docs_meta/docs/ 里有没有人抄现值。那一层在射程外，是**描述**这些字面的地方。
#     历史卡里指向旧入口的行号搬完就悬空——那是历史的正常形态，不是失准，本本不去红它。
#   查不到哪一边先动的。对不上时本本只说对不上，**谁先动要翻 git**。
cd "$(dirname "$0")/../.."
fail=0
ROOT="${SWITCH_ROOT:-.}"
ROOT="${ROOT%/}"
LOCK="$ROOT/CLAUDE.md"
SHORT="$ROOT/AGENTS.md"
MDC="$ROOT/.cursor/rules/switches.mdc"
IMP='@.cursor/rules/switches.mdc'
PTR='.cursor/rules/switches.mdc'
OLD='config.md'
GIT_FAILED=0

# 主仓库那一路必须能用 git，否则答不出要红
if [ ! -v SWITCH_ROOT ]; then
  # SWITCH_ROOT 未设，这是主仓库，检查 git 是否可用
  if ! git ls-files --cached --others --exclude-standard -- .claude .cursor >/dev/null 2>&1; then
    GIT_FAILED=1
  fi
fi

# occ <文件> <字面> —— 数出现**处数**，不是行数：一行里写两次也要看得见。
occ() {
  grep -oF -- "$2" "$1" 2>/dev/null | wc -l | tr -d ' '
}

# 射程清单现算，不写死名单。顺序固定，便于逐行对读。
# 按 SWITCH_ROOT 有没有被设分两路：未设（主仓库）用 git ls-files 排掉被忽略层，
# 已设（造红副本）用 find。两条路的分界就是「是否设了 SWITCH_ROOT」。
scope_list() {
  [ -f "$LOCK" ] && printf '%s\n' "$LOCK"
  [ -f "$SHORT" ] && printf '%s\n' "$SHORT"
  if [ -v SWITCH_ROOT ]; then
    # SWITCH_ROOT 已设，这是造红副本（被 gitignore），用 find
    find "$ROOT/.claude" "$ROOT/.cursor" -type f 2>/dev/null | sort
  else
    # SWITCH_ROOT 未设，这是主仓库，用 git ls-files 排掉被忽略层
    # 两半都要：--cached（进库的）加 --others --exclude-standard（未进库、未被忽略的）
    # 答不出就红，不许退回 find——那是两条路的分界
    if [ "$GIT_FAILED" -eq 0 ]; then
      git ls-files --cached --others --exclude-standard -- .claude .cursor 2>/dev/null | sed "s|^|$ROOT/|" | sort
    fi
  fi
}
SCOPE=$(scope_list)
nscope=$(printf '%s\n' "$SCOPE" | grep -c . | tr -d ' ')
echo "== 射程（现算，$nscope 份，用 git ls-files 或 find 分两路）：根 CLAUDE.md + 根 AGENTS.md + .claude/** + .cursor/** =="
echo "   根目录：$ROOT   （不含 docs_meta/docs/，不含 docs_meta/tests/ 自己；新取法排掉被忽略层）"
if [ "$GIT_FAILED" -eq 1 ]; then
  echo "   FAIL: 主仓库那一路 git 命令答不出，取法只许走这一条，不许退回 find"
  fail=1
fi
if [ "$nscope" -eq 0 ]; then
  echo "   FAIL: 射程内一份文件都没有，下面几段会全变恒绿"
  fail=1
fi

echo
echo "== A 真相那一份在盘上，且带自动读的标记 =="
if [ ! -f "$MDC" ]; then
  echo "   FAIL: $MDC 不在盘上——真相那一份没了，五份 harness 指针全成悬空"
  fail=1
else
  echo "   在盘上：$MDC"
  fm=$(awk '
    NR == 1 { line = $0; sub(/\r$/, "", line); if (line !~ /^---[ \t]*$/) { print "__NOFM__"; exit } ; next }
    { line = $0; sub(/\r$/, "", line); if (line ~ /^---[ \t]*$/) exit; print line }
  ' "$MDC")
  if printf '%s\n' "$fm" | grep -q '__NOFM__'; then
    echo "   FAIL: 第一行不是 ---，这一份没有 frontmatter，规划席那条通道认不出它"
    fail=1
  else
    nalways=$(printf '%s\n' "$fm" | grep -cE '^alwaysApply:[ \t]*true[ \t]*$' | tr -d ' ')
    if [ "$nalways" -eq 1 ]; then
      echo "   frontmatter 里 alwaysApply: true 恰好一行"
    else
      echo "   FAIL: frontmatter 里 alwaysApply: true 数到 $nalways 行，要恰好 1"
      fail=1
    fi
  fi
fi

echo
echo "== B 根 CLAUDE.md 里那行 @ 导入，恰好一处 =="
if [ ! -f "$LOCK" ]; then
  echo "   FAIL: $LOCK 不在盘上"
  fail=1
else
  nimp=$(occ "$LOCK" "$IMP")
  nline=$(grep -cE '^@\.cursor/rules/switches\.mdc[ \t]*$' "$LOCK" | tr -d ' ')
  if [ "$nimp" -eq 1 ] && [ "$nline" -eq 1 ]; then
    echo "   导入处数 1，独占一行 1 —— 实现席那条通道恰好一条"
  else
    echo "   FAIL: 导入处数 $nimp、独占一行 $nline，两个都要恰好 1"
    echo "         0 = 实现席读不到；多 = 两条导入，改一处漏一处；写进句子里那一行不是导入"
    fail=1
  fi
fi

echo
echo "== C 开关的现值没被抄进射程（字面从开关表现算，脚本正文不写死）=="
if [ ! -f "$MDC" ]; then
  echo "   FAIL: 开关表那一份不在盘上，字面无从现算——答不了就红，不假绿"
  fail=1
else
  vals=$(awk '
    {
      line = $0; sub(/\r$/, "", line)
      if (line !~ /^[ \t]*\|/) { intable = 0; key = 0; prevn = 0; next }
      nf = split(line, cell, "|")
      n = 0
      for (i = 2; i <= nf - 1; i++) {
        g = cell[i]; gsub(/^[ \t]+/, "", g); gsub(/[ \t]+$/, "", g)
        n++; col[n] = g
      }
      issep = (n > 0)
      for (i = 1; i <= n; i++) if (col[i] !~ /^:?-+:?$/) issep = 0
      if (issep) {
        key = 0
        for (i = 1; i <= prevn && i <= n; i++) if (prev[i] == "原话") key = i
        if (key) { intable = 1; found = 1 }
        next
      }
      if (intable && key) { if (key <= n && col[key] != "") print col[key]; next }
      prevn = n
      for (i = 1; i <= n; i++) prev[i] = col[i]
    }
    END { if (!found) print "__NOKEY__" }
  ' "$MDC")
  if printf '%s\n' "$vals" | grep -q '__NOKEY__'; then
    echo "   FAIL: 开关表里认不出「原话」那一列——取法答不了，答不了就红，不假绿"
    fail=1
  elif [ -z "$vals" ]; then
    echo "   FAIL: 开关表一条数据行都没有——本段会变成恒绿，这一格挡的就是那个"
    fail=1
  else
    nval=$(printf '%s\n' "$vals" | grep -c . | tr -d ' ')
    echo "   现算出 $nval 条开关现值（字面不印出来，印出来日志里就多一份）"
    cbad=0
    while IFS= read -r v; do
      [ -n "$v" ] || continue
      while IFS= read -r f; do
        [ -n "$f" ] || continue
        [ "$f" = "$MDC" ] && continue
        c=$(occ "$f" "$v")
        if [ "$c" -ne 0 ]; then
          echo "   BAD: $f 里抄了 $c 处开关现值 —— 行号 $(grep -nF -- "$v" "$f" | cut -d: -f1 | tr '\n' ' ')"
          cbad=$((cbad + 1))
        fi
      done <<EOF
$SCOPE
EOF
    done <<EOF
$vals
EOF
    if [ "$cbad" -eq 0 ]; then
      echo "   射程内（除开关表自己）0 处，现态仍然只有一份"
    else
      echo "   FAIL: 上面 $cbad 份抄了开关的现值。现态只许住开关表那一份，别处要查就读那一份"
      fail=1
    fi
  fi
fi

echo
echo "== D 旧入口没被搬回来 =="
dbad=0
while IFS= read -r f; do
  [ -n "$f" ] || continue
  c=$(occ "$f" "$OLD")
  if [ "$c" -ne 0 ]; then
    echo "   BAD: $f 里 $c 处提到旧入口那个文件名 —— 行号 $(grep -nF -- "$OLD" "$f" | cut -d: -f1 | tr '\n' ' ')"
    dbad=$((dbad + 1))
  fi
done <<EOF
$SCOPE
EOF
if [ -e "$ROOT/.claude/config.md" ]; then
  echo "   BAD: $ROOT/.claude/config.md 又在盘上了"
  dbad=$((dbad + 1))
fi
if [ "$dbad" -eq 0 ]; then
  echo "   射程内 0 处，旧入口也不在盘上"
else
  echo "   FAIL: 上面 $dbad 处。留一个旧入口就是两处入口，拧档改一处另一处静默变陈"
  fail=1
fi

echo
echo "== E harness 指针一份不漏（份数现算，不存名单、不存数）=="
nag=0
agbad=0
for f in "$ROOT"/.claude/agents/*.md; do
  [ -f "$f" ] || continue
  nag=$((nag + 1))
  c=$(occ "$f" "$PTR")
  if [ "$c" -ne 1 ]; then
    echo "   BAD: $f 指向新住处 $c 处，要恰好 1"
    agbad=$((agbad + 1))
  fi
done
if [ "$nag" -eq 0 ]; then
  echo "   FAIL: .claude/agents/ 下现数 0 份 .md——本段会变成恒绿，这一格挡的就是那个"
  fail=1
else
  if [ "$agbad" -eq 0 ]; then
    echo "   agents 现数 $nag 份，每一份恰好一处"
  else
    echo "   FAIL: agents 现数 $nag 份，其中 $agbad 份不是恰好一处。漏改的那一份成了悬空指针"
    fail=1
  fi
fi
nsk=0
nskptr=0
skbad=0
for f in "$ROOT"/.claude/skills/*/SKILL.md; do
  [ -f "$f" ] || continue
  nsk=$((nsk + 1))
  c=$(occ "$f" "$PTR")
  if [ "$c" -gt 1 ]; then
    echo "   BAD: $f 指向新住处 $c 处，至多 1"
    skbad=$((skbad + 1))
  fi
  [ "$c" -eq 1 ] && nskptr=$((nskptr + 1))
done
if [ "$skbad" -eq 0 ] && [ "$nskptr" -ge 1 ]; then
  echo "   skills 现数 $nsk 份，带指针的 $nskptr 份，没有一份写重"
else
  echo "   FAIL: skills 现数 $nsk 份，带指针的 $nskptr 份，写重的 $skbad 份"
  echo "         带指针的要至少一份（那个 1 是下界，不是「几份」那个数），且没有一份写两处"
  fail=1
fi

echo
if [ "$fail" -eq 0 ]; then echo "ALL PASS"; else echo "FAILED"; fi
exit $fail
