#!/usr/bin/env python3
"""Import every resource SVG from an official AWS icon ZIP.
Usage: python3 scripts/import_aws_resource_icons.py /path/to/Icon-package_MMDDYYYY.zip
Writes assets/aws-resource-icons/ and its MANIFEST.json. Stdlib only.
"""
import json, re, shutil, sys, tempfile, zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "aws-resource-icons"
if len(sys.argv) != 2:
    raise SystemExit("usage: import_aws_resource_icons.py /path/to/Icon-package_MMDDYYYY.zip")
zpath = Path(sys.argv[1]).resolve()
if not zipfile.is_zipfile(zpath):
    raise SystemExit(f"not a ZIP: {zpath}")
OUT.mkdir(parents=True, exist_ok=True)
with tempfile.TemporaryDirectory() as td:
    with zipfile.ZipFile(zpath) as z:
        z.extractall(td)
    files = [p for p in Path(td).rglob("*.svg")
             if "Resource-Icons_" in str(p) and "__MACOSX" not in p.parts]
    if not files:
        raise SystemExit("no Resource-Icons_* SVGs found")
    names = [p.name for p in files]
    if len(names) != len(set(names)):
        raise SystemExit("duplicate resource filenames; preserve subdirectories in a new importer")
    for old in OUT.glob("*.svg"):
        old.unlink()
    manifest = []
    for src in sorted(files, key=lambda p: p.name):
        dst = OUT / src.name
        shutil.copyfile(src, dst)
        text = dst.read_text(encoding="utf-8")
        cat = next((x for x in src.parts if x.startswith("Res_") and "48_" not in x), "General")
        theme = "dark" if "Dark" in src.name else "light" if "Light" in src.name else "category"
        title = re.sub(r"_(16|32|48|64)(_(Light|Dark))?$", "", src.stem)
        title = title.removeprefix("Res_").replace("-", " ")
        manifest.append({"file": src.name, "resource": title,
                         "category": cat.removeprefix("Res_").replace("-", " "),
                         "theme": theme})
    (OUT / "MANIFEST.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(f"imported {len(manifest)} official AWS resource icons")
