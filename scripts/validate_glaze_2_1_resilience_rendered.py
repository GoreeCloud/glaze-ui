#!/usr/bin/env python3
"""Rendered acceptance for Glaze UI 2.1 Candidate resilience and exceptional-state reference flow."""
from __future__ import annotations
import tempfile,urllib.parse
from validate_rendered_reference import RENDER_ATTEMPTS,TV_FORCED_COLORS_ATTEMPTS,acceptance_result,browser_command,find_browser,run_browser,serve_root

def run_case(browser,port,*,width,height,appearance,form_factor,clarity='solid',density='standard',performance='constrained',mode='normal'):
 params={'width':width,'height':height,'appearance':appearance,'clarity':clarity,'density':density,'performance':performance,'formFactor':form_factor,'mode':mode};name=f"2.1-resilience {form_factor} {width}x{height} {appearance} clarity={clarity} density={density} performance={performance} mode={mode}";attempts=TV_FORCED_COLORS_ATTEMPTS if mode=='forced-colors' and form_factor=='tv' else RENDER_ATTEMPTS;last='browser did not produce a result'
 for attempt in range(1,attempts+1):
  query=urllib.parse.urlencode({**params,'attempt':attempt});url=f"http://127.0.0.1:{port}/reference/candidate-2.1-resilience-acceptance.html?{query}"
  with tempfile.TemporaryDirectory(prefix='glaze-21-resilience-render-') as profile:
   command=browser_command(browser,url,profile,width=width,height=height,mode=mode)
   try:completed=run_browser(command)
   except Exception as exc:
    last=f"attempt {attempt} browser execution failed: {exc}"
    if attempt<attempts:print(f"Glaze UI 2.1 resilience acceptance retrying: {name}");continue
    break
  status,text=acceptance_result(completed.stdout)
  if completed.returncode!=0:last=f"attempt {attempt} browser exited {completed.returncode}\n{completed.stderr[-2000:]}"
  elif status=='pass' and text and text.startswith('PASS'):print(f"Glaze UI 2.1 resilience acceptance passed: {name}");return
  elif status=='fail':raise SystemExit(f"Glaze UI 2.1 resilience acceptance failed for {name}:\n{text or '(no result text)'}")
  else:last=f"attempt {attempt} did not reach PASS (status={status or 'missing'})\n{text or (completed.stdout[-3000:] if completed.stdout else completed.stderr[-3000:])}"
  if attempt<attempts:print(f"Glaze UI 2.1 resilience acceptance retrying: {name}")
 raise SystemExit(f"Glaze UI 2.1 resilience acceptance failed for {name} after {attempts} attempts:\n{last}")

def main():
 browser=find_browser()
 with serve_root() as port:
  cases=(dict(width=1280,height=900,appearance='light',form_factor='desktop',clarity='solid',performance='constrained'),dict(width=390,height=844,appearance='dark',form_factor='mobile',clarity='clear',performance='balanced',mode='reduced-transparency'),dict(width=820,height=1180,appearance='light',form_factor='tablet',clarity='balanced',density='compact',performance='balanced',mode='large-text'),dict(width=1280,height=900,appearance='dark',form_factor='desktop',clarity='balanced',performance='balanced',mode='forced-colors'))
  for case in cases:run_case(browser,port,**case)
 print('Glaze UI 2.1 resilience and exceptional-state rendered acceptance passed')

if __name__=='__main__':main()
