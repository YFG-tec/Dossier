#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
框架图生成脚本（make_frame.py）

依赖：
  - matplotlib 3.11.2 或兼容版本
  - pillow 12.3.0 或兼容版本
  - numpy 2.5.3 或兼容版本

运行方法：
  在仓库根目录运行：
  .venv/Scripts/python.exe docs_meta/src/figures/make_frame.py

输出：
  docs_meta/src/figures/dossier-frame.png (1760 × 1024)

中文字体：Microsoft YaHei
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Arc, FancyArrowPatch
import numpy as np

# 颜色定义（来自 naming.md:123）
COLOR_INK = '#1D1D1F'      # 墨
COLOR_RED = '#D9342B'       # 朱
COLOR_BG = '#FFFFFF'        # 白底
COLOR_GRAY_BG = '#F5F5F4'   # 流转带底色
COLOR_GRAY_LINE = '#ECECEC' # 列导引线
COLOR_GRAY_TEXT = '#6B6B6B'
COLOR_GRAY_TEXT_LIGHT = '#8A8A8A'
COLOR_GRAY_TEXT_LIGHTER = '#9A9A9A'

# 设置字体
plt.rcParams['font.family'] = 'Microsoft YaHei'
plt.rcParams['axes.unicode_minus'] = False

# ============================================================================
# 1. 创建画布，分辨率 2× = 1760 × 1024
# ============================================================================
fig, ax = plt.subplots(figsize=(17.6, 10.24), dpi=100)
ax.set_xlim(0, 880)
ax.set_ylim(512, 0)  # 顶部是 y=0
ax.axis('off')

# 背景
fig.patch.set_facecolor(COLOR_BG)
ax.add_patch(patches.Rectangle((0, 0), 880, 512,
                                fill=True, facecolor=COLOR_BG,
                                edgecolor='none', zorder=0))

# ============================================================================
# 2. 标题与图例
# ============================================================================
ax.text(20, 34, '目录即权限', fontsize=21, fontweight='bold',
        color=COLOR_INK, va='top')

# 图例符号和说明
legend_y = 33
# 写 ▣
ax.add_patch(patches.FancyBboxPatch((475, 21), 15, 15,
                                     boxstyle="round,pad=0.5",
                                     fill=True, facecolor=COLOR_INK,
                                     edgecolor='none'))
ax.text(497, legend_y, '写', fontsize=13, color=COLOR_GRAY_TEXT, va='center')

# 只读 ○
circle = patches.Circle((549, 28.5), 7, fill=False,
                       edgecolor=COLOR_INK, linewidth=2, alpha=0.4)
ax.add_patch(circle)
ax.text(563, legend_y, '只读', fontsize=13, color=COLOR_GRAY_TEXT, va='center')

# 不许碰 ·
ax.text(607, legend_y, '·', fontsize=16, color=COLOR_INK,
        ha='center', va='center', alpha=0.4)
ax.text(625, legend_y, '不许碰', fontsize=13,
        color=COLOR_GRAY_TEXT, va='center')

# 朱
ax.add_patch(patches.FancyBboxPatch((727, 21), 15, 15,
                                     boxstyle="round,pad=0.5",
                                     fill=True, facecolor=COLOR_RED,
                                     edgecolor='none'))
ax.text(749, legend_y, '朱＝只有人能落', fontsize=13,
        color=COLOR_GRAY_TEXT, va='center')

# ============================================================================
# 3. 列头（层名）
# ============================================================================
col_headers = ['约定', '合同', '在办', '实现', '把关', '交付', '草稿']
col_x = [216, 312, 408, 504, 600, 696, 792]

for label, x in zip(col_headers, col_x):
    ax.text(x, 62, label, fontsize=17, color=COLOR_INK,
            ha='center', va='top', fontweight='normal')

# 列头下分隔线
ax.plot([168, 840], [76, 76], color=COLOR_INK, linewidth=2)

# 列导引线
for x in col_x[:-1]:
    ax.plot([x + 48, x + 48], [80, 298], color=COLOR_GRAY_LINE, linewidth=1)

# 实现席分隔线
ax.plot([168, 840], [166, 166], color='#E2E2E2', linewidth=1)

# ============================================================================
# 4. 行标（手名）及权威递进
# ============================================================================
row_labels = ['人', '规划席', '实现', '测试', '审查']
row_y = [106, 138, 194, 238, 282]

