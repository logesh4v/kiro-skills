#!/usr/bin/env python3
"""Finalize a sourced draft. Usage: finalize_blog.py POST.md BRIEF.md
Blocks on [VERIFY], updates the brief's generated claim-source table, and writes
POST-publish.md with internal provenance tags removed. Stdlib only.
"""
import argparse, re, sys
from pathlib import Path

TAG = re.compile(r"\[(code|dash|aws-doc|author|VERIFY)(?::\s*([^\]]*))?\]")
START, END = "<!-- claim-sources:start -->", "<!-- claim-sources:end -->"
ap = argparse.ArgumentParser()
ap.add_argument("post"); ap.add_argument("brief")
a = ap.parse_args(); post = Path(a.post); brief = Path(a.brief)
raw = post.read_text(encoding="utf-8")
verify = [m.group(0) for m in TAG.finditer(raw) if m.group(1) == "VERIFY"]
if verify:
    print(f"FAIL [VERIFY] left: {len(verify)}")
    for v in verify: print(" -", v)
    raise SystemExit(1)

rows = []
for line in raw.splitlines():
    tags = list(TAG.finditer(line))
    if not tags: continue
    claim = TAG.sub("", line).strip().replace("|", "\\|")
    claim = re.sub(r"^[#>*\-\d. ]+", "", claim)
    if len(claim) > 140: claim = claim[:137] + "..."
    for m in tags:
        kind, source = m.group(1), (m.group(2) or "author statement")
        rows.append((claim or "(context line)", kind, source.replace("|", "\\|")))

table = [START, "## Claim sources (generated)", "", "| Claim | Kind | Source |",
         "|---|---|---|"]
for claim, kind, source in rows:
    table.append(f"| {claim} | `{kind}` | {source} |")
table += [END, ""]
block = "\n".join(table)
b = brief.read_text(encoding="utf-8") if brief.exists() else "# Brief\n\n"
if START in b and END in b:
    b = re.sub(re.escape(START) + r".*?" + re.escape(END) + r"\n?", block,
               b, flags=re.S)
else:
    b = b.rstrip() + "\n\n" + block
brief.write_text(b, encoding="utf-8")
clean = TAG.sub("", raw)
out = post.with_name(post.stem + "-publish" + post.suffix)
out.write_text(clean, encoding="utf-8")
print(f"PASS {len(rows)} claim-source rows -> {brief}")
print(f"PASS publish copy -> {out}")
