#!/usr/bin/env python3
"""Lint a blog draft. usage: check_blog.py POST.md --genre builder|partner [--svg f.svg]
Exit 1 on FAIL; writes lint-report.txt. Stdlib only."""
import argparse, re, sys
from pathlib import Path

BUDGET = {"builder": (1800, 2500), "partner": (0, 1800)}
PUFF = ["leading", "best-in-class", "world-class", "seamless", "revolutionary",
        "cutting-edge", "robust", "game-changing", "effortless", "we believe",
        "state-of-the-art", "powerful", "simply", "easily"]
FUD = ["bypass", "exploit", "jailbreak", "attack", "breach"]
FULL = {"Amazon S3": "Amazon Simple Storage Service (Amazon S3)",
        "Amazon ECS": "Amazon Elastic Container Service (Amazon ECS)",
        "Amazon EKS": "Amazon Elastic Kubernetes Service (Amazon EKS)",
        "Amazon RDS": "Amazon Relational Database Service (Amazon RDS)",
        "Amazon SQS": "Amazon Simple Queue Service (Amazon SQS)",
        "Amazon SNS": "Amazon Simple Notification Service (Amazon SNS)",
        "Amazon EC2": "Amazon Elastic Compute Cloud (Amazon EC2)"}
ACR = ["FNOL", "CORS", "SSE", "kNN", "OTP", "CVE", "CSV", "RAG", "CKYC", "IRDAI",
       "VPC", "ALB", "IAM", "KMS", "OCR", "MRZ", "JWT"]
LEAK = [(r"\b\d{12}\b(?<!123456789012)", "account id"),
        (r"arn:aws:[a-z0-9-]*:[a-z0-9-]*:(?!<|x|\$|1234)\d", "real ARN"),
        (r"\b\d{1,3}(\.\d{1,3}){3}/\d{1,2}\b", "CIDR"),
        (r"\b[a-z0-9-]{6,}\.amazonaws\.com\b", "AWS hostname"),
        (r"(?i)(secret|token|password)\s*[:=]\s*\S", "credential")]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("post"); ap.add_argument("--genre", required=True, choices=BUDGET)
    ap.add_argument("--svg"); a = ap.parse_args()
    raw = Path(a.post).read_text(encoding="utf-8")
    body = re.sub(r"```.*?```|<!--.*?-->", "", raw, flags=re.S)
    body = re.sub(r"^>.*$", "", body, flags=re.M)
    flat = re.sub(r"\s+", " ", body); low = flat.lower()
    out, fail = [], False

    def rep(ok, msg):
        nonlocal fail; fail |= not ok
        out.append(("PASS " if ok else "FAIL ") + msg)

    n = len(re.findall(r"[A-Za-z0-9'\u2019]+", re.sub(r"[#*|`_\[\]-]", " ", flat)))
    lo, hi = BUDGET[a.genre]
    rep(lo <= n <= hi, f"word budget {n} (genre {a.genre}: {lo}-{hi})")
    if a.genre == "partner" and n > 1500:
        out.append(f"WARN  {n} words > 1,500 AWS ideal - justify to reviewer")
    h = [p for p in PUFF if re.search(r"\b%s\b" % re.escape(p), low)]
    rep(not h, "banned vocabulary" + (": " + ", ".join(h) if h else ""))
    if a.genre == "partner":
        h = [p for p in FUD if re.search(r"\b%s\b" % p, low)]
        rep(not h, "FUD words" + (": " + ", ".join(h) if h else ""))
        rep("shared responsibility" in low, "shared-responsibility line")
        rep(not re.search(r"\b([Ii]|[Ww]e) (built|set out|hit)\b", flat), "no first person")
    rep("the cloud" not in low.replace("the aws cloud", ""), "says 'the AWS Cloud'")
    for s, f in FULL.items():
        i, j = flat.find(s), flat.find(f)
        if i != -1:
            rep(j != -1 and j <= i, f"full name first: {s}")
    for ac in ACR:
        if re.search(r"\b%s\b" % ac, flat):
            rep(re.search(r"\((AWS |Amazon )?%s\)" % ac, flat) is not None, f"acronym expanded: {ac}")
    v = len(re.findall(r"\[VERIFY[^\]]*\]", raw))
    rep(v == 0, f"[VERIFY] left: {v}")
    figs, caps = re.findall(r"!\[[^\]]*\]\([^)]+\)", raw), re.findall(r"\*Figure \d+:", raw)
    rep(len(caps) >= len(figs), f"figures captioned {len(caps)}/{len(figs)}")
    for pat, name in LEAK:
        rep(not re.search(pat, raw), f"post leak: {name}")
    if a.svg and Path(a.svg).exists():
        svg = Path(a.svg).read_text(encoding="utf-8")
        for pat, name in LEAK:
            rep(not re.search(pat, svg), f"svg leak: {name}")
        rep("linearGradient" not in svg, "svg icons flat")
    Path(a.post).with_name("lint-report.txt").write_text("\n".join(out) + "\n")
    print("\n".join(out)); print("\nRESULT:", "FAIL" if fail else "PASS")
    sys.exit(1 if fail else 0)


if __name__ == "__main__":
    main()
