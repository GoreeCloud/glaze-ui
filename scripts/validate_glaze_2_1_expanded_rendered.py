#!/usr/bin/env python3
"""Rendered interaction and visual-invariant regression for expanded Glaze UI 2.1 Candidate flows."""
from __future__ import annotations
import tempfile,urllib.parse
from validate_rendered_reference import RENDER_ATTEMPTS,TV_FORCED_COLORS_ATTEMPTS,acceptance_result,browser_command,find_browser,run_browser,serve_root
def run_case(browser,port,*,flow,width,height,appearance,form_factor,clarity='balanced',expression='balanced',density='standard',performance='balanced',mode='normal',scenario='none'):
 params={'flow':flow,'width':width,'height':height,'appearance':appearance,'clarity':clarity,'expression':expression,'density':density,'performance':performance,'formFactor':form_factor,'mode':mode,'scenario':scenario};name=f"2.1-expanded {flow} {form_factor} {width}x{height} {appearance} clarity={clarity} density={density} performance={performance} mode={mode} scenario={scenario}";attempts=TV_FORCED_COLORS_ATTEMPTS if mode=='forced-colors' and form_factor=='tv' else RENDER_ATTEMPTS;last='browser did not produce a result'
 for attempt in range(1,attempts+1):
  query=urllib.parse.urlencode({**params,'attempt':attempt});url=f"http://127.0.0.1:{port}/reference/candidate-2.1-expanded-acceptance.html?{query}"
  with tempfile.TemporaryDirectory(prefix='glaze-21-expanded-render-') as profile:
   command=browser_command(browser,url,profile,width=width,height=height,mode=mode)
   try:completed=run_browser(command)
   except Exception as exc:
    last=f"attempt {attempt} browser execution failed: {exc}"
    if attempt<attempts:print(f"Glaze UI 2.1 expanded regression retrying: {name}");continue
    break
  status,text=acceptance_result(completed.stdout)
  if completed.returncode!=0:last=f"attempt {attempt} browser exited {completed.returncode}\n{completed.stderr[-2000:]}"
  elif status=='pass' and text and text.startswith('PASS'):print(f"Glaze UI 2.1 expanded regression passed: {name}");return
  elif status=='fail':raise SystemExit(f"Glaze UI 2.1 expanded regression failed for {name}:\n{text or '(no result text)'}")
  else:last=f"attempt {attempt} did not reach PASS (status={status or 'missing'})\n{text or (completed.stdout[-3000:] if completed.stdout else completed.stderr[-3000:])}"
  if attempt<attempts:print(f"Glaze UI 2.1 expanded regression retrying: {name}")
 raise SystemExit(f"Glaze UI 2.1 expanded regression failed for {name} after {attempts} attempts:\n{last}")
def main():
 browser=find_browser()
 with serve_root() as port:
  cases=(dict(flow='search',width=1280,height=900,appearance='light',form_factor='desktop',scenario='command-open-select'),dict(flow='search',width=390,height=844,appearance='dark',form_factor='mobile',clarity='clear',mode='reduced-transparency'),dict(flow='search',width=1280,height=900,appearance='deep-dark',form_factor='desktop',mode='increased-contrast'),dict(flow='communication',width=390,height=844,appearance='dark',form_factor='mobile',scenario='message-send'),dict(flow='communication',width=1280,height=900,appearance='light',form_factor='desktop',expression='expressive',mode='reduced-motion'),dict(flow='communication',width=820,height=1180,appearance='dark',form_factor='tablet',density='compact',mode='large-text'),dict(flow='media',width=1280,height=900,appearance='deep-dark',form_factor='desktop',clarity='clear',performance='full',scenario='playback-toggle'),dict(flow='media',width=1920,height=1080,appearance='dark',form_factor='tv',density='far-view'),dict(flow='media',width=1280,height=900,appearance='light',form_factor='desktop',performance='minimal'),dict(flow='media',width=1280,height=900,appearance='dark',form_factor='desktop',mode='forced-colors'))
  for case in cases:run_case(browser,port,**case)
 print('Glaze UI 2.1 expanded interaction and visual-invariant regression passed')
if __name__=='__main__':main()
