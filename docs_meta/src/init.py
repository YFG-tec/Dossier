#!/usr/bin/env python3
"""
运行时契约：Python >= 3.13（3.12 兼容模式可用；解释器优先项目内 `.venv`，未建则系统，首次需要时建——5.32）＋ Git Bash（Windows）。详见 docs_meta/tests/check-env.sh。
"""
import sys
import os
import pathlib
import subprocess
from pathlib import PurePath


DOSSIER_SRC_PLACEHOLDER = '{{DOSSIER_SRC}}'
SETUP_PROBE_SOURCE = pathlib.Path(__file__).resolve().with_name('setup_probe.py')


def get_repo_root():
    """计算仓库根"""
    script_file = pathlib.Path(__file__).resolve()
    # docs_meta/src/init.py -> docs_meta/src -> docs_meta -> 仓库根
    return script_file.parent.parent.parent


def get_default_target():
    """计算默认靶子：仓库根的父目录"""
    # 靶子 = 仓库根的父目录
    return get_repo_root().parent


def main():
    # 配置输出编码
    sys.stdout.reconfigure(encoding='utf-8')

    # 解析参数
    args = sys.argv[1:]

    target_path = None
    use_here = False
    force = False
    non_interactive = False
    dry_run = False
    skip_self_test = False
    help_requested = False

    for arg in args:
        if arg == '--help':
            help_requested = True
        elif arg == '--here':
            use_here = True
        elif arg == '--force':
            force = True
        elif arg == '--non-interactive':
            non_interactive = True
        elif arg == '--dry-run':
            dry_run = True
        elif arg == '--skip-self-test':
            skip_self_test = True
        elif not arg.startswith('--'):
            if target_path is None:
                target_path = arg

    # 处理 --help
    if help_requested:
        print('python docs_meta/src/init.py [TARGET] [--here] [--force] [--non-interactive] [--dry-run]')
        sys.exit(0)

    # 检查参数冲突：TARGET 和 --here 同时给
    if target_path is not None and use_here:
        sys.exit(2)

    # 确定靶子
    if use_here:
        target = pathlib.Path.cwd().resolve()
    elif target_path is not None:
        target = pathlib.Path(target_path).resolve()
    else:
        target = get_default_target()

    # 检查靶子存在性和可写性
    if not target.exists() or not os.access(target, os.W_OK):
        sys.exit(3)

    # 定义要铺的项目和内容
    structure = [
        ('docs', None),
        ('docs/TODO.md', '# 待办\n\n（空。还没有一行。）\n\n## 已办\n\n（空。）\n'),
        ('docs/SESSION.md', '# 本刀运行态\n\n（空。还没点行。）\n\n---\n\n## 横线以下 · 审阅\n\n（空。）\n'),
        # 装桌检查单（5.20，PROMPT_083 裁定 5）：起步闸与首刀自检的入口页
        ('docs/SETUP.md', '# 装桌检查单\n\n装桌五步，依次勾：\n\n1. `git submodule update --remote`\n2. `python docs_meta/src/init.py` 铺桌\n3. 起步闸：`bash docs_meta/tests/check-env.sh` 的 E 段绿才开\n4. 首刀前：`bash docs_meta/tests/run.sh` 红绿自检\n5. 转译基线回执（见 5.30 刀）\n'),
        ('docs/cmd', None),
        ('docs/cmd/.gitkeep', ''),
        ('docs/design', None),
        ('docs/design/.gitkeep', ''),
        ('docs/reports', None),
        ('docs/reports/.gitkeep', ''),
        ('.tmp', None),
        ('.tmp/README.md', '草稿。零权威，不准自称通过。\n'),
    ]

    # 执行铺装
    created_count = 0
    skipped_count = 0
    overwritten_count = 0

    print(f'靶子：{target}')

    for path_str, content in structure:
        full_path = target / path_str
        is_dir = content is None

        if is_dir:
            # 处理目录
            if full_path.exists():
                print(f'= {path_str}/')
                skipped_count += 1
            else:
                if not dry_run:
                    full_path.mkdir(parents=True, exist_ok=True)
                print(f'+ {path_str}/')
                created_count += 1
        else:
            # 处理文件
            if full_path.exists():
                # 文件已存在，检查 --force 逻辑
                if force and not non_interactive:
                    # 先问一句，默认否
                    response = input(f'覆盖 {path_str} ？[n] ')
                    if response.lower() == 'y':
                        if not dry_run:
                            full_path.parent.mkdir(parents=True, exist_ok=True)
                            if path_str.endswith('.gitkeep'):
                                full_path.write_bytes(b'')
                            else:
                                full_path.write_text(content, encoding='utf-8', newline='\n')
                        print(f'+ {path_str}')
                        overwritten_count += 1
                    else:
                        print(f'= {path_str}')
                        skipped_count += 1
                else:
                    # 默认或 --non-interactive：不覆盖
                    print(f'= {path_str}')
                    skipped_count += 1
            else:
                # 文件不存在，创建
                if not dry_run:
                    full_path.parent.mkdir(parents=True, exist_ok=True)
                    if path_str.endswith('.gitkeep'):
                        full_path.write_bytes(b'')
                    else:
                        full_path.write_text(content, encoding='utf-8', newline='\n')
                print(f'+ {path_str}')
                created_count += 1

    # 处理 .mirror/ 那一棵
    repo_root = get_repo_root()
    mirror_root = repo_root / '.mirror'
    src_dir = repo_root / 'docs_meta' / 'src'

    # 检查 .mirror/ 是否存在
    if not mirror_root.exists():
        print(f'.mirror/ 不在仓库根，退出', file=sys.stderr)
        sys.exit(5)

    # 现算 DOSSIER_SRC：同盘落相对路径；跨盘降级为绝对路径，不中断装桌。
    try:
        relative_path = os.path.relpath(src_dir, target)
        relative_path_posix = PurePath(relative_path).as_posix()
    except ValueError:
        relative_path_posix = src_dir.resolve().as_posix()
        print('\033[33m跨盘装桌：DOSSIER_SRC 落绝对路径\033[0m')

    # 遍历 .mirror/ 下的所有文件和目录
    for item in sorted(mirror_root.rglob('*')):
        rel_item_path = item.relative_to(mirror_root)
        is_dir = item.is_dir()

        if is_dir:
            # 处理目录
            target_item = target / rel_item_path
            if target_item.exists():
                print(f'= {rel_item_path.as_posix()}/')
                skipped_count += 1
            else:
                if not dry_run:
                    target_item.mkdir(parents=True, exist_ok=True)
                print(f'+ {rel_item_path.as_posix()}/')
                created_count += 1
        else:
            # 处理文件
            target_item = target / rel_item_path

            # 读取文件内容
            file_content = item.read_text(encoding='utf-8')
            # 替换占位符
            file_content = file_content.replace(DOSSIER_SRC_PLACEHOLDER, relative_path_posix)

            if target_item.exists():
                # 文件已存在，检查 --force 逻辑
                if force and not non_interactive:
                    # 先问一句，默认否
                    response = input(f'覆盖 {rel_item_path.as_posix()} ？[n] ')
                    if response.lower() == 'y':
                        if not dry_run:
                            target_item.parent.mkdir(parents=True, exist_ok=True)
                            target_item.write_text(file_content, encoding='utf-8', newline='\n')
                        print(f'+ {rel_item_path.as_posix()}')
                        overwritten_count += 1
                    else:
                        print(f'= {rel_item_path.as_posix()}')
                        skipped_count += 1
                else:
                    # 默认或 --non-interactive：不覆盖
                    print(f'= {rel_item_path.as_posix()}')
                    skipped_count += 1
            else:
                # 文件不存在，创建
                if not dry_run:
                    target_item.parent.mkdir(parents=True, exist_ok=True)
                    target_item.write_text(file_content, encoding='utf-8', newline='\n')
                print(f'+ {rel_item_path.as_posix()}')
                created_count += 1

    # 5.41 装桌自测：探针随 docs_meta/src/ 走；默认跑，显式开关才跳过。
    if skip_self_test:
        print('= 5.41 装桌自测：按开关跳过（跳过不是绿）')
    elif dry_run:
        print('= 5.41 装桌自测：dry-run 未铺锁页，不跑')
    else:
        probe = subprocess.run(
            [sys.executable, str(SETUP_PROBE_SOURCE), str(target)],
        )
        if probe.returncode != 0:
            print('装桌自测失败：init 不给绿，见上方红读数', file=sys.stderr)
            sys.exit(6)
    # 特殊输出：--force --non-interactive
    if force and non_interactive:
        print('按默认否')

    # 末行
    print(f'建 {created_count} 件，跳过 {skipped_count} 件，覆盖 {overwritten_count} 件')

    sys.exit(0)


if __name__ == '__main__':
    main()
