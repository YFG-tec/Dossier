#!/usr/bin/env bash

# 5.40 的印窗／持牌自检。零权威，只作证，不算「通过」。
# 用法：bash docs_meta/tests/check-recusal.sh    夹具自证＋活刀读数
#
# 谁加的：2026-10-09 由 cmd/PROMPT_095.md 新增，建造手按工牌写入。
# 被检对象只有 workflow.md:413-414 那两句：印窗零变更（回避）、印后持牌。
# 印时点读 SESSION 文件 mtime（PROMPT_095 裁定 1 明写：保守向红）。
#
# 这一本查不到什么，先写明：
#   - mtime 证「什么时候动」，证不了「哪只手动的」，也证不了工牌内容是否被读；
#   - 工牌只取盘上 brief.md 的落盘时序作牌证，不把 .tmp/ 抬成权威；
#   - 活刀态三件（SESSION 许可面＋红印行、卡面写到哪几处、点名路径）读不齐时 SKIP 不猜。
#
# 探针红线：夹具一律用 mktemp -d 落在树外，本脚本不写仓库 .tmp/。
# find/sort 固定走 /usr/bin：Windows 系统也有同名 find.exe、sort.exe，非登录壳一撞名就假空或带 CR。
set -u

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd -P)"
fail=0

pass() { printf '[PASS] %s\n' "$1"; }
skip() { printf '[SKIP] %s\n' "$1"; }
red()  { printf '[FAIL] %s\n' "$1"; fail=1; }

mtime_of() {
    stat -c '%Y' "$1" 2>/dev/null || :
}

# 读一份 SESSION 指到的卡；三件不齐时由调用侧决定 SKIP 还是红。
read_permit() {
    local session=$1
    local permit_line permit=''
    permit_line=$(awk -F'|' '/\*\*许可面\*\*/ {print $3; exit}' "$session" 2>/dev/null)
    permit=$(printf '%s\n' "$permit_line" | sed -n 's/.*](\([^)]*\)).*/\1/p')
    printf '%s' "$permit"
}

read_scope_row() {
    local card=$1
    awk -F'|' '/\*\*写到哪几处\*\*/ {gsub(/^ +| +$/, "", $3); print $3; exit}' "$card" 2>/dev/null
}

