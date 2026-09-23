#!/usr/bin/env python3
"""Behavior tests for finalize_blog.py. Stdlib only."""
import subprocess, sys, tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SCRIPT=ROOT/'blog-writer/scripts/finalize_blog.py'
fails=0

def check(ok,msg):
 global fails; fails += not ok; print(('PASS ' if ok else 'FAIL ')+msg)

with tempfile.TemporaryDirectory() as td:
 p=Path(td); post=p/'post.md'; brief=p/'brief.md'
 post.write_text('# Post\nClaim one [code: src/app.py:10].\nMissing [VERIFY: dashboard].\n')
 brief.write_text('# Brief\n')
 r=subprocess.run([sys.executable,str(SCRIPT),str(post),str(brief)],capture_output=True,text=True)
 check(r.returncode==1 and 'FAIL [VERIFY] left: 1' in r.stdout,'VERIFY blocks finalization')
 check(not (p/'post-publish.md').exists(),'blocked run writes no publish copy')
 post.write_text('# Post\nClaim one [code: src/app.py:10].\nAuthor says yes [author].\nAWS supports it [aws-doc: https://docs.aws.amazon.com/x, read 24 September 2026].\n')
 r=subprocess.run([sys.executable,str(SCRIPT),str(post),str(brief)],capture_output=True,text=True)
 clean=(p/'post-publish.md').read_text(); ledger=brief.read_text()
 check(r.returncode==0,'resolved draft finalizes')
 check('[code:' not in clean and '[author]' not in clean and '[aws-doc:' not in clean,'publish copy has no provenance tags')
 check('src/app.py:10' in ledger and 'docs.aws.amazon.com/x' in ledger,'brief records code and AWS-doc sources')
 check(ledger.count('<!-- claim-sources:start -->')==1,'brief has one generated source table')
print('\nRESULT:','FAIL' if fails else 'PASS',f'({fails} failing)')
sys.exit(1 if fails else 0)
