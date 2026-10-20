# 企业微信接续已有 Codex 聊天

此文档可随 Git 同步，不包含 Bot ID、Secret 或内部账号标识。

## 使用

在目标 Codex 聊天说“使用 $wecom-transfer，把当前会话转到企业微信”。
技能直接请求本机 HTTP 接口，绑定原聊天并主动发送切换通知，无需复制或粘贴入口。
后续在企微机器人单聊直接发文字或语音，完成后自动回传原单聊。

- 另一个 Codex 聊天再次调用技能：切换目标。
- 企微 `/desktop status`：查看当前目标。
- 企微 `/desktop off`：解除绑定，恢复企微独立对话，已提交消息不会撤回。
- 绑定重启后保留；附件当前不投递，需在电脑端添加。
- 电脑需开机联网，Codex 桌面保持打开；目标正在处理时，等待本轮结束再执行新消息。

## 无提权调用

直接在普通 PowerShell 中使用 SKILL.md 的内联 Invoke-RestMethod，不启动用户目录中的脚本。
只需真实聊天 UUID，不读凭证、不启动嵌套 Codex 查询、不操作剪贴板。

查询绑定：

```powershell
Invoke-RestMethod 'http://127.0.0.1:8787/desktop/transfer' -Headers @{ 'X-Codex-Transfer' = '1' }
Invoke-RestMethod 'http://127.0.0.1:8787/health'
```

`status: bound` 是绑定成功，`notification: sent` 是企微通知发送获回执。
`awaiting_wecom_message` 表示等待真实企微指令，不等于双向验收成功。
`notification: unknown` 时绑定已保存，不自动重复通知。
GET 接口还返回 `delivery.status`：no_message 为尚无新消息，accepted 为已入队，delivered 为最终文本已回传。
此查询不返回消息正文、账号标识或凭证，无需直接读取受保护的 .runtime 目录。

## 服务边界与错误

- 部署目录：D:/Services/WeCom-Codex-Bridge。
- 上游：https://github.com/flyman008/wecom-codex-bridge （MIT）；本机增加 HTTP 接续接口及持久绑定。
- 仅监听 127.0.0.1，绑定接口拒绝浏览器 Origin、Fetch Metadata、非回环 Host 和缺失专用请求头的请求。
- 接口仅接受 threadId，不能提交命令、读取任意文件或绕过企微发送人白名单。
- 自动绑定仅支持一个机器人和一个已授权单聊接收人；多目标配置返回歧义错误。
- 绑定状态存于 .runtime/desktop-transfer；不进入 Git。
- `wecom_disconnected`：等待或修复机器人长连接。
- `desktop_transfer_disabled`：核对已获授权的 CODEX_DESKTOP_TASKS_ENABLED 设置。
- `single_bot_required` / `single_authorized_owner_required`：配置有歧义，不猜接收人。
- `transfer_busy`：另一切换正在处理，先查询最终绑定。
- `transfer_unavailable`：检查服务诊断；接口只返回脱敏错误码。
- 404：仍在运行旧版服务，需由维护操作升级及重启一次。

原聊天投递仍使用 scripts/codex-tasks.mjs send/wait，按真实企微 msgid 去重。
accepted 只是入队；对应原轮次真实结束且回传记录为 delivered 才能确认完整回传。
sending / unknown 不自动重发，不使用 exec resume 并行恢复原聊天。
旧的准确名称指令仍兼容，只临时路由该条消息，不修改绑定。

## 维护

普通接续无需提权；升级代码、重启服务属于维护操作，可能需要一次目录写入权限。
不要为了每次接续修改沙箱配置、开放用户目录或读取机器人密钥。

在部署目录中按需执行：

```powershell
.\scripts\status-service.ps1
npm run doctor
```

核对无活跃任务后重启：

```powershell
.\scripts\stop-service.ps1
.\scripts\start-service.ps1
```

旧部署 D:/Services/WeCom-Codex 保留供回退且自启已禁用；同一机器人不得同时连接新旧服务。
本机 .env、.runtime、logs 及含凭证手册保持私有，不提交 Git。

2026-10-18 原聊天带名称投递及回传已验收通过。
2026-10-20 修复旧技能依赖用户目录脚本执行和只复制入口的问题，增加普通权限 HTTP 绑定。

## 服务扩展源码

[assets/bridge-transfer.patch](../assets/bridge-transfer.patch) 保存本次本机桥接扩展与回归测试，不含凭证或运行记录。
它针对本机已经完成发送人白名单和明确标题路由修复的基线；不是适用于任意上游版本的通用安装器。
维护恢复时先备份当前代码，在部署目录执行 git apply --check 核对，再按需要应用补丁、npm run check 和重启。
当前电脑已安装，无需再次应用；普通调用技能不需要修改服务文件。
