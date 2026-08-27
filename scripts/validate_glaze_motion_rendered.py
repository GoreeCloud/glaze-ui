#!/usr/bin/env python3
"""Rendered acceptance for the Glaze Motion 0.2 Experimental Motion Core layer."""
from __future__ import annotations
import contextlib,html,http.server,os,re,shutil,signal,socket,subprocess,tempfile,threading
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; RENDER_ATTEMPTS=3; RENDER_TIMEOUT_SECONDS=45; VIRTUAL_TIME_BUDGET_MS=5000
def fail(message): raise SystemExit(f"Glaze Motion rendered acceptance failed: {message}")
def find_browser():
    for name in ("google-chrome","google-chrome-stable","chromium","chromium-browser"):
        path=shutil.which(name)
        if path:return path
    fail("no supported Chromium-family browser found")
@contextlib.contextmanager
def serve_root():
    class QuietHandler(http.server.SimpleHTTPRequestHandler):
        def log_message(self,*_args): pass
    with socket.socket() as probe: probe.bind(("127.0.0.1",0)); port=probe.getsockname()[1]
    server=http.server.ThreadingHTTPServer(("127.0.0.1",port),QuietHandler); thread=threading.Thread(target=server.serve_forever,daemon=True); previous=Path.cwd()
    try: os.chdir(ROOT); thread.start(); yield port
    finally: server.shutdown(); thread.join(timeout=5); os.chdir(previous)
def stop_process_group(process):
    if os.name!="posix":
        if process.poll() is None: process.kill()
        return
    try: os.killpg(process.pid,signal.SIGKILL)
    except ProcessLookupError: pass
def run_browser(command):
    process=subprocess.Popen(command,cwd=ROOT,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,start_new_session=(os.name=="posix"))
    try: stdout,stderr=process.communicate(timeout=RENDER_TIMEOUT_SECONDS); return subprocess.CompletedProcess(command,process.returncode,stdout,stderr)
    except subprocess.TimeoutExpired as exc: stop_process_group(process); stdout,stderr=process.communicate(); exc.stdout=stdout; exc.stderr=stderr; raise
    finally: stop_process_group(process)
def result_from_dom(output):
    match=re.search(r'<pre\s+id="result"\s+data-status="([^"]+)"[^>]*>(.*?)</pre>',output,flags=re.DOTALL)
    if not match:return None,None
    return match.group(1),html.unescape(re.sub(r"<[^>]+>","",match.group(2))).strip()
def browser_command(browser,url,profile,width,height,reduced):
    command=[browser,"--headless=new","--no-sandbox","--disable-gpu","--disable-dev-shm-usage","--disable-background-networking","--disable-background-timer-throttling","--disable-backgrounding-occluded-windows","--disable-renderer-backgrounding","--disable-default-apps","--disable-extensions","--disable-sync","--hide-scrollbars","--mute-audio","--no-first-run","--run-all-compositor-stages-before-draw",f"--virtual-time-budget={VIRTUAL_TIME_BUDGET_MS}",f"--user-data-dir={profile}",f"--window-size={width},{height}"]
    if reduced: command.append("--force-prefers-reduced-motion")
    command.extend(["--dump-dom",url]); return command
def run_case(browser,port,width,height,reduced):
    mode="reduced-motion" if reduced else "normal"; case=f"{width}x{height} {mode}"; last_failure="browser did not produce a result"
    for attempt in range(1,RENDER_ATTEMPTS+1):
        url=f"http://127.0.0.1:{port}/reference/glaze-motion.html?attempt={attempt}"
        with tempfile.TemporaryDirectory(prefix="glaze-motion-render-") as profile:
            try: completed=run_browser(browser_command(browser,url,profile,width,height,reduced))
            except subprocess.TimeoutExpired as exc:
                stderr=exc.stderr.decode(errors="replace") if isinstance(exc.stderr,bytes) else (exc.stderr or ""); last_failure=f"attempt {attempt} timed out after {RENDER_TIMEOUT_SECONDS}s\n{stderr[-1500:]}"
                if attempt<RENDER_ATTEMPTS: print(f"Glaze Motion rendered acceptance retrying after timeout: {case}"); continue
                break
        status,text=result_from_dom(completed.stdout)
        if completed.returncode!=0:last_failure=f"attempt {attempt} browser exited {completed.returncode}\n{completed.stderr[-1500:]}"
        elif status=="pass" and text and text.startswith("PASS"): print(f"Glaze Motion rendered acceptance passed: {case}"); return
        elif status=="fail": fail(f"{case}: {text or 'harness reported FAIL without detail'}")
        else:last_failure=f"attempt {attempt} did not reach PASS (status={status or 'missing'})\n{text or completed.stdout[-1500:]}"
        if attempt<RENDER_ATTEMPTS: print(f"Glaze Motion rendered acceptance retrying after incomplete result: {case}")
    fail(f"{case} after {RENDER_ATTEMPTS} attempts:\n{last_failure}")
def main():
    browser=find_browser()
    with serve_root() as port: run_case(browser,port,390,844,False); run_case(browser,port,390,844,True); run_case(browser,port,1280,900,False)
    print("Glaze Motion 0.2 Experimental rendered acceptance passed")
if __name__=="__main__": main()
