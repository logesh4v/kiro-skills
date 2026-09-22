#!/usr/bin/env python3
"""Render an SVG architecture diagram to a 2x PNG with headless Chrome.

usage: render_diagram.py figure.svg [--scale 2] [--out figure.png]
Reads width/height from the SVG root; wraps it in an HTML page sized exactly,
screenshots with Chrome. Never use Quick Look/qlmanage for this: it crops.
Stdlib only; needs Chrome/Chromium/Edge installed.
"""
import argparse, re, shutil, subprocess, sys, tempfile
from pathlib import Path

CANDIDATES = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
    "google-chrome", "chromium", "chromium-browser", "chrome", "msedge",
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
]


def find_chrome():
    for c in CANDIDATES:
        if Path(c).exists() or shutil.which(c):
            return c
    sys.exit("no Chrome/Chromium/Edge found; install one or pass --chrome")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("svg"); ap.add_argument("--scale", type=int, default=2)
    ap.add_argument("--out"); ap.add_argument("--chrome")
    a = ap.parse_args()
    svg = Path(a.svg).resolve()
    if not svg.exists():
        sys.exit(f"not found: {svg}")
    head = svg.read_text(encoding="utf-8")[:2000]
    w = re.search(r'\bwidth="(\d+)', head); h = re.search(r'\bheight="(\d+)', head)
    if not (w and h):
        sys.exit("SVG root needs integer width= and height= attributes")
    W, H = int(w.group(1)) * a.scale, int(h.group(1)) * a.scale
    out = Path(a.out) if a.out else svg.with_suffix(".png")
    chrome = a.chrome or find_chrome()

    with tempfile.TemporaryDirectory() as td:
        page = Path(td) / "wrap.html"
        page.write_text(
            "<!doctype html><html><head><meta charset='utf-8'><style>"
            "html,body{margin:0;padding:0;background:#fff}"
            f"img{{display:block;width:{W}px;height:{H}px}}</style></head>"
            f"<body><img src='{svg.as_uri()}'></body></html>", encoding="utf-8")
        cmd = [chrome, "--headless=new", "--disable-gpu", "--hide-scrollbars",
               "--force-device-scale-factor=1", "--allow-file-access-from-files",
               "--default-background-color=FFFFFFFF", f"--window-size={W},{H}",
               f"--screenshot={out}", page.as_uri()]
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    if not out.exists():
        sys.exit(f"render failed:\n{r.stderr[-800:]}")
    print(f"{out}  {W}x{H}  ({out.stat().st_size // 1024} KB)")
    print("NOW OPEN THE PNG AND LOOK: clipped edges? overlapping labels? arrows ending in space?")


if __name__ == "__main__":
    main()
