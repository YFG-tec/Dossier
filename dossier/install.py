#!/usr/bin/env python3
"""
运行时契约：Python >= 3.13（3.12 兼容模式可用；解释器优先项目内 `.venv`，未建则系统，首次需要时建——5.32）＋ Git Bash（Windows）。详见 checks/check-env.sh。
"""
import hashlib
import json
import os
import pathlib
import subprocess
import sys

from datetime import datetime
from pathlib import PurePath


DOSSIER_ROOT_PLACEHOLDER = '{{DOSSIER_ROOT}}'

def render(content, source_prefix):
    """Render a template at its selected source location (shared by upgrades)."""
    return content.replace(DOSSIER_ROOT_PLACEHOLDER, source_prefix)
SETUP_PROBE_SOURCE = pathlib.Path(__file__).resolve().with_name('setup_probe.py')
BASELINE_RELATIVE_PATH = '.dossier/baseline.json'
BASELINE_HASH_ALGORITHM = 'git-blob-sha1'


def get_repo_root():
    """计算仓库根"""
    from .paths import SOURCE_ROOT
    return SOURCE_ROOT


def get_default_target():
    """计算默认靶子：submodules依赖的宿主，否则本框架根"""
    # 不从新框架目录无参操作外层旧桌
    from .paths import default_host
    return default_host()


def build_structure():
    """装桌骨架清单。5.30 起与 dossier.py baseline 共用一份——清单只写这里，不落第二真相。"""
    return [
        ('docs', None),
        ('docs/TODO.md', '# 待办\n\n（空。还没有一行。）\n'),
        ('docs/archives', None),
        ('docs/archives/README.md', '档案目录，只增不删。\n'),
        ('docs/SESSION.md', '# 本刀运行态\n\n（空。还没点行。）\n\n---\n\n## 横线以下 · 审阅\n\n（空。）\n'),
        # 装桌检查单（5.20，PROMPT_083 裁定 5）：起步闸与首刀自检的入口页
        ('docs/SETUP.md', '# 装桌检查单\n\n装桌五步，依次勾：\n\n1. 固定恢复：`git submodule update --init -- submodules/dossier`（不选新版）\n2. 首次从可信正式 tag 文件或 Release 附件取得 bootstrap.py：`python bootstrap.py --repository URL --host-root .`；显式版本加 `--version TAG_OR_COMMIT`\n3. 起步闸：`bash {{DOSSIER_ROOT}}/checks/check-env.sh --host-root .` 的 E 段绿才开\n4. 升级先 `python {{DOSSIER_ROOT}}/dossier.py factory plan --repository URL --host-root . > upgrade.json`，审阅后 `python {{DOSSIER_ROOT}}/dossier.py factory apply --plan upgrade.json --host-root .`；factory status/rollback 查看或回退\n5. 转译基线回执：`python {{DOSSIER_ROOT}}/dossier.py baseline --here`（偏则红；refresh 只重记读数，不是升级）。成品只附 env 检查，开发检查不随包交付。\n'),
        ('docs/cmd', None),
        ('docs/cmd/.gitkeep', ''),
        ('docs/design', None),
        ('docs/design/.gitkeep', ''),
        ('docs/reports', None),
        ('docs/reports/.gitkeep', ''),
        ('.tmp', None),
        ('.tmp/README.md', '草稿。零权威，不准自称通过。\n'),
    ]


def blob_sha1(path):
    """git hash-object 同族一枚：blob 头＋原字节走 SHA-1（5.30 裁定 1）。"""
    data = pathlib.Path(path).read_bytes()
    header = f'blob {len(data)}\0'.encode('ascii')
    return hashlib.sha1(header + data).hexdigest()


def get_parent_head(repo_root):
    """现算母本 HEAD；取不到返回 None——基线必填读数，缺了明红不给伪空值。"""
    proc = subprocess.run(
        ['git', 'rev-parse', 'HEAD'],
        cwd=str(repo_root),
        capture_output=True,
        text=True,
        encoding='utf-8',
    )
    if proc.returncode != 0:
        return None
    return proc.stdout.strip()


def collect_manifest(repo_root):
    """装出全集清单：骨架文件＋templates/ 逐件；目录不进，.dossier/ 不进。"""
    paths = set()
    for path_str, content in build_structure():
        if content is not None:
            paths.add(PurePath(path_str).as_posix())
    mirror_root = repo_root / 'templates'
    for item in mirror_root.rglob('*'):
        if item.is_file():
            paths.add(item.relative_to(mirror_root).as_posix())
    return sorted(paths)


