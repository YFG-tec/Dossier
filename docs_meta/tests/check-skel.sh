#!/usr/bin/env bash
# 宿主骨架验收：一棵宿主树是不是范式要的那个形状。零权威，只作证，不算「通过」。
# 用法：bash docs_meta/tests/check-skel.sh            自造临时树，跑 init 后检查，跑完清掉
#       bash docs_meta/tests/check-skel.sh TARGET     只读扫描 TARGET，一个字节不写
#
# 谁加的：2026-09-16 由 cmd/PROMPT_027.md 新增，契约测试这只手写的。
# **这是收紧，不是放宽**，不另发一次授权（roles.md：收紧是测试那只手的本职）。
#
# 为什么要有这一本：2.8c 交了 init.py，宿主那棵树现在铺得出来了。没有任何一本把关看得见它。
#   init.py 改坏了，十四本一本都不会红。这一本补的就是这一格：扫宿主骨架本身。
#
# 为什么不给靶子的时候要自己造一棵：母本自己不是宿主，盘上没有宿主树。
#   跳过会让这一本恒真式。默认靶子取母本仓库根的父目录（D:\00_Works），没有 docs/，永远红。
#   所以只剩一条路：自己造。
#
# 为什么给了靶子就一个字节不写：把关不许改自己的断言对象。
#   宿主那棵树里装的是宿主的真活，一本检查跑过去顺手铺了两件，那是第二个 init，不是把关。
#
# 钉的是哪几裁：
#   **期望值不从 init.py 里取，从出处里取**（verify.md 第一条：同源同义反复）。
#   22 件清单独立抄一份：
#   - 11 件原有：8 件对 directory.md（:171–:182 的树、:126、:243），3 份 .gitkeep 对 cmd/PROMPT_026.md:262 那一裁
#   - 11 份新增 harness：CLAUDE.md、AGENTS.md 对 directory.md:115–:116，
#     .claude/ 及 .cursor/rules/switches.mdc 对本卡第 1 件那张清单（cmd/PROMPT_030.md）
#   三份 .gitkeep 和九份 harness 的出处是冻住的卡，不是代码。
#   **期望值不从核里取，这一条对 22 件都成立。**
#
#   **两路都判 D 段**（不给长大的桌留口子）。代价：桌一长大，D 段会红。
#   管长大的桌是另一本，不是把 D 放宽。那一件记进缺口。
#
# 它查不到什么，照写不吹：
#   **空跑那一路查不到任何一次真实的宿主铺装。** 盘上没有真宿主，自造的那棵是合成的。
#   **E 段没有红证。** 造红要改核，而核不归这只手。所以 E 现在是回归测——
#   今天不红，将来坏了才红。不是恒真式（能红），但本刀没在盘上演示过。
#   **这一本自己没有哨兵。** 断言写反了不会有东西红，只有四棵坏树和人眼。
#   **F 段查不到那个串指的是不是这一次的子模块。** 指到另一份真的 `directory.md` 照样绿。
#   和 check-link.sh C 段「拦不住指错了刀」同一个形状。
#
# 口径（脚本和文档必须同一套，见 cmd/PROMPT_027.md 两路表第 2 行、这一本的「这一本自己的规矩」）：
#
#   靶子路径规范：给相对靶子时，相对路径按调用者当时所在目录算，不按仓库根算。
#   两路都印：检查开始前，两种调法（给靶子或自造）都要印出已解析的靶子绝对路径。
#
#   为什么自造那一路的临时树改到 .tmp/ 下：
#   原来是 mktemp -d，在 Windows 上落在 C:\Users\...\Temp\，和仓库（D:）不同盘。
#   init.py 的 os.path.relpath 跨盘符会抛 ValueError，当场退 4。
#   把临时树改到仓库 .tmp/ 下（.gitignore 排掉，和仓库永远同盘），就不会跨盘。
#   这样红的是核，不是临时目录选在哪儿。`.tmp/` 被排掉、盘面看不见，不算在母本上冒烟。
#
#   A 段 22 件逐件钉死：
#   |  路径              | 类型   |
#   | --------------- | ---- |
#   | docs/            | 目录   |
#   | docs/TODO.md     | 文件   |
#   | docs/SESSION.md  | 文件   |
#   | docs/cmd/        | 目录   |
#   | docs/cmd/.gitkeep | 文件  |
#   | docs/design/     | 目录   |
#   | docs/design/.gitkeep | 文件 |
#   | docs/reports/    | 目录   |
#   | docs/reports/.gitkeep | 文件 |
#   | .tmp/            | 目录   |
#   | .tmp/README.md   | 文件   |
#   | CLAUDE.md        | 文件   |
#   | AGENTS.md        | 文件   |
#   | .claude/settings.json | 文件 |
#   | .claude/agents/builder.md | 文件 |
#   | .claude/agents/contract-tester.md | 文件 |
#   | .claude/agents/review.md | 文件 |
#   | .claude/agents/spec-guard.md | 文件 |
#   | .claude/skills/example-report/SKILL.md | 文件 |
#   | .claude/skills/one-slice/SKILL.md | 文件 |
#   | .claude/skills/write-cmd/SKILL.md | 文件 |
#   | .cursor/rules/switches.mdc | 文件 |
#   目录要是目录，文件要是文件。缺一件红，类型错也红。红的那一行必须点名那一件的相对路径。
#
#   B 段：docs/figures/ 不许在（directory.md:189）
#
#   C 段三条，都是词的共现，不是字节比对（paradigm.md 第 6 节：能机检的是词，不是意思）：
#   - docs/TODO.md 里有一行是 `## 已办`（directory.md:173–:174）
#   - docs/SESSION.md 里有一行恰好是 `---`（人 2026-09-09 那一裁）
#   - .tmp/README.md 里含「零权威」（directory.md:247）
#
#   D 段七样不许在。两处出源，都是「加厚才出现」或「有第一张图时再建」，现在都不该在：
#   - 五样：research/、docs/README.md、utils/、papers/、codes/（directory.md:130–:137）
#   - 两样：docs/design/figures/、docs/reports/figures/（directory.md:191）
#   两路都判，不给长大的桌留口子。
#
#   E 段幂等（只在自造那一路）：
#   - 同一棵树上再跑一趟 init（--force --non-interactive）
#   - 末行必须是 `建 0 件，跳过 30 件，覆盖 0 件`
#   - 整树逐份 cksum 与第一趟相同
#   第二路跳过 E 的时候要印一行说明，必须同时含「幂等」和「跳过」。
#
# 保存调用者当前目录（cd 之前）
caller_pwd="$PWD"

