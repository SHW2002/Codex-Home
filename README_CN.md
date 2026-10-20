# codex-home

[English](README.md) | 简体中文

用于在个人设备间同步可复用的 Codex 指令和自定义技能。

## 同步内容

- [AGENTS.md](AGENTS.md) 中的全局指令。
- [skills/](skills/README_CN.md) 下自定义技能的指令、脚本、参考文档及界面元数据。
- [wecom-transfer](skills/wecom-transfer/SKILL.md)：将当前已有桌面聊天直接绑定到企业微信。

## 企微快捷入口

在希望接续的 Codex 会话中输入：

    $wecom-transfer 把当前会话转到企业微信。

技能通过本机 HTTP 接口直接绑定原聊天，并向已授权单聊发送切换通知。之后在企微直接发送文字或语音即可，无需聊天名称前缀。/desktop status 查看目标，/desktop off 解除；普通使用无需提权或读取凭证。
详见[无密钥操作说明](skills/wecom-transfer/references/operations.md)。

当前技能对应本机 Windows 部署 D:/Services/WeCom-Codex-Bridge；其他设备使用前应核对路径并自行配置已授权机器人。

## 本地保留

根目录采用同步白名单；凭证及其备份、机器配置、会话历史、数据库、缓存、插件、系统技能和其他运行数据保留在本机。
包含真实凭证的私有操作手册位于仓库之外，不应复制到本仓库。

将可复用内容放在允许同步的文件或自定义技能目录中，核对暂存区后再提交推送。
