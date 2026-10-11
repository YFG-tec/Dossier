#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
用户版架构图生成脚本（make_frame.py，5.36/PROMPT_092 重写）。
「Dossier 的一天」：你（四件事）→ 代理席闭环（蓝印）→ 机器验真横带。
替换 3.3 的权限矩阵图（矩阵图归档于 git 历史）；朱红只给「你」的元素（naming.md 色律）。

依赖：
  - matplotlib 3.11.2 或兼容版本
  - pillow 12.3.0 或兼容版本（matplotlib 默认后端）

运行方法：
  在仓库根目录运行：
  .venv/Scripts/python.exe docs_meta/src/figures/make_frame.py

输出：
  docs_meta/src/figures/dossier-frame.png (1760 × 1024)

中文字体：Microsoft YaHei
数据面：队列＝docs/queue.md（在办层序列单）；刀/todo/SESSION 均为 docs/ 在办层文件。
"""
import matplotlib
matplotlib.use("Agg")  # 不弹窗（verify.md：画图不弹窗）
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

# 颜色定义（来自 naming.md:123）
COLOR_INK = '#1D1D1F'       # 墨
COLOR_RED = '#D9342B'       # 朱（只给「你」）
COLOR_BLUE = '#2F6FED'      # 蓝印蓝
COLOR_BG = '#FFFFFF'        # 白底
COLOR_GRAY_LINE = '#D9D9D6' # 细线
COLOR_GRAY_TEXT = '#6B6B6B' # 次要文字
COLOR_GRAY_BG = '#F7F7F5'   # 机器验真横带底

plt.rcParams['font.family'] = 'Microsoft YaHei'
plt.rcParams['axes.unicode_minus'] = False

# 画布：880×512 逻辑，dpi 200 → 1760×1024
fig, ax = plt.subplots(figsize=(8.8, 5.12), dpi=200)
ax.set_xlim(0, 880); ax.set_ylim(0, 512)
ax.axis('off'); fig.patch.set_facecolor(COLOR_BG)

def box(x, y, w, h, ec, fc='white', lw=1.6, r=3.0, z=2):
    p = FancyBboxPatch((x, y), w, h,
        boxstyle=f'round,pad=0,rounding_size={r}',
        linewidth=lw, edgecolor=ec, facecolor=fc, zorder=z)
    ax.add_patch(p); return p

def arrow(x1, y1, x2, y2, color, lw=1.8, style='-|>', ms=14, conn='arc3,rad=0', z=3, ls='-'):
    a = FancyArrowPatch((x1, y1), (x2, y2), arrowstyle=style, mutation_scale=ms,
        linewidth=lw, color=color, connectionstyle=conn, zorder=z, linestyle=ls)
    ax.add_patch(a); return a

def txt(x, y, s, size=11, color=COLOR_INK, ha='center', va='center', w='normal', z=4):
    ax.text(x, y, s, fontsize=size, color=color, ha=ha, va=va, fontweight=w, zorder=z)

# ── 标题 ──────────────────────────────────────────────
txt(24, 486, 'Dossier 的一天', size=19, w='bold', ha='left')
txt(24, 462, '你点行，代理跑刀，机器验真', size=11.5, color=COLOR_GRAY_TEXT, ha='left')

# ── 左栏：你 ──────────────────────────────────────────
box(24, 120, 180, 300, COLOR_RED, lw=2.2)
txt(114, 396, '你', size=16, color=COLOR_RED, w='bold')
txt(114, 374, '每天只做四件事', size=10.5, color=COLOR_GRAY_TEXT)
items = ['点一行待办', '说一声开工', '结案时认账', '断点时拍板']
iy = 336
for it in items:
    box(40, iy - 18, 148, 38, COLOR_RED, fc='#FDF6F5', lw=1.1, r=2.5)
    txt(114, iy + 1, it, size=11.5)
    iy -= 52
txt(114, 138, '其余都有人代笔', size=10, color=COLOR_GRAY_TEXT)

# ── 中栏：代理席（蓝印）───────────────────────────────
box(258, 120, 396, 300, COLOR_BLUE, lw=2.2)
txt(456, 396, '代理席', size=16, color=COLOR_BLUE, w='bold')
txt(456, 374, '按队列自己往下走，每刀一报', size=10.5, color=COLOR_GRAY_TEXT)

steps = ['取队列', '写卡', '派手施工', '独立审查', '跑验收', '蓝印记档']
sx, sy, sw, sh, gap = 276, 300, 56, 34, 8
positions = []
x = sx
for s in steps:
    box(x, sy, sw, sh, COLOR_BLUE, lw=1.3, r=2.5)
    fs = 9.0 if len(s) >= 4 else 10.5
    txt(x + sw/2, sy + sh/2, s, size=fs)
    positions.append(x + sw/2)
    x += sw + gap
for i in range(len(positions) - 1):
    x1 = 276 + (i + 1) * (sw + gap) - gap
    arrow(x1, sy + sh/2, x1 + gap, sy + sh/2, COLOR_BLUE, lw=1.4, ms=10)
# 闭环回箭头（蓝印记档 → 取队列）
arrow(positions[-1], sy + 40, positions[0], sy + 40, COLOR_BLUE, lw=1.4, ms=10,
      conn='arc3,rad=0.05')
txt(456, 254, '撞断点：停下、盘上留痕、等你拍板', size=10.5, color=COLOR_RED)
arrow(456, 274, 456, 292, COLOR_RED, lw=1.5, ms=11)

# 角注两枚
box(276, 152, 176, 44, COLOR_GRAY_LINE, lw=1.0, r=2.5, fc=COLOR_BG)
txt(364, 184, '蓝印＝你的章', size=10.5, w='bold')
txt(364, 166, '效力相同，只标是谁落的', size=9, color=COLOR_GRAY_TEXT)
box(466, 152, 170, 44, COLOR_GRAY_LINE, lw=1.0, r=2.5, fc=COLOR_BG)
txt(551, 184, '永不 push', size=10.5, w='bold', color=COLOR_INK)
txt(551, 166, '远端同步是你的动作', size=9, color=COLOR_GRAY_TEXT)

# ── 底部横带：机器验真 ────────────────────────────────
box(24, 36, 630, 62, COLOR_INK, lw=1.2, fc=COLOR_GRAY_BG)
txt(54, 78, '机器验真', size=12, w='bold', ha='left')
txt(54, 56, '二十二本机械检查一条入口 · 起步闸（开工自检）· 配置指纹（偏没偏一条命令问答）',
    size=10, color=COLOR_GRAY_TEXT, ha='left')

# ── 右栏重排：每刀一报置顶，状态在磁盘居中，桌间信箱沉底 ─
box(696, 300, 160, 110, COLOR_GRAY_LINE, lw=1.2, r=3.0)
txt(776, 374, '每刀一报', size=12, w='bold')
txt(776, 350, '每刀都有回执：', size=9.5, color=COLOR_GRAY_TEXT)
txt(776, 330, '卡上写的验收 · 独立审查的结论', size=9.5, color=COLOR_GRAY_TEXT)
txt(776, 310, '· 全部落盘可查', size=9.5, color=COLOR_GRAY_TEXT)

box(696, 190, 160, 80, COLOR_GRAY_LINE, lw=1.2, r=3.0)
txt(776, 250, '状态在磁盘', size=11.5, w='bold')
txt(776, 226, '不在聊天里漂移', size=9.5, color=COLOR_GRAY_TEXT)
txt(776, 206, '换窗口不丢范围', size=9.5, color=COLOR_GRAY_TEXT)

box(696, 64, 160, 80, COLOR_INK, lw=1.2, r=3.0, fc=COLOR_BG)
txt(776, 126, '桌间信箱', size=11, w='bold')
txt(776, 102, '可选 · 一桌一址', size=9, color=COLOR_GRAY_TEXT)
txt(776, 82, '不装零影响', size=9, color=COLOR_GRAY_TEXT)
ax.plot([654, 676, 676, 696], [150, 150, 104, 104], color=COLOR_INK, lw=1.0,
        linestyle=(0, (3, 3)), zorder=2)
# ── 主箭头 ────────────────────────────────────────────
arrow(210, 300, 252, 300, COLOR_RED, lw=2.0, ms=15)
txt(231, 316, '点行＋开工', size=9, color=COLOR_RED)
arrow(658, 352, 690, 352, COLOR_BLUE, lw=1.8, ms=13)
txt(672, 340, '刀报', size=9, color=COLOR_BLUE)
# 认账/拍板回线：走画布顶部，绕开蓝框与回环弧（首版穿框，目检修）
import matplotlib.lines as mlines
ax.add_line(mlines.Line2D([836, 836], [410, 444], color=COLOR_RED, lw=1.4, ls=(0, (4, 3)), zorder=3))
ax.add_line(mlines.Line2D([836, 126], [444, 444], color=COLOR_RED, lw=1.4, ls=(0, (4, 3)), zorder=3))
arrow(126, 444, 114, 428, COLOR_RED, lw=1.4, ms=12)
txt(415, 458, '认账 / 拍板（断点续跑也是一句话）', size=9, color=COLOR_GRAY_TEXT)

plt.tight_layout(pad=0.4)
out = 'docs_meta/src/figures/dossier-frame.png'
fig.savefig(out, dpi=200, facecolor=COLOR_BG)
print('written:', out)

# render-stamp：git 内容戳（check-rename 第 4 条的尺——6.11 裁 A 形，重渲即随图更新）
import subprocess as _sp
_bh = _sp.run(['git', 'hash-object', __file__], capture_output=True, text=True, check=True).stdout.strip()
with open('docs_meta/src/figures/dossier-frame.render-stamp', 'w', newline='\n') as _s:
    _s.write(_bh + '\n')
print(f'Stamped: {_bh[:12]}…')