for label, y in zip(row_labels, row_y):
    ax.text(150, y, label, fontsize=17, color=COLOR_INK,
            ha='right', va='center')

# 规划席默认 Cursor
ax.text(150, 155, '默认 Cursor', fontsize=11, color=COLOR_GRAY_TEXT_LIGHTER,
        ha='right', va='center')

# ============================================================================
# 5. 实现席括弧与标识
# ============================================================================
# 左边括弧（三行：实现、测试、审查）
bracket_x = [94, 86]  # x 坐标
bracket_y_top = 169
bracket_y_bottom = 295
bracket_width = 8

# 绘制括弧
ax.plot([bracket_x[1], bracket_x[1], bracket_x[0]],
        [bracket_y_top, bracket_y_bottom, bracket_y_bottom],
        color=COLOR_INK, linewidth=1.5, alpha=0.55, solid_capstyle='butt')

# 实现席标签
ax.text(76, 220, '实现席', fontsize=14, color=COLOR_GRAY_TEXT,
        ha='right', va='center')
ax.text(76, 237, '默认', fontsize=11, color=COLOR_GRAY_TEXT_LIGHTER,
        ha='right', va='center')
ax.text(76, 251, 'Claude Code', fontsize=11, color=COLOR_GRAY_TEXT_LIGHTER,
        ha='right', va='center')

# ============================================================================
# 6. 矩阵格子
# ============================================================================
# 格子大小
box_size = 22
box_radius = 5

# 定义所有的黑色实心格子（▣）
# 格式：(row_idx, col_idx)
filled_cells = [
    (0, 0),  # 人 × 约定
    (0, 1),  # 人 × 合同
    # (0, 2),  # 人 × 在办 - 特殊，用朱
    (1, 1),  # 规划席 × 合同
    (1, 2),  # 规划席 × 在办
    (1, 5),  # 规划席 × 交付
    (1, 6),  # 规划席 × 草稿
    (2, 3),  # 实现 × 实现
    (2, 6),  # 实现 × 草稿
    (3, 4),  # 测试 × 把关
    (3, 6),  # 测试 × 草稿
]

# 绘制黑色实心格子
for row_idx, col_idx in filled_cells:
    y = row_y[row_idx]
    x = col_x[col_idx]
    ax.add_patch(patches.FancyBboxPatch((x - box_size/2, y - box_size/2),
                                        box_size, box_size,
                                        boxstyle=f"round,pad={box_radius*0.3}",
                                        fill=True, facecolor=COLOR_INK,
                                        edgecolor='none'))

# 朱色格子（人 × 在办）
y = row_y[0]
x = col_x[2]
ax.add_patch(patches.FancyBboxPatch((x - box_size/2, y - box_size/2),
                                    box_size, box_size,
                                    boxstyle=f"round,pad={box_radius*0.3}",
                                    fill=True, facecolor=COLOR_RED,
                                    edgecolor='none'))

# 定义所有的只读格子（○）
# 格式：(row_idx, col_idx)
readonly_cells = [
    (0, 5),  # 人 × 交付
    (1, 0),  # 规划席 × 约定
    (2, 0),  # 实现 × 约定
    (2, 1),  # 实现 × 合同
    (2, 2),  # 实现 × 在办
    (2, 5),  # 实现 × 交付
    (3, 0),  # 测试 × 约定
    (3, 1),  # 测试 × 合同
    (3, 2),  # 测试 × 在办
    (3, 5),  # 测试 × 交付
    (4, 0),  # 审查 × 约定
    (4, 1),  # 审查 × 合同
    (4, 2),  # 审查 × 在办
    (4, 5),  # 审查 × 交付
]

# 定义不许碰的格子（·）
# 格式：(row_idx, col_idx)
forbidden_cells = [
    (0, 3),  # 人 × 实现
    (0, 4),  # 人 × 把关
    (0, 6),  # 人 × 草稿
    (1, 3),  # 规划席 × 实现
    (1, 4),  # 规划席 × 把关
    (2, 4),  # 实现 × 把关
    (3, 3),  # 测试 × 实现
    (4, 3),  # 审查 × 实现
    (4, 4),  # 审查 × 把关
    (4, 6),  # 审查 × 草稿
]

