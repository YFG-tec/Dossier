#!/usr/bin/env python3
# 图标光栅化：SVG -> 512px PNG + 小尺寸对照条。
# 依赖：
#   - pillow 12.3.0（读 SVG、拼对照条）
#   - Microsoft Edge 无头模式（截图出 PNG）
#     默认路径：C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe
#     或 C:\Program Files\Microsoft\Edge\Application\msedge.exe
#     环境变量覆盖：设置 EDGE_PATH 指向 msedge.exe
# 用法：python render_icon.py

import os
import sys
import pathlib
import subprocess
import tempfile
from PIL import Image

def get_edge_path():
    """获取 Edge 可执行文件路径"""
    # 优先检查环境变量
    if 'EDGE_PATH' in os.environ:
        edge = os.environ['EDGE_PATH']
        if os.path.exists(edge):
            return edge
        else:
            sys.stderr.write(f"EDGE_PATH 指定的路径不存在: {edge}\n")
            sys.exit(1)

    # Windows 默认路径
    default_paths = [
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    ]

    for path in default_paths:
        if os.path.exists(path):
            return path

    sys.stderr.write("找不到 Microsoft Edge。请设置 EDGE_PATH 环境变量。\n")
    sys.exit(1)

def main():
    # 确定脚本和图标的路径（相对于仓库根）
    script_dir = pathlib.Path(__file__).parent
    repo_root = script_dir.parent.parent.parent

    icon_dir = repo_root / "docs_meta" / "src" / "figures"

    edge_exe = get_edge_path()

    tpl = ('<!doctype html><meta charset="utf-8">\n'
           '<style>html,body{margin:0;padding:0;background:#fff}\n'
           'svg{display:block;width:512px;height:512px}</style>\n')

    # 用临时目录放 HTML，避免污染源目录
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = pathlib.Path(tmpdir)

        # 读取和处理两份 SVG
        output_dir = icon_dir  # 输出到图标目录
        for name in ["dossier-icon", "dossier-icon-dark"]:
            svg_file = icon_dir / f"{name}.svg"
            html_file = tmpdir / f"{name}.html"
            png_file = output_dir / f"{name}.png"

            if not svg_file.exists():
                sys.stderr.write(f"SVG 不存在: {svg_file}\n")
                sys.exit(1)

            # 读 SVG，缩放到 512×512
            svg = svg_file.read_text(encoding="utf-8")
            svg = svg.replace('width="256" height="256"', 'width="512" height="512"', 1)
            html_file.write_text(tpl + svg, encoding="utf-8")

            # 用 Edge 截图
            try:
                subprocess.run([
                    edge_exe,
                    "--headless", "--disable-gpu", "--no-sandbox", "--hide-scrollbars",
                    "--force-device-scale-factor=1", "--window-size=512,512",
                    f'--screenshot={png_file}',
                    f'file:///{html_file.as_posix()}'
                ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            except subprocess.CalledProcessError as e:
                sys.stderr.write(f"Edge 截图失败: {e}\n")
                sys.exit(1)

        # 生成小尺寸对照条
        sizes = [128, 64, 48, 32, 16]
        for src_name, tag in [('dossier-icon.png', 'light'), ('dossier-icon-dark.png', 'dark')]:
            src = output_dir / src_name
            if not src.exists():
                sys.stderr.write(f"PNG 不存在: {src}\n")
                sys.exit(1)

            im = Image.open(src).convert('RGB')
            sheet = Image.new('RGB', (sum(sizes) + 20 * len(sizes), 140), (240, 240, 240))
            x = 10
            for s in sizes:
                sheet.paste(im.resize((s, s), Image.LANCZOS), (x, (140 - s) // 2))
                x += s + 20
            sheet.resize((sheet.width * 3, sheet.height * 3), Image.NEAREST).save(
                output_dir / f'sheet-{tag}.png'
            )

    print('rendered')

if __name__ == '__main__':
    main()