cd "$(dirname "$0")/../.."

fail=0
target=""
create_tree=false
temp_tree=""

# ---- 参数解析 ----
if [ $# -eq 0 ]; then
  create_tree=true
elif [ $# -eq 1 ]; then
  target=$1
else
  echo "用法：bash docs_meta/tests/check-skel.sh [TARGET]" >&2
  exit 1
fi

# ---- 将相对路径转成绝对路径 ----
# 如果 target 是相对路径，则相对调用者的 PWD 转成绝对
if [ "$create_tree" = false ] && [ -n "$target" ]; then
  case "$target" in
    /* | [A-Z]:* | [a-z]:* )
      # 已经是绝对路径（/ 开头或 D:\ 格式或 d:\ 格式）
      ;;
    * )
      # 相对路径，转成相对调用者 PWD 的绝对路径
      target="$caller_pwd/$target"
      ;;
  esac
fi

# ---- 自造临时树 ----
if [ "$create_tree" = true ]; then
  temp_tree=$(mktemp -d "$PWD/.tmp/skel.XXXXXX")
  if [ -z "$temp_tree" ]; then
    echo "创建临时目录失败" >&2
    exit 1
  fi

  cleanup() {
    if [ -n "$temp_tree" ] && [ -d "$temp_tree" ]; then
      rm -rf "$temp_tree"
    fi
  }
  trap cleanup EXIT INT TERM

  target=$temp_tree

  # 第一趟 init
  python -B docs_meta/src/init.py "$target" >/dev/null 2>&1
  rc=$?
  if [ "$rc" -ne 0 ]; then
    echo "init.py 失败，退出码 $rc" >&2
    exit 1
  fi
fi

# ---- 检查靶子存在性和类型 ----
if [ ! -e "$target" ]; then
  echo "靶子不存在：$target" >&2
  exit 1
fi

if [ ! -d "$target" ]; then
  echo "靶子不是目录：$target" >&2
  exit 1
fi

# ---- 打印靶子路径（两路共用） ----
echo "靶子：$target"
echo

# ---- A 段：22 件逐件检查 ----
check_a() {
  local entries=(
    "docs:d"
    "docs/TODO.md:f"
    "docs/SESSION.md:f"
    "docs/cmd:d"
    "docs/cmd/.gitkeep:f"
    "docs/design:d"
    "docs/design/.gitkeep:f"
    "docs/reports:d"
    "docs/reports/.gitkeep:f"
    ".tmp:d"
    ".tmp/README.md:f"
    "CLAUDE.md:f"
    "AGENTS.md:f"
    ".claude/settings.json:f"
    ".claude/agents/builder.md:f"
    ".claude/agents/contract-tester.md:f"
    ".claude/agents/review.md:f"
    ".claude/agents/spec-guard.md:f"
    ".claude/skills/example-report/SKILL.md:f"
    ".claude/skills/one-slice/SKILL.md:f"
    ".claude/skills/write-cmd/SKILL.md:f"
    ".cursor/rules/switches.mdc:f"
  )

  local count=0
  for entry in "${entries[@]}"; do
    local path=${entry%:*}
    local type=${entry#*:}
    local full_path="$target/$path"
    local status="OK"

    if [ "$type" = "d" ]; then
      if [ ! -d "$full_path" ]; then
        echo "   FAIL: $path（目录）不存在"
        status="FAIL"
      fi
    else
      if [ ! -f "$full_path" ]; then
        echo "   FAIL: $path（文件）不存在"
        status="FAIL"
      fi
    fi

    if [ "$status" = "FAIL" ]; then
      fail=1
    else
      count=$((count+1))
    fi
  done

  if [ "$count" -eq 22 ]; then
    echo "   OK   22 件都在"
  else
    echo "   现有 $count / 22"
  fi
}

# ---- B 段：docs/figures 不许在 ----
check_b() {
  if [ -d "$target/docs/figures" ]; then
    echo "   FAIL: docs/figures 不该在"
    fail=1
  else
    echo "   OK   docs/figures 不在"
  fi
}

# ---- C 段：词的共现 ----
check_c() {
  local has_todo_section=0
  local has_session_line=0
  local has_tmp_keyword=0

  # docs/TODO.md 里有「## 已办」
  if [ -f "$target/docs/TODO.md" ]; then
    if grep -q '## 已办' "$target/docs/TODO.md" 2>/dev/null; then
      has_todo_section=1
    fi
  fi

  if [ "$has_todo_section" -eq 0 ]; then
    echo "   FAIL: docs/TODO.md 里没有「## 已办」"
    fail=1
  fi

  # docs/SESSION.md 里有「---」
  if [ -f "$target/docs/SESSION.md" ]; then
    if grep -q '^---$' "$target/docs/SESSION.md" 2>/dev/null; then
      has_session_line=1
    fi
  fi

  if [ "$has_session_line" -eq 0 ]; then
    echo "   FAIL: docs/SESSION.md 里没有「---」"
    fail=1
  fi

  # .tmp/README.md 里含「零权威」
  if [ -f "$target/.tmp/README.md" ]; then
    if grep -q '零权威' "$target/.tmp/README.md" 2>/dev/null; then
      has_tmp_keyword=1
    fi
  fi

  if [ "$has_tmp_keyword" -eq 0 ]; then
    echo "   FAIL: .tmp/README.md 里没有「零权威」"
    fail=1
  fi

  if [ "$has_todo_section" -eq 1 ] && [ "$has_session_line" -eq 1 ] && [ "$has_tmp_keyword" -eq 1 ]; then
    echo "   OK   三个词的共现都在"
  fi
}

# ---- D 段：七样不许在 ----
check_d() {
  local bad_items=(
    "research"
    "docs/README.md"
    "utils"
    "papers"
    "codes"
    "docs/design/figures"
    "docs/reports/figures"
  )

  local found=0
  for item in "${bad_items[@]}"; do
    if [ -e "$target/$item" ]; then
      echo "   FAIL: $item 不该在"
      found=1
    fi
  done

  if [ "$found" -eq 0 ]; then
    echo "   OK   七样都不在"
  else
    fail=1
  fi
}

# ---- E 段：幂等（只在自造那一路）----
check_e() {
  if [ "$create_tree" = false ]; then
    echo "   （幂等跳过：扫描模式不修改靶子——点名幂等且跳过）"
    return
  fi

  # 第一趟的 cksum
  local cksum1=""
  if [ -d "$target" ]; then
    cksum1=$(find "$target" -type f -exec cksum {} \; | sort)
  fi

  # 第二趟 init（--force --non-interactive）
  python -B docs_meta/src/init.py "$target" --force --non-interactive >/dev/null 2>&1

  # 检查末行
  local init_output=$(python -B docs_meta/src/init.py "$target" --force --non-interactive 2>/dev/null)
  local last_line=$(printf '%s\n' "$init_output" | tail -1)

  if ! printf '%s' "$last_line" | grep -qF '建 0 件，跳过 30 件，覆盖 0 件'; then
    echo "   FAIL: 第二趟末行不对：$last_line"
    fail=1
    return
  fi

  # 第二趟的 cksum
  local cksum2=""
  if [ -d "$target" ]; then
    cksum2=$(find "$target" -type f -exec cksum {} \; | sort)
  fi

  if [ "$cksum1" = "$cksum2" ]; then
    echo "   OK   幂等：整树逐份 cksum 相同"
  else
    echo "   FAIL: 幂等破了：cksum 不同"
    fail=1
  fi
}

# ---- F 段：占位符替换和出处指针验证 ----
check_f() {
  # F1：靶子里 {{DOSSIER_SRC}} 0 处
  local f1_count=$(grep -rlF '{{DOSSIER_SRC}}' "$target" 2>/dev/null | wc -l)
  if [ "$f1_count" -ne 0 ]; then
    echo "   FAIL: F1 靶子里还有 {{DOSSIER_SRC}}，共 $f1_count 处"
    fail=1
  else
    echo "   OK   F1 {{DOSSIER_SRC}} 0 处"
  fi

  # F2：从 CLAUDE.md 里抓出出处指针，验证 directory.md 存在且是文件
  if [ ! -f "$target/CLAUDE.md" ]; then
    echo "   FAIL: F2 靶子里没有 CLAUDE.md"
    fail=1
    return
  fi

  # 从 CLAUDE.md 里抓出相对路径（出处指针）
  # 形式：母本布局 ../.../.../docs_meta/src，真宿主布局 <子模块名>/docs_meta/src
  # 都以反引号或空格为分隔符
  local relpath=$(grep -oE '[^[:space:]`]*docs_meta/src' "$target/CLAUDE.md" | head -1)

  if [ -z "$relpath" ]; then
    echo "   FAIL: F2 从 CLAUDE.md 里没抓到出处指针"
    fail=1
    return
  fi

  # 检查 $target/$relpath/directory.md 是否存在且是文件
  local dirfile="$target/$relpath/directory.md"
  if [ ! -f "$dirfile" ]; then
    echo "   FAIL: F2 出处指针指向的 directory.md 不存在或非文件：$dirfile"
    fail=1
  else
    echo "   OK   F2 出处指针指向的 directory.md 存在且是文件"
  fi
}

# ---- 主检查流程 ----
echo "== A 22 件逐件在 =="
check_a
echo

echo "== B docs/figures/ 不许在 =="
check_b
echo

echo "== C 三份占位的结构还在 =="
check_c
echo

echo "== D 不该预建的那七样一个都不许在 =="
check_d
echo

echo "== E 幂等 =="
check_e
echo

echo "== F 占位符替换和出处指针 =="
check_f
echo

if [ "$fail" -eq 0 ]; then
  echo "ALL PASS"
else
  echo "FAILED"
fi

exit "$fail"
