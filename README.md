# codex-home

English | [简体中文](README_CN.md)

Reusable Codex instructions and custom skills synchronized across personal devices.

## Included content

- Global instructions in [AGENTS.md](AGENTS.md).
- Custom skills and their scripts, references, and interface metadata under [skills/](skills/README.md).
- The [wecom-transfer skill](skills/wecom-transfer/SKILL.md), which directly binds an existing desktop chat to the locally deployed WeCom bot.

## WeCom shortcut

In the Codex conversation you want to continue, invoke:

    $wecom-transfer Continue this chat through WeCom.

The skill binds the existing chat through a loopback HTTP endpoint and sends a switch notification to your authorized private chat. Then send plain text or voice messages in WeCom without a title prefix. Use /desktop status to inspect the target or /desktop off to disconnect. Ordinary skill use needs no elevation or credentials.
See the [credential-free operations guide](skills/wecom-transfer/references/operations.md).

The skill targets the existing Windows deployment in D:/Services/WeCom-Codex-Bridge.
On another device, review the local paths and prepare its own authorized bot configuration.

## Local-only data

The repository uses a root allowlist. Credentials, credential backups, machine configuration, conversation history, databases, caches, plugins, built-in skills, and other runtime state remain local.
The private operator manual containing real credentials is outside this repository and must not be copied into it.

Keep reusable changes in the allowed files or custom skill directories, review the staged changes, and sync them through the configured remote.