# 绘制只读圆圈
for row_idx, col_idx in readonly_cells:
    y = row_y[row_idx]
    x = col_x[col_idx]
    circle = patches.Circle((x, y), 9, fill=False,
                           edgecolor=COLOR_INK, linewidth=2, alpha=0.4)
    ax.add_patch(circle)

# 绘制不许碰的符号（·）
for row_idx, col_idx in forbidden_cells:
    y = row_y[row_idx]
    x = col_x[col_idx]
    ax.text(x, y, '·', fontsize=16, color=COLOR_INK,
            ha='center', va='center', alpha=0.4)

# 合同列的※标记
ax.text(326, 182, '※', fontsize=12, color=COLOR_GRAY_TEXT, ha='center', va='center')

# ============================================================================
# 7. 表格下线与说明
# ============================================================================
ax.plot([168, 840], [298, 298], color=COLOR_INK, linewidth=2)

ax.text(168, 315, '审查那一行一个实心都没有——审查的手不写文件',
        fontsize=12, color=COLOR_GRAY_TEXT, ha='left', va='top')
ax.text(840, 315, '※ 卡片点名才改合同',
        fontsize=12, color=COLOR_GRAY_TEXT, ha='right', va='top')

# ============================================================================
# 8. 接上表的过渡箭头
# ============================================================================
# 竖箭头：表示上下连接
arrow_x = 26
arrow_y_top = 330
arrow_y_mid = 342
arrow_y_bottom = 352

# 竖线
ax.plot([arrow_x, arrow_x], [arrow_y_top, arrow_y_top + 12],
        color=COLOR_INK, linewidth=1.5, alpha=0.6)
# 箭头（向下的 V 形）
ax.plot([arrow_x - 4, arrow_x, arrow_x + 4],
        [arrow_y_top + 7, arrow_y_top + 12, arrow_y_top + 7],
        color=COLOR_INK, linewidth=1.5, alpha=0.6)

# 桥文字：整句一次画，不分段（中文字宽无法手算对齐）
bridge_text = '同一批手，摊到时间上——上表说谁许写，下带说什么时候轮到谁'
ax.text(40, arrow_y_mid, bridge_text, fontsize=13, color=COLOR_INK,
        ha='left', va='center')

# ============================================================================
# 9. 流转带（灰色底）
# ============================================================================
band_x = 14
band_y = 352
band_width = 852
band_height = 128
band_radius = 10

ax.add_patch(patches.FancyBboxPatch((band_x, band_y), band_width, band_height,
                                    boxstyle=f"round,pad={band_radius*0.5}",
                                    fill=True, facecolor=COLOR_GRAY_BG,
                                    edgecolor='none', zorder=1))

# 流转带标题
ax.text(32, 378, '换阶段就是换手', fontsize=16, fontweight='bold',
        color=COLOR_INK, ha='left', va='top', zorder=2)

# ============================================================================
# 10. 流转带上的席位标签
# ============================================================================
ax.text(225, 398, '规划席', fontsize=13, color=COLOR_GRAY_TEXT,
        ha='center', va='center', zorder=2)
ax.text(498, 398, '实现席（三只手串行，不并行改核）', fontsize=13,
        color=COLOR_GRAY_TEXT, ha='center', va='center', zorder=2)
ax.text(763, 398, '人', fontsize=13, color=COLOR_GRAY_TEXT,
        ha='center', va='center', zorder=2)

# ============================================================================
# 11. 流转带中的三段弧线（席位分隔）
# ============================================================================
bracket_y_mid = 410
bracket_height = 7

# 规划席段
x1, x2 = 160, 290
ax.plot([x1, x1], [bracket_y_mid - bracket_height, bracket_y_mid],
        color=COLOR_INK, linewidth=2, zorder=2)
ax.plot([x1, x2], [bracket_y_mid, bracket_y_mid],
        color=COLOR_INK, linewidth=2, zorder=2)
ax.plot([x2, x2], [bracket_y_mid, bracket_y_mid - bracket_height],
        color=COLOR_INK, linewidth=2, zorder=2)

# 实现席段
x1, x2 = 306, 690
ax.plot([x1, x1], [bracket_y_mid - bracket_height, bracket_y_mid],
        color=COLOR_INK, linewidth=2, zorder=2)
ax.plot([x1, x2], [bracket_y_mid, bracket_y_mid],
        color=COLOR_INK, linewidth=2, zorder=2)
