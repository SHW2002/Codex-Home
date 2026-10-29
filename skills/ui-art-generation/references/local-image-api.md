# 本地生图接口配置与调用

用户已经明确要求本个人技能使用历史生图 API 和 URL，模型固定为 `gpt-image-2.5-sunburst`，质量为 `high`。使用本技能执行生图时沿用这一配置，不要求用户每次重述接口选择；这不授权超出当前任务的额外生成或发布。

## 当前配置

真实配置以技能根目录 `.env` 为准：

| 项目 | 配置 |
| --- | --- |
| 当前本地文件 | `C:/Users/S.H.W/.codex/skills/ui-art-generation/.env`；技能迁移时按相对路径 `.env` 定位 |
| API 密钥变量 | `OPENAI_API_KEY` |
| API Base URL 变量 | `OPENAI_BASE_URL` |
| 模型变量 | `OPENAI_IMAGE_MODEL=gpt-image-2.5-sunburst` |
| 质量变量 | `OPENAI_IMAGE_QUALITY=high` |
| 典型尺寸 | `1536x1024` 素材图集、`1024x1024` 头像 |
| 执行入口 | 当前 `imagegen` 技能目录下 `scripts/image_gen.py` |

该配置的 API 密钥和地址已从 `E:/Projects/Unity/Kaltsit-Go-Go-Go/.kaltsit-imagegen.env` 迁入，本技能不再依赖其他项目的环境文件。只有当前文件遗失或用户要求重新同步时，才用该历史位置恢复。

加载 `.env` 后只将上述四个变量注入本次生图进程。不要打印文件、实际变量值、认证头或完整请求日志，不把真实密钥和地址存入提示词、源码、产物清单或技能正文。可提交的 `.env.example` 中密钥和地址留空；真实 `.env` 必须通过 `git check-ignore`，且不能已经被 Git 跟踪。

文件格式示意，凭据位置仅作占位，不能据此覆盖已有真实配置：

```dotenv
OPENAI_API_KEY=
OPENAI_BASE_URL=
OPENAI_IMAGE_MODEL=gpt-image-2.5-sunburst
OPENAI_IMAGE_QUALITY=high
```

历史任务实际使用 `edit` 命令携带风格参考图；它在这类调用中也可承担参考图引导生成。提示词必须说明输入是画风参考还是实际待编辑对象，不能误把风格参考物体画入结果。

## 调用方式

1. 读取当前 `imagegen/SKILL.md` 及其 CLI 文档；本用户已明确选择 API/CLI，按现有脚本的 `--help` 和实际模型能力拼参数，不照搬过期参数。
2. 通过工作区依赖工具定位 Python，检查 `openai`、Pillow 等所需依赖。不要修改用户机器的全局包版本；已有隔离依赖可复用。
3. 提示词保存 UTF-8 文件，使用 `--prompt-file`，避免 PowerShell 字符转义改变内容；已经整理完整的提示词可用当前 CLI 支持的 `--no-augment`。
4. 加载本地 `.env`，核对四个变量非空，并显式使用 `--model <OPENAI_IMAGE_MODEL的值>`、`--quality <OPENAI_IMAGE_QUALITY的值>`。CLI 不会自动读取这两个自定义变量；API 密钥和 Base URL 通过其标准环境变量读取。
5. 新组合先 `--dry-run` 核对模型、尺寸、参考顺序和输出路径，再做任务内已授权的真实调用。dry-run 不证明服务端模型存在或透明能力可用。
6. 使用技能提供的官方 CLI，不另写一套生图 SDK runner，也不改它的模型校验或透明参数校验。

2026-10-28 订单和纸袋插画已验证以下调用形状，执行时从本地配置加载相同模型与质量：

```text
python <imagegen-dir>/scripts/image_gen.py edit --model gpt-image-2.5-sunburst --quality high --size 1536x1024 --background transparent --output-format png --image style-primary.png --image style-secondary.png --prompt-file sprites-prompt.txt --no-augment --out output/imagegen/<task>/sheet.png
```

尖括号表示需替换的路径，不是直接可执行命令。路径含空格时使用 shell 的参数数组/正确引号，不能用 `JSON.stringify()` 代替 shell 转义。局部编辑若需 `--mask`，按 CLI 文档核对尺寸、透明含义及适用的输入图。

## 型号与透明能力不能混为一谈

- `gpt-image-2.5-sunburst / high` 是用户固定要求，并已在此前任务中使用。除用户当次另有明确指定外必须沿用；只有用户要求更新到当时最新最高档时才重新核对，不自动替换。
- 本机 `imagegen` 文档对 CLI `gpt-image-2` 明确限制 `background=transparent`。该限制不能外推为所有模型都不透明，也不能把其他型号的成功经历当作它支持透明。
- 使用当前可用的官方文档查询能力核实用户点名的型号；历史参考页为 `https://developers.openai.com/api/docs/models/gpt-image-2.5-sunburst`，其存在性和内容仍需当次核实。
- 服务端拒绝参数时保留错误摘要，查明具体能力；不伪造 alpha、不悄悄换成 `gpt-image-1.5`，也不重复收费重试同一无效参数。
- 403、余额/额度或模型不可用需要明确报告。普通瞬时网络错误可有限重试并使用新的输出名；响应不确定时先检查是否已有产物。

此技能的创建和离线脚本验证都不需要调用生图接口。
