# 操作说明，不是开关

下面这几条是宿主怎么用，不是这张桌的规矩，别当判据引。

**动过 `.claude/` 要重载窗口才生效。** 代理名册是会话进程启动时扫一次的快照，之后不重扫。
新加或改名 `.claude/agents/*.md`，当前这个会话看不见，派的时候报
`Agent type 'xxx' not found`。skill 和 settings 同理。

重载窗口（VS Code / Cursor 的 Reload Window）之后名册重建，新的那几只手就派得动了。
`--resume` 同一个会话也重建。2026-09-12 实测过这三格。

**这不是文件坏了。** 撞上的时候先看会话是什么时候起的，别去改 agent 文件。
`2.6c` 那一刀就是这么误判的：会话 09-08 起，`.claude/agents/` 09-12 才落盘，
差了三天半，所以整刀都派不动，当时记成了「这个 harness 派不出任何一只手」。

## 这一份开关两席是怎么读到的（2026-09-12 实测）

实现席：根 CLAUDE.md 里那一行 @ 导入，会展开。
规划席：.cursor/rules/*.mdc 带 alwaysApply: true 的正文自动进上下文；@ 导入行一律不展开。

这两格是外部产品那一天的行为，不是常量。换一组平台要重走一遍这个编译流程，
一组平台走一次。厂商改了机制，这份产物会静默失准，盘上不会红——这是明着留的残余。

## Bash 弹窗：A 档前缀（2026-09-13）

不是这张桌的规矩，不当判据引。人裁：A 直接改项目 `.claude/settings.json`，B/C 暂不处理。
读测前缀：`grep` / `awk` / `sed -n` / `echo` / `wc` / `head` / `tail` / `mkdir`、`bash docs_meta/tests/*`、`SWITCH_ROOT=` / `SECT_ROOT=`、只读 `git status|diff|log|ls-files`。
**没放** `tee`、`chmod`。改完要重载窗口。

**没验过的一句，写在改动旁边：** 前缀够宽之后，宿主还往不往 `settings.local.json` 追加原文，本席没量。
`Bash(awk *)` 按厂商文档罩住整句，包括 `awk … > 文件`。A 不是只读；堵重定向要 `deny` 或 hook，人裁暂不处理。

人 2026-09-13 后裁：git 写操作堵严，其余不管。项目 `settings.json` 的 `deny` 拦
`git commit` / `push` / `reset` / `rebase`（含 `git -C …` 那一形）。
`status` / `diff` / `log` / `ls-files` 仍在 allow。`&&` 拼在后面的 `git commit` 前缀匹配可能罩不住，厂商文档如此，不吹。改完重载窗口。
