---
name: text-to-image
description: 调用本仓库阿里云 Token Plan 文生图接口生成图片。用户要求画图、文生图、生成图片、出一张图，或使用 /text-to-image 时使用。
---

# text-to-image · Token Plan 文生图

这不是角色，是本仓库 Claude Code 的宿主接法。课题那三份 skill（`write-cmd` / `one-slice` / `example-report`）一个字不碰。

鉴权走项目 `.claude/settings.local.json` 里的 `$ANTHROPIC_AUTH_TOKEN`（`sk-sp-`）。不要打印、不要写入文件、不要写进回复。不要改用户级 Claude Code 插件设置，也不要改进库的 `.claude/settings.json`。

## 什么时候用

用户要画图、文生图、生成图片，或打了 `/text-to-image`。不要用它给算例报告造「通过」用的图。

## 步骤

1. 从用户话里抽出 prompt、model、size（默认 `1024*1024`）。用户点名了模型就必须用那个名字，不要退回默认。没点名才用 `qwen-image-2.0`。常用：`qwen-image-2.0`、`qwen-image-2.0-pro`、`wan2.7-image`、`wan2.7-image-pro`。

2. 用 Bash 调专用端点。文生图不走 Anthropic `/v1/messages`，也不走 OpenAI `compatible-mode` 聊天口。prompt 含引号或换行时先写成 JSON 再提交：

```bash
mkdir -p .tmp/text-to-image
curl -s -X POST "https://token-plan.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation" \
  -H "Authorization: Bearer $ANTHROPIC_AUTH_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "<model>",
    "input": {
      "messages": [{"role":"user","content":[{"text":"<prompt>"}]}]
    },
    "parameters": {"size":"<size>"}
  }'
```

3. 从 `output.choices[*].message.content[*].image` 取 URL。没有 URL 就把完整错误 JSON 报给用户，停止。

4. 下载到 `.tmp/text-to-image/`（`.tmp/*` 不进 git），不要落到仓库根：

```bash
curl -s -o ".tmp/text-to-image/generated_$(date +%Y%m%d_%H%M%S).png" "<URL>"
```

5. 只回报本地路径。图本身零权威，不当验收材料。

## 对账

| 项 | 值 |
|---|---|
| 端点 | `https://token-plan.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation` |
| 鉴权 | `Authorization: Bearer $ANTHROPIC_AUTH_TOKEN` |
| 默认模型 | `qwen-image-2.0` |
| 默认尺寸 | `1024*1024` |
| 落盘 | `.tmp/text-to-image/generated_YYYYMMDD_HHMMSS.png` |
| 斜杠命令 | `/text-to-image 画一只猫` |
