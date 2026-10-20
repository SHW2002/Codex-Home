---
name: wecom-transfer
description: 通过已部署的本机桥接服务，将当前已有 Codex 聊天直接绑定到企业微信；适用于“把当前会话转到企微”“从企微继续这个聊天”，后续消息无需聊天名称前缀。
---

# 企业微信接续当前聊天

复用本机 `http://127.0.0.1:8787` 的桥接服务。调用一次即绑定原聊天，并向已授权的企微单聊发送切换通知；之后直接在企微发文字或语音即可继续。

## 执行

1. 从当前环境的 `CODEX_THREAD_ID` 取得真实聊天 ID；缺失时通过桌面 `list_threads` 核对，不按目录猜测，也不把桥接子会话的 ID 当作目标。
2. **直接在普通 PowerShell 工具中请求本机接口**，不先启动技能目录中的 Node 脚本，不读取密钥，不申请提权：

   ```powershell
   $transferThread = $env:CODEX_THREAD_ID
   # 若上一阶段通过桌面工具核对了 ID，则在此使用核对后的 UUID。
   $transferBody = @{ threadId = $transferThread } | ConvertTo-Json -Compress
   Invoke-RestMethod -Uri 'http://127.0.0.1:8787/desktop/transfer' `
     -Method Post -Headers @{ 'X-Codex-Transfer' = '1' } `
     -ContentType 'application/json; charset=utf-8' `
     -Body ([Text.Encoding]::UTF8.GetBytes($transferBody)) -TimeoutSec 45
   ```

3. 核对返回 `status: bound`、`binding.threadId` 与目标一致。告知用户已切换，直接在企微单聊发消息即可；`notification: sent` 表示切换通知已发送，`delivery: awaiting_wecom_message` 表示还没有新的企微指令，不能声称已完成双向验收。
4. `notification: unknown` 时绑定仍已保存，只说明通知回执不确定；不要自动重复绑定或发送测试。用户需要验收时，用其授权的无文件改动消息，并核对对应原聊天回复及 `delivered` 回传记录。

当前聊天忙碌时，新企微消息会等待本轮结束；不要在当前轮一直等待自己回复。

## 切换与解除

- 在另一个 Codex 聊天再次调用本技能即可切换到那个原聊天，按 UUID 路由，不要求唯一名称。
- 企微发送 `/desktop status` 查看目标，发送 `/desktop off` 解除，恢复企微独立对话；已有已投递消息不会撤回。
- 绑定持久保存，服务重启后保留。目前接续支持文字和语音，附件会明确拒绝投递。
- 原有带准确名称的入口仍可临时路由一条消息，不改变持久绑定。

## 排障边界

- 首先用同样的请求头 GET `/desktop/transfer` 查询绑定及脱敏 `delivery.status`，并 GET `/health` 检查服务；普通接续不需要 `.env`、Bot ID 或 Secret，也不直接读取受保护的 `.runtime`。`accepted` 表示已入队，`delivered` 才表示最终回复已回传。
- 禁止把普通环境失败改为每次提权运行旧脚本；旧版 Node 文件入口曾在启动前因用户目录 `EPERM` 失败，内联 HTTP 调用解决了这个依赖。
- 接口返回 404 表示服务尚未升级；连接失败、`wecom_disconnected`、`desktop_transfer_disabled` 等按 [references/operations.md](references/operations.md) 诊断现有服务，不关闭沙箱或新增模型目录授权。
- `single_bot_required` 或 `single_authorized_owner_required` 表示配置存在歧义，不能猜测目标接收人。
- 不伪造企微消息 ID，不调用裸 `codex queue`，不另启 `exec resume`；真实消息仍由原桥接核对发送人、去重并回传。
