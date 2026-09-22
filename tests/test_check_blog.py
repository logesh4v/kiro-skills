#!/usr/bin/env python3
"""Behavioural test for blog-writer/scripts/check_blog.py. Stdlib only.

Runs the linter on the fixtures under tests/fixtures/ and asserts:
  - partner-pass.md  -> exit 0, RESULT: PASS
  - partner-fail.md  -> exit 1 and every expected FAIL line is present
  - builder-fail.md  -> exit 1 and every expected FAIL line is present
Run from the repo root:  python3 tests/test_check_blog.py
"""
import subprocess, sys, tempfile, shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LINT = ROOT / "blog-writer" / "scripts" / "check_blog.py"
FIX = ROOT / "tests" / "fixtures"
fails = 0


def run(fixture, genre):
    # copy to a temp dir so lint-report.txt never lands in the repo
    tmp = Path(tempfile.mkdtemp())
    dst = tmp / fixture
    shutil.copy(FIX / fixture, dst)
    p = subprocess.run([sys.executable, str(LINT), str(dst), "--genre", genre],
                       capture_output=True, text=True)
    shutil.rmtree(tmp, ignore_errors=True)
    return p.returncode, p.stdout


def expect(cond, msg):
    global fails
    fails += not cond
    print(("PASS " if cond else "FAIL ") + msg)


code, out = run("partner-pass.md", "partner")
expect(code == 0 and "RESULT: PASS" in out, "partner-pass.md passes")
if code != 0:
    print(out)

code, out = run("partner-fail.md", "partner")
expect(code == 1, "partner-fail.md exits 1")
for line in ["FAIL banned vocabulary: seamless",
             "FAIL FUD words: bypass",
             "FAIL shared-responsibility line",
             "FAIL no first person",
             "FAIL says 'the AWS Cloud'",
             "FAIL full name first: Amazon S3",
             "FAIL acronym expanded: IAM",
             "FAIL [VERIFY] left: 1",
             "FAIL figures captioned 0/1",
             "FAIL post leak: account id",
             "FAIL post leak: real ARN"]:
    expect(line in out, f"partner-fail.md reports: {line[5:]}")

code, out = run("builder-fail.md", "builder")
expect(code == 1, "builder-fail.md exits 1")
expect("FAIL word budget" in out, "builder-fail.md reports: word budget (too short)")
expect("PASS acronym expanded: KMS" in out, "builder-fail.md accepts '(AWS KMS)' short form")

print("\nRESULT:", "FAIL" if fails else "PASS", f"({fails} failing)")
sys.exit(1 if fails else 0)
