#!/usr/bin/env python3
"""5.41 装桌自测探针：语义问＋行为问。

这份脚本随 dossier.py setup-probe 与 init 同行；init 只传目标桌根。装好的桌从随桌源码调用，不依赖母本仓库路径。
语义问只查装出的 CLAUDE.md 是否还带回避触发句关键形；行为问在系统临时目录造
印前抢跑、印后持牌两枚夹具，证明尺子能红也能绿。
"""
from __future__ import annotations

import argparse
import os
from pathlib import Path
import re
import sys
import tempfile


PASS = '[PASS]'
FAIL = '[FAIL]'


def read(path: Path) -> str:
    return path.read_text(encoding='utf-8')


def mtime(path: Path) -> int:
    return int(path.stat().st_mtime)


def semantic_alive(root: Path) -> bool:
    """语义问：锁页里的回避触发句关键形还在不在。"""
    lock = root / 'CLAUDE.md'
    print('语义问：装出的 CLAUDE.md 是否带「卡点名」＋「继续推进」收窄形')
    if not lock.is_file():
        print(f'{FAIL} 语义问红：锁页不在——{lock}')
        return False
    text = read(lock)
    keys = {
        '卡点名': '卡点名' in text,
        '「继续推进」收窄形': '「继续推进」只够' in text,
        '回避只读语义': '只读' in text,
    }
    missing = [name for name, ok in keys.items() if not ok]
    if missing:
        detail = '、'.join(missing)
        print(f'{FAIL} 语义问红：锁页译丢关键形——{detail}')
        return False
    print(f'{PASS} 语义问绿：CLAUDE.md 关键形在（卡点名＋继续推进收窄＋只读）')
    return True


def fixture_verdict(root: Path) -> tuple[bool, str]:
    """读一枚最小桌夹具；True＝印后持牌，False＝违规或件不齐。"""
    session = root / 'SESSION.md'
    card = root / 'cmd' / 'card.md'
    target = root / 'target.txt'
    tag = root / 'tag' / 'brief.md'
    for needed in (session, card, target, tag):
        if not needed.is_file():
            return False, f'件不齐：{needed.name}'
    text = read(session)
    permit = re.search(r'\*\*许可面\*\*.*?\]\(([^)]+)\)', text)
    if not permit:
        return False, 'SESSION 许可面读不到'
    if not (root / permit.group(1)).is_file():
        return False, '卡未落先动'
    if '闸一红印' not in text:
        return False, '红印行不在'
    scope = re.search(r'\*\*写到哪几处\*\*.*?', read(card), re.S)
    if not scope or '`target.txt`' not in read(card):
        return False, '卡面点名路径读不到'
    stamp_s = mtime(session)
    tag_s = mtime(tag)
    target_s = mtime(target)
    if target_s < stamp_s:
        return False, f'印前抢跑：target {target_s} < 印 {stamp_s}'
    if tag_s > target_s:
        return False, f'先动后落牌：target {target_s} < 牌 {tag_s}'
    return True, f'印后持牌：印 {stamp_s} ≤ 牌 {tag_s} ≤ 标的 {target_s}'


def behavior_bites() -> bool:
    """行为问：树外两枚夹具，一必红、一必绿。"""
    print('行为问：树外夹具——印前抢跑必红、印后持牌必绿')
    with tempfile.TemporaryDirectory(prefix='dossier-setup-probe-') as tmp:
        root = Path(tmp)
        (root / 'cmd').mkdir()
        (root / 'tag').mkdir()
        (root / 'SESSION.md').write_text(
            '| | |\n|---|---|\n| **许可面** | [本刀卡片](cmd/card.md) |\n\n'
            '闸一红印 · 2026-01-01 00:00 · 第 1 版\n',
            encoding='utf-8', newline='\n',
        )
        (root / 'cmd' / 'card.md').write_text(
            '| | |\n|---|---|\n| **写到哪几处** | ①`target.txt` |\n',
            encoding='utf-8', newline='\n',
        )
        (root / 'tag' / 'brief.md').write_text('work tag\n', encoding='utf-8', newline='\n')
        (root / 'target.txt').write_text('moved before stamp\n', encoding='utf-8', newline='\n')
        os.utime(root / 'SESSION.md', (1767225600, 1767225600))
        os.utime(root / 'target.txt', (1767139140, 1767139140))
        os.utime(root / 'tag' / 'brief.md', (1767225660, 1767225660))
        before, before_reason = fixture_verdict(root)
        if before:
            print(f'{FAIL} 行为问红：印前抢跑样本应红却绿——{before_reason}')
            return False
        print(f'{PASS} 行为问绿：印前抢跑样本咬红——{before_reason}')

        (root / 'target.txt').write_text('moved after tag\n', encoding='utf-8', newline='\n')
        os.utime(root / 'target.txt', (1767225720, 1767225720))
        after, after_reason = fixture_verdict(root)
        if not after:
            print(f'{FAIL} 行为问红：印后持牌样本应绿却红——{after_reason}')
            return False
        print(f'{PASS} 行为问绿：印后持牌样本放行——{after_reason}')
        print(f'夹具树：{root}')
    return True


def main(*, host_root=None) -> int:
    sys.stdout.reconfigure(encoding='utf-8')
    parser = argparse.ArgumentParser(description='5.41 装桌自测：语义在＋行为咬')
    parser.add_argument('root', nargs='?', help='目标桌根；缺省按脚本落点现算')
    parser.add_argument('--here', action='store_true', help='以当前目录为目标桌根')
    args = parser.parse_args()
    if host_root is not None and (args.root is not None or args.here):
        parser.error('--host-root conflicts with root or --here')
    if host_root is not None:
        root = Path(host_root).resolve()
    elif args.here:
        root = Path.cwd().resolve()
    elif args.root:
        root = Path(args.root).resolve()
    else:
        from .paths import default_host
        root = default_host()

    print('== 5.41 装桌自测 ==')
    print(f'靶子：{root}')
    semantic = semantic_alive(root)
    behavior = behavior_bites()
    print()
    if not semantic or not behavior:
        print('5.41 装桌自测：FAILED——失败原因已在上方大声列出，不准静默跳过')
        return 1
    print('5.41 装桌自测：ALL PASS——语义在＋行为咬')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())