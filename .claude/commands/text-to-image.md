调用本仓库 Token Plan 文生图 API，根据描述生成图片。

用户需求：$ARGUMENTS

## 步骤

1. 从用户需求中提取 prompt（图片描述）、model、size（默认 `1024*1024`）。若用户明确指定了模型（如「模型=wan2.7-image」或「用 wan2.7-image 画」），必须严格使用用户指定的模型名，不要回退到默认模型；仅当用户未指定模型时才使用默认 `qwen-image-2.0`。常用图像生成模型有 `qwen-image-2.0`、`qwen-image-2.0-pro`、`wan2.7-image`、`wan2.7-image-pro` 等，完整列表以百炼模型列表为准。

2. 鉴权用环境变量 `$ANTHROPIC_AUTH_TOKEN`（本仓库已在 `.claude/settings.local.json` 配好）。不要打印、不要写入文件、不要写进回复。

3. 调用 API 生成图片（使用 Bash 工具执行 curl）。prompt 里若有引号或换行，先写成 JSON 再提交，不要手拼：

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

4. 从返回 JSON 的 `output.choices[*].message.content[*].image` 中提取图片 URL。若没有 URL，把完整错误 JSON 报给用户，停止。

5. 下载到 `.tmp/text-to-image/`，不要落到仓库根：

```bash
curl -s -o ".tmp/text-to-image/generated_$(date +%Y%m%d_%H%M%S).png" "<URL>"
```

6. 向用户展示生成的图片文件路径。
