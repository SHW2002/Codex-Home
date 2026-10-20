// Optional terminal helper. Inside Codex sandbox use inline PowerShell from SKILL.md.
const args = process.argv.slice(2);
let threadId = process.env.CODEX_THREAD_ID || process.env.CODEX_SESSION_ID;
let statusOnly = false;
for (let i = 0; i < args.length; i++) {
  if (args[i] === '--status') statusOnly = true;
  else if (args[i] === '--thread') threadId = args[++i];
  else throw new Error('Use --thread UUID or --status; copying an entry is no longer required');
}
async function main() {
  if (!statusOnly && !/^[0-9a-f]{8}(-[0-9a-f]{4}){3}-[0-9a-f]{12}$/i.test(threadId ?? '')) {
    throw new Error('invalid_thread_id');
  }
  const response = await fetch('http://127.0.0.1:8787/desktop/transfer', {
    method: statusOnly ? 'GET' : 'POST',
    headers: { 'X-Codex-Transfer': '1', 'Content-Type': 'application/json' },
    ...(statusOnly ? {} : { body: JSON.stringify({ threadId }) }),
    signal: AbortSignal.timeout(45000),
  });
  const body = await response.json();
  if (!response.ok) throw new Error(body.error || `http_${response.status}`);
  console.log(JSON.stringify(body, null, 2));
}
main().catch(error => {
  console.error(JSON.stringify({ error: error.cause?.code || error.message,
    action: 'See references/operations.md; use inline PowerShell in a Codex sandbox' }));
  process.exitCode = 1;
});
