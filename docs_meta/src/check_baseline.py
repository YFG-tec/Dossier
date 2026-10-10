#!/usr/bin/env python3
"""5.30 随桌比对入口：一条命令重算现哈希对基线。

这份脚本随 docs_meta/src/ 与 init 同行；装好的桌从随桌源码调用，不依赖母本仓库路径。
尺子只报事实：基线清单内的件逐件报「同／偏／缺」，偏则大声红、退码非 0；
桌侧后来长出的件（todo、卡、报告）不在此尺——量的是转译漂移，不是桌在长大。
--refresh 供人故意重译后重落基线（记新时戳与母本 HEAD）；基线是读数，重译还是回滚归人。
"""
from __future__ import annotations

import argparse
import json
import pathlib
import sys

import init

PASS = '[PASS]'
FAIL = '[FAIL]'
RED = '\033[31m'
RESET = '\033[0m'


def load_baseline(target):
    """读基线；不在或读不成，明红返回 None。"""
    path = target / pathlib.Path(init.BASELINE_RELATIVE_PATH)
    if not path.is_file():
        print(f'{FAIL} 基线不在——{path}；先跑 init 落基线', file=sys.stderr)
        return None
    try:
        baseline = json.loads(path.read_text(encoding='utf-8'))
    except (OSError, json.JSONDecodeError) as exc:
        print(f'{FAIL} 基线读不成——{exc}', file=sys.stderr)
        return None
    if not isinstance(baseline.get('files'), dict):
        print(f'{FAIL} 基线缺 files 读数——先 --refresh 重落', file=sys.stderr)
        return None
    return baseline


def main() -> int:
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

    parser = argparse.ArgumentParser(description='5.30 转译基线比对：重算现哈希对基线，只报事实不判合法性')
    parser.add_argument('target', nargs='?', help='目标桌根；缺省与 init 同口径（仓库根的父目录）')
    parser.add_argument('--here', action='store_true', help='以当前目录为目标桌根')
    parser.add_argument('--refresh', action='store_true', help='重落基线：记新时戳与母本 HEAD，供人故意重译后用')
    args = parser.parse_args()

    if args.here:
        target = pathlib.Path.cwd().resolve()
    elif args.target:
        target = pathlib.Path(args.target).resolve()
    else:
        target = init.get_default_target()

    repo_root = init.get_repo_root()

    print('== 5.30 转译基线比对 ==')
    print(f'靶子：{target}')

    if args.refresh:
        # 重落前先对清单点名：缺件说明桌没铺齐，先红，不许拍缩水基线。
        missing = [rel for rel in init.collect_manifest(repo_root) if not (target / pathlib.Path(rel)).is_file()]
        if missing:
            for rel in missing:
                print(f'{FAIL} 缺 {rel}——桌没铺齐，先重跑 init，不许落缩水基线', file=sys.stderr)
            return 1
        baseline = init.write_baseline(target, repo_root)
        if baseline is None:
            return 1
        print(f"基线重落：{len(baseline['files'])} 件（时戳 {baseline['generated_at']}，母本 HEAD {baseline['parent_head'][:12]}）")
        return 0

    baseline = load_baseline(target)
    if baseline is None:
        return 1

    same_count = 0
    drift_count = 0
    absent_count = 0
    for rel in sorted(baseline['files']):
        expected = baseline['files'][rel]
        full = target / pathlib.Path(rel)
        if not full.is_file():
            absent_count += 1
            print(f'{FAIL} 缺 {rel}')
            continue
        actual = init.blob_sha1(full)
        if actual == expected:
            same_count += 1
            print(f'{PASS} 同 {rel}')
        else:
            drift_count += 1
            print(f'{FAIL} 偏 {rel}——基线 {expected[:12]}，现算 {actual[:12]}')

    print()
    if drift_count or absent_count:
        print(f'{RED}基线比对 FAILED——{same_count} 同、{drift_count} 偏、{absent_count} 缺；偏了是读数，重译还是回滚归人{RESET}', file=sys.stderr)
        return 1
    print(f'基线比对 ALL PASS——{same_count} 件全同（只报事实，此绿不判合法性）')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())