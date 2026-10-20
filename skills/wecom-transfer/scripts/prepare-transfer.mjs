import { access } from 'node:fs/promises';
import { pathToFileURL } from 'node:url';
import { join } from 'node:path';
import { spawnSync } from 'node:child_process';

const bridgeRoot = 'D:/Services/WeCom-Codex-Bridge';
const manual = 'C:/Users/S.H.W/Documents/Codex/2026-10-18/new-chat/outputs/企业微信-Codex-本地操作手册-私密.md';

function options(args) {
  const result = { copy: false };
  for (let index = 0; index < args.length; index++) {
    const key = args[index];
    if (key === '--copy') result.copy = true;
    else if (key === '--thread' || key === '--message') {
      const value = args[++index];
      if (!value) throw new Error(`缺少 ${key} 参数值`);
      result[key.slice(2)] = value;
    } else throw new Error('未知参数；使用 --thread UUID、--message 指令、--copy');
  }
  return result;
}

async function prepare() {
  const args = options(process.argv.slice(2));
  const threadId = args.thread || process.env.CODEX_THREAD_ID || process.env.CODEX_SESSION_ID;
  if (!/^[0-9a-f]{8}(-[0-9a-f]{4}){3}-[0-9a-f]{12}$/i.test(threadId ?? '')) {
    throw new Error('未取得有效的当前聊天 ID，请显式传入 --thread');
  }
  await access(join(bridgeRoot, 'dist/src/agents/codex-cli.js'));
  const response = await fetch('http://127.0.0.1:8787/health', { signal: AbortSignal.timeout(3000) });
  const health = await response.json();
  if (!response.ok || health.status !== 'ok') throw new Error('企微桥接尚未在线，请按本地操作手册恢复现有服务');
  const { queryTasks } = await import(pathToFileURL(join(bridgeRoot, 'scripts/codex-tasks.mjs')).href);
  const info = await queryTasks('read', threadId, 'codex');
  const title = String(info.title ?? '').trim();
  if (!title || title.length > 160 || /[“”"「」『』\r\n]/.test(title)) {
    throw new Error('聊天名称不适合当前企微路由格式，请使用不含引号换行的唯一名称');
  }
  const matches = await queryTasks('list', title, 'codex');
  const exact = matches.tasks.filter(task => task.title === title);
  if (exact.length !== 1 || exact[0].id !== threadId) throw new Error('聊天名称不唯一，无法安全生成目标入口');
  const instruction = args.message || '请简短汇报本会话的当前进度和待办，不修改文件，完成后把回复发回企业微信喵';
  if (Buffer.byteLength(instruction, 'utf8') > 28000) throw new Error('指令过长，请缩短后重试');
  const entryMessage = `在“${title}”这个已有 Codex 聊天中继续：${instruction}`;
  let clipboard = 'not_requested';
  if (args.copy) {
    const clipboardEnv = { ...process.env };
    delete clipboardEnv.PSModulePath;
    const copied = spawnSync('powershell.exe', [
      '-NoLogo', '-NoProfile', '-NonInteractive', '-Command',
      '[Console]::InputEncoding = [Text.UTF8Encoding]::new(); $entry = [Console]::In.ReadToEnd(); Set-Clipboard -Value $entry',
    ], { input: entryMessage, encoding: 'utf8', windowsHide: true, timeout: 8000, env: clipboardEnv });
    clipboard = copied.status === 0 ? 'copied' : 'unavailable';
  }
  console.log(JSON.stringify({ status: 'ready', threadId, title, health: health.status, clipboard,
    entryMessage, operatorManual: manual, delivery: 'not_submitted' }, null, 2));
}

prepare().catch(() => {
  // Operational errors may contain host details; keep credentials and query contents out of output.
  console.error('无法准备企微入口：请核对聊天 ID、服务状态、名称唯一性和本机执行权限；详见本地操作手册。');
  process.exitCode = 1;
});
