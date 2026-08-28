#!/usr/bin/env node

import { execFileSync, spawn } from 'node:child_process';
import { createServer } from 'node:http';
import { mkdtemp, readFile, rm, stat } from 'node:fs/promises';
import { existsSync, readFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { dirname, extname, join, relative, resolve, sep } from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const sleep = ms => new Promise(resolvePromise => setTimeout(resolvePromise, ms));

function requireCondition(condition, message) {
  if (!condition) throw new Error(`Glaze UI 2.0 prefers-contrast acceptance failed: ${message}`);
}

function findBrowser() {
  for (const name of ['google-chrome', 'google-chrome-stable', 'chromium', 'chromium-browser']) {
    try {
      const path = execFileSync('which', [name], { encoding: 'utf8' }).trim();
      if (path) return path;
    } catch {
      // Try the next Chromium-family browser.
    }
  }
  throw new Error('no supported Chromium-family browser found');
}

function contentType(path) {
  return ({
    '.html': 'text/html; charset=utf-8',
    '.css': 'text/css; charset=utf-8',
    '.js': 'text/javascript; charset=utf-8',
    '.mjs': 'text/javascript; charset=utf-8',
    '.json': 'application/json; charset=utf-8',
    '.svg': 'image/svg+xml',
  })[extname(path)] || 'application/octet-stream';
}

async function startServer() {
  const server = createServer(async (request, response) => {
    try {
      const url = new URL(request.url || '/', 'http://127.0.0.1');
      const rel = decodeURIComponent(url.pathname).replace(/^\/+/, '');
      const path = resolve(ROOT, rel || 'reference/candidate-2.0-resilience.html');
      requireCondition(path === ROOT || path.startsWith(`${ROOT}${sep}`), 'static request escaped repository root');
      const info = await stat(path);
      requireCondition(info.isFile(), 'static request did not resolve to a file');
      response.writeHead(200, {
        'content-type': contentType(path),
        'cache-control': 'no-store',
      });
      response.end(await readFile(path));
    } catch (error) {
      response.writeHead(404, { 'content-type': 'text/plain; charset=utf-8' });
      response.end(error instanceof Error ? error.message : String(error));
    }
  });

  await new Promise((resolvePromise, reject) => {
    server.once('error', reject);
    server.listen(0, '127.0.0.1', resolvePromise);
  });
  const address = server.address();
  requireCondition(address && typeof address === 'object', 'static server address unavailable');
  return { server, port: address.port };
}

async function waitForDevToolsPort(profileDir, browserProcess) {
  const activePort = join(profileDir, 'DevToolsActivePort');
  for (let attempt = 0; attempt < 100; attempt += 1) {
    if (browserProcess.exitCode != null) throw new Error(`Chromium exited before DevTools became ready: ${browserProcess.exitCode}`);
    if (existsSync(activePort)) {
      const [port] = readFileSync(activePort, 'utf8').trim().split(/\r?\n/);
      if (port) return Number(port);
    }
    await sleep(50);
  }
  throw new Error('DevToolsActivePort was not created');
}

async function openProtocolSocket(debugPort) {
  const response = await fetch(`http://127.0.0.1:${debugPort}/json/new?about:blank`, { method: 'PUT' });
  requireCondition(response.ok, `DevTools target creation returned ${response.status}`);
  const target = await response.json();
  requireCondition(typeof target.webSocketDebuggerUrl === 'string', 'DevTools target websocket URL missing');

  const socket = new WebSocket(target.webSocketDebuggerUrl);
  await new Promise((resolvePromise, reject) => {
    socket.addEventListener('open', resolvePromise, { once: true });
    socket.addEventListener('error', () => reject(new Error('DevTools websocket failed to open')), { once: true });
  });

  let nextId = 1;
  const pending = new Map();
  socket.addEventListener('message', event => {
    const message = JSON.parse(event.data);
    if (!message.id || !pending.has(message.id)) return;
    const { resolve: resolvePending, reject } = pending.get(message.id);
    pending.delete(message.id);
    if (message.error) reject(new Error(`${message.error.code}: ${message.error.message}`));
    else resolvePending(message.result || {});
  });

  const send = (method, params = {}) => new Promise((resolvePromise, reject) => {
    const id = nextId++;
    pending.set(id, { resolve: resolvePromise, reject });
    socket.send(JSON.stringify({ id, method, params }));
  });

  return { socket, send };
}

async function waitForContrastEvidence(send) {
  const expression = `(() => {
    const body = document.body;
    const root = document.documentElement;
    const probe = document.getElementById('contrast-probe');
    const material = document.getElementById('contrast-material');
    if (!body || !probe || !material) return null;
    const probeStyle = getComputedStyle(probe);
    const materialStyle = getComputedStyle(material);
    return {
      runtime: body.dataset.runtimeAccepted || null,
      marker: body.dataset.prefersContrastMore || null,
      media: matchMedia('(prefers-contrast: more)').matches,
      forcedColors: matchMedia('(forced-colors: active)').matches,
      probeValue: getComputedStyle(root).getPropertyValue('--glaze-contrast-probe').trim(),
      borderWidth: parseFloat(probeStyle.borderTopWidth),
      outlineWidth: parseFloat(probeStyle.outlineWidth),
      materialBorderWidth: parseFloat(materialStyle.borderTopWidth),
      overflow: Math.max(root.scrollWidth - root.clientWidth, body.scrollWidth - body.clientWidth),
    };
  })()`;

  for (let attempt = 0; attempt < 100; attempt += 1) {
    const result = await send('Runtime.evaluate', {
      expression,
      returnByValue: true,
      awaitPromise: true,
    });
    const value = result.result?.value;
    if (value?.runtime === 'true') return value;
    if (value?.runtime === 'false') throw new Error('contrast reference reported runtime failure');
    await sleep(50);
  }
  throw new Error('contrast reference did not reach runtime acceptance');
}

async function main() {
  requireCondition(typeof WebSocket === 'function', 'Node runtime does not provide WebSocket support');
  const browser = findBrowser();
  const profileDir = await mkdtemp(join(tmpdir(), 'glaze-candidate20-contrast-'));
  const { server, port } = await startServer();
  const browserProcess = spawn(browser, [
    '--headless=new',
    '--no-sandbox',
    '--disable-gpu',
    '--disable-dev-shm-usage',
    '--disable-background-networking',
    '--disable-background-timer-throttling',
    '--disable-renderer-backgrounding',
    '--disable-default-apps',
    '--disable-extensions',
    '--disable-sync',
    '--hide-scrollbars',
    '--mute-audio',
    '--no-first-run',
    '--remote-debugging-port=0',
    `--user-data-dir=${profileDir}`,
    '--window-size=1280,900',
    'about:blank',
  ], { stdio: ['ignore', 'ignore', 'pipe'] });

  let socket;
  try {
    const debugPort = await waitForDevToolsPort(profileDir, browserProcess);
    const protocol = await openProtocolSocket(debugPort);
    socket = protocol.socket;
    const send = protocol.send;

    await send('Page.enable');
    await send('Runtime.enable');
    await send('Emulation.setEmulatedMedia', {
      media: '',
      features: [{ name: 'prefers-contrast', value: 'more' }],
    });

    const targetUrl = `http://127.0.0.1:${port}/reference/candidate-2.0-resilience.html?case=contrast&appearance=light`;
    await send('Page.navigate', { url: targetUrl });
    const evidence = await waitForContrastEvidence(send);

    requireCondition(evidence.media === true, 'DevTools media override did not expose prefers-contrast: more');
    requireCondition(evidence.forcedColors === false, 'prefers-contrast acceptance must remain independent of forced-colors');
    requireCondition(evidence.marker === 'true', `reference contrast marker ${evidence.marker || 'missing'} != true`);
    requireCondition(evidence.probeValue === '1', `prefers-contrast media rule did not apply: probe=${evidence.probeValue || 'missing'}`);
    requireCondition(evidence.borderWidth >= 3, `contrast boundary below 3px: ${evidence.borderWidth}`);
    requireCondition(evidence.outlineWidth >= 3, `contrast outline below 3px: ${evidence.outlineWidth}`);
    requireCondition(evidence.materialBorderWidth >= 2, `core Glaze increased-contrast boundary below 2px: ${evidence.materialBorderWidth}`);
    requireCondition(evidence.overflow <= 1, `increased-contrast layout overflowed by ${evidence.overflow}px`);

    console.log('Glaze UI 2.0 Candidate prefers-contrast: more rendered acceptance passed via DevTools media emulation');
  } finally {
    try { socket?.close(); } catch {}
    if (browserProcess.exitCode == null) browserProcess.kill('SIGKILL');
    await new Promise(resolvePromise => server.close(resolvePromise));
    await rm(profileDir, { recursive: true, force: true });
  }
}

main().catch(error => {
  console.error(error instanceof Error ? error.message : String(error));
  process.exitCode = 1;
});