def write_baseline(target, repo_root, *, writer=None):
    """落桌侧转译基线：清单逐件内容哈希＋生成时戳＋母本 HEAD（5.30 裁定 1）。

    零权威，只作证：哈希记的是落盘时点的盘上实况，不判那份内容合不合法；
    偏了是读数，重译还是回滚归人。
    """
    head = get_parent_head(repo_root)
    if head is None:
        print('母本 HEAD 取不到：基线缺必填读数，不给落', file=sys.stderr)
        return None
    files = {}
    for rel in collect_manifest(repo_root):
        full = target / pathlib.Path(rel)
        if not full.is_file():
            print(f'基线清单缺件，不给落缩水基线——{rel}；先重跑 init 铺齐', file=sys.stderr)
            return None
        files[rel] = blob_sha1(full)
    baseline = {
        'version': 1,
        'generated_at': datetime.now().astimezone().isoformat(timespec='seconds'),
        'parent_head': head,
        'hash_algorithm': BASELINE_HASH_ALGORITHM,
        'files': files,
    }
    out = target / pathlib.Path(BASELINE_RELATIVE_PATH)
    out.parent.mkdir(parents=True, exist_ok=True)
    data = (json.dumps(baseline, ensure_ascii=False, indent=2, sort_keys=True) + '\n').encode('utf-8')
    if writer is None:
        out.write_bytes(data)
    else:
        writer(BASELINE_RELATIVE_PATH, data)
    return baseline


