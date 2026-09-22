#!/usr/bin/env python3
"""Validate every skill in this repo. Stdlib only. Exit 1 on any failure.

Checks, per <skill>/SKILL.md:
  - frontmatter has name == folder name, description 1..1024 chars
  - every references/*.md the procedure names exists
  - scripts/*.py compile, are < 4096 bytes, and are executable
  - assets/aws-icons/MANIFEST.json matches the files on disk exactly
  - no account id / real ARN / hostname leaks in any .md/.svg/.json
Run from the repo root:  python3 tests/validate_skill.py
"""
import json, py_compile, re, sys, os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEAK = [(r"\b\d{12}\b(?<!123456789012)", "account id"),
        (r"arn:aws:[a-z0-9-]*:[a-z0-9-]*:(?!<|x|\$|1234)\d", "real ARN"),
        (r"\b[a-z0-9-]{6,}\.amazonaws\.com\b", "AWS hostname")]
fails = 0


def check(ok, msg):
    global fails
    fails += not ok
    print(("PASS " if ok else "FAIL ") + msg)


def frontmatter(text):
    m = re.match(r"---\n(.*?)\n---\n", text, re.S)
    if not m:
        return {}
    fm = {}
    for line in m.group(1).splitlines():
        if ":" in line and not line.startswith(" "):
            k, v = line.split(":", 1)
            fm[k.strip()] = v.strip()
    return fm


def validate(skill: Path):
    name = skill.name
    text = (skill / "SKILL.md").read_text(encoding="utf-8")
    fm = frontmatter(text)
    check(fm.get("name") == name, f"{name}: frontmatter name == folder ({fm.get('name')!r})")
    d = fm.get("description", "")
    check(0 < len(d) <= 1024, f"{name}: description length {len(d)} (1..1024)")

    for ref in set(re.findall(r"references/([A-Za-z0-9_.-]+\.md)", text)):
        check((skill / "references" / ref).exists(), f"{name}: references/{ref} exists")

    for py in sorted((skill / "scripts").glob("*.py")) if (skill / "scripts").exists() else []:
        try:
            py_compile.compile(str(py), doraise=True)
            ok = True
        except py_compile.PyCompileError as e:
            ok = False
            print("      ", e)
        check(ok, f"{name}: {py.name} compiles")
        check(py.stat().st_size < 4096, f"{name}: {py.name} < 4 KB ({py.stat().st_size} B)")
        check(os.access(py, os.X_OK), f"{name}: {py.name} executable")

    man = skill / "assets" / "aws-icons" / "MANIFEST.json"
    if man.exists():
        entries = json.loads(man.read_text())
        listed = {e["file"] for e in entries}
        on_disk = {p.name for p in man.parent.glob("*.svg")}
        check(listed == on_disk, f"{name}: MANIFEST.json matches icon files "
              f"(missing on disk: {sorted(listed - on_disk)}, unlisted: {sorted(on_disk - listed)})")
        for e in entries:
            check(re.fullmatch(r"#[0-9A-Fa-f]{6}", e.get("color", "")) is not None,
                  f"{name}: {e['file']} has a hex colour")

    for f in list(skill.rglob("*.md")) + list(skill.rglob("*.svg")) + list(skill.rglob("*.json")):
        s = f.read_text(encoding="utf-8", errors="ignore")
        for pat, what in LEAK:
            check(not re.search(pat, s), f"{name}: no {what} in {f.relative_to(skill)}")


skills = [p.parent for p in ROOT.glob("*/SKILL.md")]
check(bool(skills), f"found {len(skills)} skill(s)")
for s in skills:
    validate(s)
print("\nRESULT:", "FAIL" if fails else "PASS", f"({fails} failing)")
sys.exit(1 if fails else 0)
