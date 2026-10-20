# 企业微信接续已有 Codex 聊天

此文档可随 Git 同步，不包含 Bot ID、Secret 或内部账号标识。

## 现有部署

- 上游：https://github.com/flyman008/wecom-codex-bridge （MIT）。
- 本机部署目录：D:/Services/WeCom-Codex-Bridge。
- 健康检查：http://127.0.0.1:8787/health，正常为 status: ok。
- 配置文件：部署目录中的 .env，仅保存在本机。
- 机器人字段：WECOM_BOT_ID、WECOM_BOT_SECRET。
- 发送人白名单：PC_CONTROL_ALLOWED_USERIDS；群聊关闭。
- 桌面任务投递开启；操作系统服务控制关闭。
- 普通对话保留上下文，模型参数继承当前用户本机 Codex 配置。

## 快捷使用

在目标 Codex 会话中调用 $wecom-transfer；辅助脚本核对真实聊天 ID、准确名称、名称唯一性及服务状态，并可复制入口文字。

手动使用脚本：

    node '<本技能目录>/scripts/prepare-transfer.mjs' --thread '<已核对的聊天UUID>' --copy

使用 --message 可传入第一条具体指令。脚本的 ready 表示入口已生成，不表示已投递。
然后在已配对的企微机器人单聊粘贴发送，例如：

    在“聊天准确名称”这个已有 Codex 聊天中继续：请汇报当前进度，不修改文件，完成后把回复发回企业微信。

每条需要继续桌面聊天的企微消息都保留名称前缀。不带目标名称的普通消息会进入企微自己的连续对话。
电脑需开机联网，Codex 桌面保持打开；消息可能等待当前轮次结束后执行。

## 原聊天与回传

消息入口先核对原始发送人及群聊策略，再使用原有 scripts/codex-tasks.mjs 的 list/send/wait 查询与投递。
不要伪造企微消息 ID、调用裸 codex queue 绕过去重，或用 exec resume 并行恢复桌面原聊天。
accepted 只是入队；只有对应轮次真实结束且回传记录为 delivered 才能确认回传成功。
sending 或 unknown 不自动重发，先核对原聊天和本地回传记录。

2026-10-18 的无文件改动确认测试已通过，确认文字成功回到原企微会话；2026-10-20 复核服务健康正常。
首次验收曾因嵌套 Codex 沙箱内无法查询桌面聊天而失败，现由桥接服务在鉴权后直接调用原有投递脚本。

## 服务管理

在部署目录中按需执行：

    .\scripts\status-service.ps1
    npm run doctor
    .\scripts\start-service.ps1

重启前检查活跃任务，按顺序停止再启动：

    .\scripts\stop-service.ps1
    .\scripts\start-service.ps1

当前登录自启任务为“企微Codex桥接-cc6b9e1dac”。旧部署 D:/Services/WeCom-Codex 保留供回退，旧任务 WeCom-Codex 已禁用；不要同时启动新旧长连接。

## 凭证与恢复

普通接续无需读取凭证。真实凭证在部署目录的 .env，以及仓库外受 ACL 限制的本地私有操作手册中。
需要维护时从本机配置恢复，不把凭证写入技能、Git、命令参数或聊天。
企微 CLI 授权丢失时，在本机交互运行 node node_modules/@wecom/cli/bin/wecom.js auth init --manual，再以 auth show --status 核对 authorized。
Codex 使用当前用户自己的登录状态，不使用机器人 Secret 登录 Codex。

新设备必须核对脚本中的本地路径、单独配置凭证并授权发送人；不要同时连接同一机器人。