ax.plot([x2, x2], [bracket_y_mid, bracket_y_mid - bracket_height],
        color=COLOR_INK, linewidth=2, zorder=2)

# 人段
x1, x2 = 706, 820
ax.plot([x1, x1], [bracket_y_mid - bracket_height, bracket_y_mid],
        color=COLOR_INK, linewidth=2, zorder=2)
ax.plot([x1, x2], [bracket_y_mid, bracket_y_mid],
        color=COLOR_INK, linewidth=2, zorder=2)
ax.plot([x2, x2], [bracket_y_mid, bracket_y_mid - bracket_height],
        color=COLOR_INK, linewidth=2, zorder=2)

# ============================================================================
# 12. 流转带中的阶段标签
# ============================================================================
stage_y = 434
ax.text(225, stage_y, '立案', fontsize=16, color=COLOR_INK,
        ha='center', va='center', zorder=2)
ax.text(370, stage_y, '施工', fontsize=16, color=COLOR_INK,
        ha='center', va='center', zorder=2)
ax.text(498, stage_y, '举证', fontsize=16, color=COLOR_INK,
        ha='center', va='center', zorder=2)
ax.text(626, stage_y, '对账', fontsize=16, color=COLOR_INK,
        ha='center', va='center', zorder=2)
ax.text(763, stage_y, '结案', fontsize=16, color=COLOR_INK,
        ha='center', va='center', zorder=2)

# ============================================================================
# 13. 流转带中的手标签（小号、灰色）
# ============================================================================
hand_y = 452
ax.text(370, hand_y, '实现', fontsize=12, color=COLOR_GRAY_TEXT_LIGHT,
        ha='center', va='center', zorder=2)
ax.text(498, hand_y, '测试', fontsize=12, color=COLOR_GRAY_TEXT_LIGHT,
        ha='center', va='center', zorder=2)
ax.text(626, hand_y, '审查', fontsize=12, color=COLOR_GRAY_TEXT_LIGHT,
        ha='center', va='center', zorder=2)

# ============================================================================
# 14. 两道闸（虚线）
# ============================================================================
gate_y_top = 404
gate_y_bottom = 458

# 闸一（施工前）
ax.plot([298, 298], [gate_y_top, gate_y_bottom],
        color=COLOR_INK, linewidth=1.5, linestyle=(0, (4, 4)), zorder=2)

# 结案（结案后）
ax.plot([698, 698], [gate_y_top, gate_y_bottom],
        color=COLOR_INK, linewidth=1.5, linestyle=(0, (4, 4)), zorder=2)

# ============================================================================
# 15. 闸标签
# ============================================================================
ax.text(291, 472, '闸一「按卡片做」', fontsize=12.5, color=COLOR_GRAY_TEXT,
        ha='right', va='top', zorder=2)
ax.text(705, 472, '结案「勾 TODO」', fontsize=12.5, color=COLOR_GRAY_TEXT,
        ha='left', va='top', zorder=2)

# ============================================================================
# 16. 底部说明
# ============================================================================
ax.text(20, 500, '画的是桌上的一刀。母本自己没有 src/ 与 tests/——规矩作用在桌上，clone 下来不带求解器。',
        fontsize=12, color=COLOR_GRAY_TEXT_LIGHT, ha='left', va='top')

# ============================================================================
# 保存图像
# ============================================================================
# 输出为 PNG，DPI 100，尺寸 1760 × 1024
output_path = 'docs_meta/src/figures/dossier-frame.png'
# 不使用 tight_layout，直接用指定的 figsize 和 dpi（17.6 × 100 = 1760）
fig.savefig(output_path, dpi=100,
            facecolor=COLOR_BG, edgecolor='none')
plt.close(fig)

print(f'Generated: {output_path}')

# 6.11：渲染成功即盖内容戳——记「哪一版脚本生成了当前图」的 git 眼中哈希（blob）；
# 对 EOL 形态恒等（autocrlf 的 clone 树算出同值），git 带得走，mtime 和裸字节都带不走
import subprocess as _sp
_bh = _sp.run(['git', 'hash-object', __file__], capture_output=True, text=True, check=True).stdout.strip()
with open('docs_meta/src/figures/dossier-frame.render-stamp', 'w', newline='\n') as _s:
    _s.write(_bh + '\n')
print(f'Stamped: {_bh[:12]}…')
