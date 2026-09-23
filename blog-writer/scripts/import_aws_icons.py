#!/usr/bin/env python3
"""Import every 64px architecture-service SVG from an official AWS icon ZIP.
Usage: python3 scripts/import_aws_icons.py /path/to/Icon-package_MMDDYYYY.zip
Keeps the Strands mark, replaces Arch_*.svg, and rebuilds MANIFEST.json.
Stdlib only; source ZIP must come from https://aws.amazon.com/architecture/icons/.
"""
import json, re, shutil, sys, tempfile, zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "aws-icons"
PREFER = {
    "Arch_AWS-Compute-Optimizer_64.svg": "Arch_Management-Tools",
    "Arch_Amazon-Kinesis-Video-Streams_64.svg": "Arch_Analytics",
}

if len(sys.argv) != 2:
    raise SystemExit("usage: import_aws_icons.py /path/to/Icon-package_MMDDYYYY.zip")
zpath = Path(sys.argv[1]).resolve()
if not zipfile.is_zipfile(zpath):
    raise SystemExit(f"not a ZIP: {zpath}")

with tempfile.TemporaryDirectory() as td:
    with zipfile.ZipFile(zpath) as z:
        z.extractall(td)
    candidates = []
    for p in Path(td).rglob("*.svg"):
        parts = p.parts
        if "Architecture-Service-Icons_" not in str(p) or p.parent.name != "64":
            continue
        if not re.fullmatch(r"Arch_.+_64\.svg", p.name):
            continue
        cat = p.parent.parent.name
        candidates.append((p.name, cat, p))
    if not candidates:
        raise SystemExit("no Architecture-Service-Icons_*/<category>/64/*.svg found")

    selected = {}
    duplicate_notes = {}
    for name, cat, p in sorted(candidates, key=lambda x: (x[0], x[1])):
        if name not in selected or cat == PREFER.get(name):
            if name in selected:
                duplicate_notes[name] = [selected[name][0], cat]
            selected[name] = (cat, p)

    for old in OUT.glob("Arch_*.svg"):
        old.unlink()
    manifest = []
    for name, (cat, src) in sorted(selected.items()):
        dst = OUT / name
        shutil.copyfile(src, dst)
        text = dst.read_text(encoding="utf-8")
        m = re.search(r'<rect[^>]+fill="(#[0-9A-Fa-f]{6})"', text)
        if not m:
            m = re.search(r'fill="(#[0-9A-Fa-f]{6})"', text)
        if not m:
            raise SystemExit(f"no category colour: {name}")
        service = name.removeprefix("Arch_").removesuffix("_64.svg").replace("-", " ")
        manifest.append({"file": name, "service": service,
                         "category": cat.removeprefix("Arch_").replace("-", " "),
                         "color": m.group(1).upper()})

    strands = OUT / "strands-agents-mark.svg"
    if strands.exists():
        manifest.append({"file": strands.name, "service": "Strands Agents",
                         "category": "Non AWS", "color": "#00FF77"})
    (OUT / "MANIFEST.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(f"imported {len(selected)} official AWS service icons")
    print(f"manifest entries: {len(manifest)}")
    for name, cats in duplicate_notes.items():
        print(f"duplicate {name}: selected {selected[name][0]} from {', '.join(cats)}")