# 卡面可用裸文件名点名（如 make_frame.py）。只有在 docs_meta/ 下唯一命中才解析；
# 多命中、零命中都不猜，按点名原样读。
resolve_named() {
    local base=$1 raw=$2 resolved=''
    if [[ "$raw" == */* ]]; then
        printf '%s' "$raw"
        return
    fi
    if [[ -e "$base/$raw" ]]; then
        printf '%s' "$raw"
        return
    fi
    resolved=$(/usr/bin/find "$base/docs_meta" -type f -name "$raw" 2>/dev/null | LC_ALL=C /usr/bin/sort)
    if [[ "$(printf '%s\n' "$resolved" | sed '/^$/d' | wc -l)" -eq 1 ]]; then
        resolved=${resolved#"$base/"}
        printf '%s' "$resolved"
    else
        printf '%s' "$raw"
    fi
}

# mode=fixture：缺件就是红，用来证明尺子能红。
# mode=active：三件读不齐按卡裁定 SKIP，不猜。
# 返回码：0＝全绿／SKIP；1＝有红。
inspect() {
    local base=$1 label=$2 mode=$3
    local session="$base/SESSION.md"
    if [[ "$mode" == active ]]; then session="$base/docs_meta/docs/SESSION.md"; fi

    if [[ ! -f "$session" ]]; then
        if [[ "$mode" == active ]]; then skip "$label：SESSION.md 不在，三件读不齐"; return 0; fi
        printf '[FAIL] %s：SESSION.md 不在\n' "$label"; return 1
    fi

    local permit
    permit=$(read_permit "$session")
    local card="$base/$permit"
    if [[ "$mode" == active ]]; then card="$(dirname "$session")/$permit"; fi
    if [[ -z "$permit" || ! -f "$card" ]]; then
        if [[ "$mode" == active ]]; then skip "$label：许可面读不到（permit=$permit），三件读不齐"; return 0; fi
        printf '[FAIL] %s：卡未落先动——SESSION 许可面读得到，卡不在\n' "$label"; return 1
    fi

    local stamp_line
    stamp_line=$(grep -m1 '闸一红印' "$session" 2>/dev/null || true)
    if [[ -z "$stamp_line" ]]; then
        if [[ "$mode" == active ]]; then skip "$label：红印行不在，三件读不齐"; return 0; fi
        printf '[FAIL] %s：红印行不在\n' "$label"; return 1
    fi

    local scope
    scope=$(read_scope_row "$card")
    if [[ -z "$scope" ]]; then
        if [[ "$mode" == active ]]; then skip "$label：卡面「写到哪几处」读不到，三件读不齐"; return 0; fi
        printf '[FAIL] %s：卡面「写到哪几处」读不到\n' "$label"; return 1
    fi

    local stamp_s
    stamp_s=$(mtime_of "$session")
    if [[ -z "$stamp_s" ]]; then
        if [[ "$mode" == active ]]; then skip "$label：SESSION mtime 读不到，三件读不齐"; return 0; fi
        printf '[FAIL] %s：SESSION mtime 读不到\n' "$label"; return 1
    fi

    local paths=() raw p
    while IFS= read -r raw; do
        [[ -z "$raw" ]] && continue
        p=$(resolve_named "$base" "$raw")
        paths+=("$p")
    done < <(printf '%s\n' "$scope" | grep -oE '`[^`]+`' | sed -e 's/^`//' -e 's/`$//')

    if (( ${#paths[@]} == 0 )); then
        if [[ "$mode" == active ]]; then skip "$label：卡面点名路径读不到，三件读不齐"; return 0; fi
        printf '[FAIL] %s：卡面点名路径读不到\n' "$label"; return 1
    fi

    # 牌证：活刀读仓库 .tmp/<刀>/*/brief.md；夹具读 tag/brief.md。
    # 只认「印时点 ≤ 牌落盘 ≤ 标的落盘」这一条时序链。
    local tag='' tag_s='' candidate ts point_line cut=''
    point_line=$(awk -F'|' '/\*\*点的行\*\*/ {print $3; exit}' "$session" 2>/dev/null)
    [[ "$point_line" =~ ([0-9]+\.[0-9]+) ]] && cut=${BASH_REMATCH[1]}
    while IFS= read -r candidate; do
        [[ -z "$candidate" ]] && continue
        ts=$(mtime_of "$candidate")
        [[ -z "$ts" ]] && continue
        if (( ts >= stamp_s )); then tag=$candidate; tag_s=$ts; break; fi
    done < <(
        if [[ "$mode" == fixture ]]; then
            printf '%s\n' "$base/tag/brief.md"
        elif [[ -n "$cut" ]]; then
            /usr/bin/find "$base/.tmp/$cut" -type f -path '*/brief.md' 2>/dev/null | LC_ALL=C /usr/bin/sort
        fi
    )
    if [[ -z "$tag" ]]; then
        if [[ "$mode" == active ]]; then
            skip "$label：印后牌证读不到（工牌不在，或早于印时点），不猜"
            return 0
        fi
        printf '[FAIL] %s：印后无牌证（工牌／夹具牌不在，或早于印时点）\n' "$label"
        return 1
    fi

    printf '   %s：卡=%s；印=%s；牌=%s\n' "$label" "$permit" "$stamp_s" "$tag"
    local local_bad=0 target target_s
    for target in "${paths[@]}"; do
        case "$target" in
            /*|*..*) printf '[FAIL] %s：点名路径不安全，读作红：%s\n' "$label" "$target"; local_bad=1; continue ;;
        esac
        if [[ ! -e "$base/$target" ]]; then
            if [[ "$mode" == active ]]; then
                skip "$label：点名路径不在盘，三件读不齐（$target）"
                return 0
            fi
            printf '[FAIL] %s：点名路径不在盘：%s\n' "$label" "$target"; local_bad=1; continue
        fi
        target_s=$(mtime_of "$base/$target")
        if [[ -z "$target_s" ]]; then
            if [[ "$mode" == active ]]; then
                skip "$label：点名路径 mtime 读不到，三件读不齐（$target）"
                return 0
            fi
            printf '[FAIL] %s：点名路径 mtime 读不到：%s\n' "$label" "$target"; local_bad=1; continue
        fi
        if (( target_s < stamp_s )); then
            printf '[FAIL] %s：印前动＝红：%s mtime %s < 印 %s\n' "$label" "$target" "$target_s" "$stamp_s"
            local_bad=1
        elif (( tag_s > target_s )); then
            printf '[FAIL] %s：先动后落牌＝红：%s mtime %s < 牌 %s\n' "$label" "$target" "$target_s" "$tag_s"
            local_bad=1
        else
            printf '[PASS] %s：印后持牌动＝绿：%s mtime %s ≥ 印 %s／牌 %s\n' "$label" "$target" "$target_s" "$stamp_s" "$tag_s"
        fi
    done
    return "$local_bad"
}

# ---- 夹具态：树外三例，两红一绿 ----
fixture_root=$(mktemp -d "${TMPDIR:-/tmp}/dossier-recusal.XXXXXXXX")
cleanup() { rm -rf "$fixture_root"; }
trap cleanup EXIT INT TERM

printf '== 夹具态（树外 mktemp，不写仓库 .tmp/） ==\n'
printf '夹具树：%s\n\n' "$fixture_root"

# 例一：卡、印都在，标的早于印——印前抢跑，应红。
mkdir -p "$fixture_root/cmd" "$fixture_root/tag"
printf '| | |\n|---|---|\n| **许可面** | [本刀卡片](cmd/card.md) |\n| **点的行** | `todo.md` `9.99` |\n' > "$fixture_root/SESSION.md"
printf '\n闸一红印 · 2026-01-01 00:00 · 第 1 版\n' >> "$fixture_root/SESSION.md"
printf '| | |\n|---|---|\n| **写到哪几处** | ①`target.txt` |\n' > "$fixture_root/cmd/card.md"
printf 'moved before stamp\n' > "$fixture_root/target.txt"
printf 'work tag\n' > "$fixture_root/tag/brief.md"
touch -t 202601010000 "$fixture_root/SESSION.md"
touch -t 202512312359 "$fixture_root/target.txt"
touch -t 202601010001 "$fixture_root/tag/brief.md"
if (inspect "$fixture_root" '夹具A' fixture); then
    red '夹具A应红却绿：印前动没抓住'
else
    pass '夹具A期望红：印前动'
fi
printf '\n'

# 例二：牌在印后、标的在牌后——印后持牌施工，应绿。
printf 'moved after tag\n' > "$fixture_root/target.txt"
touch -t 202601010002 "$fixture_root/target.txt"
if (inspect "$fixture_root" '夹具B' fixture); then
    pass '夹具B期望绿：印后持牌动'
else
    red '夹具B应绿却红：印后施工被误伤'
fi
printf '\n'

# 例三：许可面指着卡，卡不在——卡未落先动，应红。
rm "$fixture_root/cmd/card.md"
if (inspect "$fixture_root" '夹具C' fixture); then
    red '夹具C应红却绿：卡未落先动没抓住'
else
    pass '夹具C期望红：卡未落先动'
fi

# ---- 活刀态：只读现树；三件不齐 SKIP ----
printf '\n== 活刀态（SESSION 在办刀） ==\n'
inspect "$ROOT" '活刀' active || fail=1

printf '\n'
if (( fail == 0 )); then
    printf 'ALL PASS\n'
else
    printf 'FAILED\n'
fi
exit "$fail"
