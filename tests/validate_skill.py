#!/usr/bin/env python3
"""Validate every skill in this repo. Stdlib only. Exit 1 on failure."""
import json, os, py_compile, re, sys
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEAK = [(r"(?<![\d.])(?!(?:123456789012)\b)\d{12}(?![\d.])", "account id"),
        (r"arn:aws:[a-z0-9-]*:[a-z0-9-]*:(?!<|x|\$|1234)\d", "real ARN"),
        (r"\b[a-z0-9-]{6,}\.amazonaws\.com\b", "AWS hostname")]
PATTERNS = {"application-serverless.svg", "event-driven.svg", "multi-region-dr.svg",
            "multi-account-landing-zone.svg", "hybrid-network.svg",
            "data-analytics-ml.svg", "cicd-delivery.svg",
            "migration-modernization.svg"}
fails = 0


def check(ok, msg):
    global fails
    fails += not ok
    print(("PASS " if ok else "FAIL ") + msg)


def frontmatter(text):
    m = re.match(r"---\n(.*?)\n---\n", text, re.S)
    if not m:
        return {}
    out = {}
    for line in m.group(1).splitlines():
        if ":" in line and not line.startswith(" "):
            k, v = line.split(":", 1); out[k.strip()] = v.strip()
    return out


def manifest_matches(folder, name_key, exact):
    entries = json.loads((folder / "MANIFEST.json").read_text())
    listed = [e["file"] for e in entries]
    disk = sorted(p.name for p in folder.glob("*.svg"))
    check(len(entries) == exact, f"{folder.name}: {exact} manifest entries")
    check(len(listed) == len(set(listed)), f"{folder.name}: manifest filenames unique")
    check(sorted(listed) == disk, f"{folder.name}: manifest exactly matches SVG files")
    check(all(e.get(name_key) and e.get("category") for e in entries),
          f"{folder.name}: every entry has {name_key} and category")
    return disk


def validate(skill):
    name = skill.name; text = (skill / "SKILL.md").read_text(); fm = frontmatter(text)
    check(fm.get("name") == name, f"{name}: frontmatter name equals folder")
    check(0 < len(fm.get("description", "")) <= 1024,
          f"{name}: description length 1..1024")
    refs = set(re.findall(r"references/([A-Za-z0-9_.-]+\.md)", text))
    missing = [r for r in refs if not (skill / "references" / r).exists()]
    check(not missing, f"{name}: all {len(refs)} named references exist {missing}")

    for py in sorted((skill / "scripts").glob("*.py")):
        try: py_compile.compile(str(py), doraise=True); ok = True
        except py_compile.PyCompileError as e: ok = False; print(e)
        check(ok, f"{name}: {py.name} compiles")
        check(py.stat().st_size < 4096, f"{name}: {py.name} < 4 KB ({py.stat().st_size} B)")
        check(os.access(py, os.X_OK), f"{name}: {py.name} executable")

    assets = skill / "assets"
    svc = manifest_matches(assets / "aws-icons", "service", 304)  # 303 AWS + Strands
    res = manifest_matches(assets / "aws-resource-icons", "resource", 513)
    check(all(re.fullmatch(r"#[0-9A-Fa-f]{6}", e.get("color", ""))
              for e in json.loads((assets / "aws-icons" / "MANIFEST.json").read_text())),
          f"{name}: service icon colours are hex")
    pats = {p.name for p in (assets / "diagram-patterns").glob("*.svg")}
    check(pats == PATTERNS, f"{name}: all 8 diagram patterns, no extras")

    svgs = list(skill.rglob("*.svg")); invalid = []
    for f in svgs:
        try: ET.parse(f)
        except ET.ParseError: invalid.append(str(f.relative_to(skill)))
    check(not invalid, f"{name}: all {len(svgs)} SVGs are XML-valid {invalid[:3]}")

    leaks = []
    for f in list(skill.rglob("*.md")) + svgs + list(skill.rglob("*.json")):
        s = f.read_text(encoding="utf-8", errors="ignore")
        for pat, what in LEAK:
            if re.search(pat, s): leaks.append(f"{f.relative_to(skill)}:{what}")
    check(not leaks, f"{name}: no sensitive identifiers in shipped assets {leaks[:3]}")


skills = [p.parent for p in ROOT.glob("*/SKILL.md")]
check(bool(skills), f"found {len(skills)} skill(s)")
for skill in skills: validate(skill)
print("\nRESULT:", "FAIL" if fails else "PASS", f"({fails} failing)")
sys.exit(1 if fails else 0)
