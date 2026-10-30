# 本地生图接口配置与调用

本配置只用于图片生成和图片编辑，不修改聊天、文本模型或 Codex 自身的接口。用户已选择 API/CLI，无需每次重复确认。

## 首选与备选

真实配置位于本技能根目录 `.env`，通过相对技能目录定位，兼容 Windows、fairy 和 rp1。

| 项目 | 配置 |
| --- | --- |
| 首选 | OpenAI 官方；`OPENAI_BASE_URL=https://api.openai.com/v1`，密钥为 `OPENAI_API_KEY` |
| 备选 | 变更前的生图接口及原密钥；`OPENAI_FALLBACK_BASE_URL`、`OPENAI_FALLBACK_API_KEY` |
| 模型 | `OPENAI_IMAGE_MODEL=gpt-image-2.5-sunburst`，保持用户既有要求 |
| 质量 | `OPENAI_IMAGE_QUALITY=high` |
| CLI | 当前安装的 `imagegen/scripts/image_gen.py` |

工作区的 `.kaltsit-imagegen.env` 也使用同样的首选／备选字段；项目技能仍以自己的模型要求为准，不把 UI 技能的模型名推广到其他技能。当前明确指定的配置路径优先。

`.env` 必须被 Git 忽略且未被跟踪；macOS 权限保持 `600`。只解析所需字段，不把文件作为脚本执行，不打印真实密钥、认证头或原始响应日志，不写入提示词、源码或产物记录。不设置全局用户环境，以免影响非生图任务。可提交的 `.env.example` 只包含空凭据和非敏感默认值。

## 调用与切换

1. 阅读当前 `imagegen` 技能和 CLI 文档，按实际 `--help` 支持的参数执行；不修改官方 CLI，也不另写 SDK 生图客户端。
2. 定位可用 Python 和所需依赖，提示词保存 UTF-8 文件并使用 `--prompt-file`；需要时使用 `--no-augment`。
3. 首次始终选择首选，只把该组地址和密钥映射到本次 CLI 子进程的 `OPENAI_BASE_URL`、`OPENAI_API_KEY`；不要将备选密钥发送给首选地址或反向混用。显式传入 `--model` 和 `--quality`；CLI 不自动读取这两个自定义变量。
4. 新参数组合先 `--dry-run`，检查模型、尺寸、参考图和输出路径；dry-run 不证明服务端支持。参考图调用可使用 `edit`，提示词明确它是风格参考还是编辑目标。
5. 首选返回明确失败且没有生成结果时，可以切换到已授权备选，例如认证、额度、限流或明确的模型不支持错误；保持同一提示词、参考图、模型和质量。参数错误先查参数，不机械切换；安全策略拒绝不能通过切换服务绕过。
6. 切换时在新的子进程中将两个 `OPENAI_FALLBACK_*` 字段成对映射为标准 `OPENAI_*` 变量；不改写磁盘中的首选字段。每个任务最多切换一次，备选失败后报告脱敏错误，不在两端循环重试。
7. 超时、连接中断、5xx 或结果状态不确定时，先检查已有响应和产物；不能直接在另一端重发可能已经计费的请求。无法确认时报告不确定状态，避免重复生成。
8. 记录实际采用的服务标识（首选官方／备选）、模型、质量、尺寸及产物路径，不记录凭据；发生切换时告知用户。

## 模型与透明能力

- 使用 GPT Image 2.5 系列最高能力型号 `gpt-image-2.5-sunburst`，质量保持用户既有 `high`；官方型号说明：https://developers.openai.com/api/docs/models/gpt-image-2.5-sunburst 。既有第三方模型名不保证官方支持。官方明确不支持且无结果时按上述顺序使用备选，不擅自换型号。
- 透明能力按实际模型、CLI 和服务分别核实；不伪造 alpha，不自行换成 `gpt-image-1.5`。
- 官方 API 基础地址依据：https://developers.openai.com/api/reference/python/ 。

配置修改和技能离线验证无需执行收费生图。