def main(*, host_root=None):
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
    mail_url = None
    mail_desk = None
    recommend_desk = False
    mail_book = None

    index = 0
    while index < len(args):
        arg = args[index]
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
        elif arg == '--with-mail':
            if index + 1 >= len(args):
                print('--with-mail 缺 <url>', file=sys.stderr)
                sys.exit(2)
            mail_url = args[index + 1]
            index += 1
        elif arg == '--desk':
            if index + 1 >= len(args):
                print('--desk 缺 <地址>', file=sys.stderr)
                sys.exit(2)
            mail_desk = args[index + 1]
            index += 1
        elif arg == '--recommend-desk':
            recommend_desk = True
        elif arg == '--mail-book':
            if index + 1 >= len(args) or args[index + 1].startswith('--'):
                print('--mail-book 缺 <只读簿路径>', file=sys.stderr)
                sys.exit(2)
            mail_book = args[index + 1]
            index += 1
        elif not arg.startswith('--'):
            if target_path is None:
                target_path = arg
        index += 1

    # 处理 --help
    if help_requested:
        print('python dossier.py init [TARGET] [--here] [--force] [--non-interactive] [--dry-run] [--with-mail <url> --desk <地址>] [--recommend-desk [--mail-book <只读簿路径>]]')
        print('--recommend-desk：仅交互且有 --with-mail 时显示候选；显式 --desk 优先。候选未占号，确认地址须人签簿。')
        sys.exit(0)

    if (mail_book is not None and not recommend_desk) or (recommend_desk and mail_url is None):
        print('--mail-book 只能伴 --recommend-desk；--recommend-desk 须伴 --with-mail', file=sys.stderr)
        sys.exit(2)
    use_recommendation = recommend_desk and mail_url is not None and mail_desk is None and not non_interactive
    if (mail_url is None) != (mail_desk is None) and not use_recommendation:
        print('--with-mail 与 --desk 必须同给同缺；不传旗零影响', file=sys.stderr)
        sys.exit(2)

    # 检查参数冲突：TARGET 和 --here 同时给
    if target_path is not None and use_here:
        sys.exit(2)

    # The install parser, rather than the launcher, knows which tokens are targets.
    if host_root is not None and (target_path is not None or use_here):
        print('--host-root conflicts with TARGET or --here', file=sys.stderr)
        sys.exit(2)

    # 确定靶子
    if host_root is not None:
        target = pathlib.Path(host_root).resolve()
    elif use_here:
        target = pathlib.Path.cwd().resolve()
    elif target_path is not None:
        target = pathlib.Path(target_path).resolve()
    else:
        target = get_default_target()

    # 检查靶子存在性和可写性
    if not target.exists() or not os.access(target, os.W_OK):
        sys.exit(3)

    # 推荐是显式选择的铺装前只读闸；不允许确认输入代签地址簿。
    if use_recommendation:
        from . import postman
        try:
            recommendation = postman.recommend_address(target, book=mail_book)
            print('邮箱默认候选：' + json.dumps(recommendation, ensure_ascii=False, sort_keys=True))
            if dry_run:
                print('= 推荐 dry-run：未安装，未占号；不读取确认输入')
                mail_desk = recommendation['address']
            else:
                try:
                    response = input('回车确认候选，或输入已签合法地址修改；cancel/q 取消：').strip()
                except EOFError:
                    print('邮箱推荐确认遇 EOF，取消铺装', file=sys.stderr)
                    sys.exit(2)
                if response.lower() in {'cancel', 'q', 'quit', '取消', 'n', 'no'}:
                    print('邮箱推荐已取消，未铺装', file=sys.stderr)
                    sys.exit(2)
                mail_desk = response or recommendation['address']
                if not postman.ADDRESS_RE.fullmatch(mail_desk):
                    raise postman.PostmanError('修改地址形不合法')
                signed, _ = postman.recommendation_book(
                    pathlib.Path(recommendation['book']['path']) if recommendation['book']['path'] else None,
                    required=True,
                )
                if signed is None or mail_desk not in signed:
                    raise postman.PostmanError('确认地址尚未人签簿；请人签后用显式 --desk 重跑，候选未占号')
        except Exception as exc:
            print(f'邮箱推荐失败：{exc}', file=sys.stderr)
            sys.exit(8)

    # 母本根与 DOSSIER_ROOT 现算：同盘落相对路径；跨盘降级为绝对路径，不中断装桌。
    repo_root = get_repo_root()
    mirror_root = repo_root / 'templates'
    src_dir = repo_root
    try:
        relative_path = os.path.relpath(src_dir, target)
        relative_path_posix = PurePath(relative_path).as_posix()
    except ValueError:
        relative_path_posix = src_dir.resolve().as_posix()
        print('\033[33m跨盘装桌：DOSSIER_ROOT 落绝对路径\033[0m')

    # 定义要铺的项目和内容
    structure = build_structure()

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
                                content = content.replace(DOSSIER_ROOT_PLACEHOLDER, relative_path_posix)
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
                        content = content.replace(DOSSIER_ROOT_PLACEHOLDER, relative_path_posix)
                        full_path.write_text(content, encoding='utf-8', newline='\n')
                print(f'+ {path_str}')
                created_count += 1

    # 处理 templates/ 那一棵
    # 检查 templates/ 是否存在
    if not mirror_root.exists():
        print(f'templates/ 不在仓库根，退出', file=sys.stderr)
        sys.exit(5)

    # 遍历 templates/ 下的所有文件和目录
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
            file_content = render(file_content, relative_path_posix)

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

    # 5.41 装桌自测：探针随 rules/ 走；默认跑，显式开关才跳过。
    if skip_self_test:
        print('= 5.41 装桌自测：按开关跳过（跳过不是绿）')
    elif dry_run:
        print('= 5.41 装桌自测：dry-run 未铺锁页，不跑')
    else:
        probe = subprocess.run(
            [sys.executable, "-B", "-X", "utf8", str(SETUP_PROBE_SOURCE), str(target)],
        )
        if probe.returncode != 0:
            print('装桌自测失败：init 不给绿，见上方红读数', file=sys.stderr)
            sys.exit(6)

    # 5.44 可选邮箱适配器：只在 --with-mail 时挂；不传旗零影响。
    if mail_url is not None:
        from . import postman
        try:
            postman.attach_mail(target, mail_url, mail_desk, dry_run=dry_run)
        except Exception as exc:
            print(f'邮箱可选装失败：{exc}', file=sys.stderr)
            sys.exit(8)

    # 5.30 转译基线：铺完骨架、自测跑完后落桌侧读数；dry-run 未铺出实桌，不落。
    # 基线一经落盘，init 幂等重跑不重落——重落会把宿主后续漂移洗成绿；重落走 dossier.py baseline --refresh。
    if dry_run:
        print('= 5.30 转译基线：dry-run 未铺出实桌，不落')
    else:
        if skip_self_test:
            print('= 5.41 装桌自测按开关跳过（跳过不是绿）；基线照落——基线是读数，不判绿')
        baseline_path = target / pathlib.Path(BASELINE_RELATIVE_PATH)
        if baseline_path.is_file():
            print(f'= 5.30 转译基线已在，不重落（{BASELINE_RELATIVE_PATH}）；重落走 dossier.py baseline --refresh')
        else:
            baseline = write_baseline(target, repo_root)
            if baseline is None:
                sys.exit(7)
            print(f'+ {BASELINE_RELATIVE_PATH}')
            print(f"转译基线：{len(baseline['files'])} 件（时戳 {baseline['generated_at']}，母本 HEAD {baseline['parent_head'][:12]}）")

    # 特殊输出：--force --non-interactive
    if force and non_interactive:
        print('按默认否')

    # 末行
    print(f'建 {created_count} 件，跳过 {skipped_count} 件，覆盖 {overwritten_count} 件')

    sys.exit(0)


if __name__ == '__main__':
    main()
