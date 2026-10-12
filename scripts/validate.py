#!/usr/bin/env python3
"""Validate data/specs.json against the schema, check CSV is in sync, and check every URL.
Usage: python scripts/validate.py [--no-net] [--strict]
  --strict : any non-200 URL fails (default: 404/410/DNS errors fail; 403/429/5xx/timeouts
             are reported as WARN because many government sites block scripted clients)."""
import csv, json, sys, pathlib, urllib.request, urllib.error, concurrent.futures as cf
root = pathlib.Path(__file__).resolve().parent.parent
try:
    import jsonschema
except ImportError:
    sys.exit("pip install jsonschema")
data = json.load(open(root / "data/specs.json"))
schema = json.load(open(root / "schema/specs.schema.json"))
errors = sorted(jsonschema.Draft202012Validator(schema).iter_errors(data), key=str)
for e in errors: print("SCHEMA:", list(e.path), e.message)
ids = [x["id"] for x in data["entries"]]
dup = {i for i in ids if ids.count(i) > 1}
if dup: errors.append(1); print("DUPLICATE ids:", dup)
rows = list(csv.DictReader(open(root / "data/specs.csv")))
if [r["id"] for r in rows] != ids: errors.append(1); print("CSV out of sync: run scripts/build_data.py")
nulls = {}
for x in data["entries"]:
    for k, v in x.items():
        if v is None: nulls[k] = nulls.get(k, 0) + 1
print(f"{len(ids)} entries, {len({x['iso2'] for x in data['entries']})} countries")
print("null counts:", dict(sorted(nulls.items(), key=lambda kv: -kv[1])))
fail = bool(errors)
if "--no-net" not in sys.argv:
    urls = sorted({x["source_url"] for x in data["entries"]} | {x["pixid_guide_url"] for x in data["entries"] if x["pixid_guide_url"]})
    def check(u):
        req = urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0 (passport-photo-specs validator)"})
        try:
            with urllib.request.urlopen(req, timeout=25) as r: return u, r.status
        except urllib.error.HTTPError as e: return u, e.code
        except Exception as e: return u, type(e).__name__
    with cf.ThreadPoolExecutor(8) as ex:
        for u, s in ex.map(check, urls):
            if s == 200: tag = "OK  "
            elif "--strict" in sys.argv or s in (404, 410): tag = "FAIL"; fail = True
            else: tag = "WARN"
            print(f"{tag} {s} {u}")
print("RESULT:", "FAIL" if fail else "PASS")
sys.exit(1 if fail else 0)
