"""Regenerate README table and docs/index.html from data/specs.json."""
import json, pathlib, html
root = pathlib.Path(__file__).resolve().parent.parent
d = json.load(open(root/"data/specs.json")); E = d["entries"]
def v(x): return "—" if x is None else str(x)
def size(e):
    if e["width_mm"] is not None: return f'{e["width_mm"]}×{e["height_mm"]} mm'
    if e["width_px"]: return f'{e["width_px"]}×{e["height_px"]} px'
    if e["min_px"]: return f'≥{e["min_px"]} px'
    return "—"
rows = "\n".join(f'| {e["country"]} | {e["document"]} | {size(e)} | {v(e["head_height_mm"]) + " mm" if e["head_height_mm"] else v(e["head_height_pct"]) + (" %" if e["head_height_pct"] else "")} | {v(e["background"])} | [official]({e["source_url"]}) |' for e in E)
readme = (root/"README.template.md").read_text().replace("{{TABLE}}", rows).replace("{{N}}", str(len(E))).replace("{{C}}", str(len({e['iso2'] for e in E})))
(root/"README.md").write_text(readme)
trs = "\n".join(f'<tr><td>{html.escape(e["country"])}</td><td>{html.escape(e["document"])}</td><td>{html.escape(size(e))}</td><td>{html.escape(v(e["head_height_mm"]) if e["head_height_mm"] else v(e["head_height_pct"]))}</td><td>{html.escape(v(e["background"]))}</td><td>{html.escape(v(e["file_size"]))}</td><td><a href="{html.escape(e["source_url"])}" rel="noopener">Official source</a>' + (f' · <a href="{e["pixid_guide_url"]}">Guide</a>' if e["pixid_guide_url"] else "") + '</td></tr>' for e in E)
ld = {"@context":"https://schema.org","@type":"Dataset","name":"Passport & Visa Photo Specifications (passport-photo-specs)",
 "description":f"Machine-readable passport, visa and ID photo requirements for {len(E)} documents in {len({e['iso2'] for e in E})} countries: print size, pixel dimensions, head height, background, glasses, file limits — each value sourced from an official government page.",
 "url":"https://marfa77.github.io/passport-photo-specs/","license":"https://creativecommons.org/licenses/by/4.0/","isAccessibleForFree":True,"identifier":"https://doi.org/10.5281/zenodo.23321885",
 "keywords":["passport photo","visa photo","photo requirements","biometric photo","ICAO"],"version":d["version"],"dateModified":d["source_checked"],
 "creator":{"@type":"Organization","name":"PixID","url":"https://pixid.studio"},
 "distribution":[{"@type":"DataDownload","encodingFormat":"application/json","contentUrl":"https://raw.githubusercontent.com/marfa77/passport-photo-specs/main/data/specs.json"},
                 {"@type":"DataDownload","encodingFormat":"text/csv","contentUrl":"https://raw.githubusercontent.com/marfa77/passport-photo-specs/main/data/specs.csv"}],
 "spatialCoverage":sorted({e["country"] for e in E})}
page = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Passport & Visa Photo Specifications — open dataset</title>
<meta name="description" content="{html.escape(ld['description'])}">
<script type="application/ld+json">{json.dumps(ld)}</script>
<style>body{{font:15px/1.5 system-ui,sans-serif;margin:0 auto;max-width:1100px;padding:24px;color:#1a1a1a}}h1{{font-size:1.6rem}}
input{{width:100%;padding:10px;font-size:1rem;border:1px solid #bbb;border-radius:6px;margin:12px 0}}table{{border-collapse:collapse;width:100%}}
th,td{{text-align:left;padding:7px 8px;border-bottom:1px solid #e3e3e3;vertical-align:top}}th{{background:#f5f5f5;position:sticky;top:0}}a{{color:#0b5cad}}small{{color:#666}}</style></head>
<body><h1>Passport & Visa Photo Specifications</h1>
<p>Open, machine-readable photo requirements for {len(E)} passport, visa and ID documents across {len({e['iso2'] for e in E})} countries. Every value links to the official government source; unverified values are left blank. Last checked {d["source_checked"]}.
Download <a href="https://github.com/marfa77/passport-photo-specs/blob/main/data/specs.json">JSON</a> · <a href="https://github.com/marfa77/passport-photo-specs/blob/main/data/specs.csv">CSV</a> · <a href="https://github.com/marfa77/passport-photo-specs">GitHub</a>. Data CC BY 4.0. Cite: <a href="https://doi.org/10.5281/zenodo.23321885">DOI 10.5281/zenodo.23321885</a>.</p>
<input id="q" type="search" placeholder="Filter by country or document (e.g. Canada, visa, 35×45)…" aria-label="Filter">
<table id="t"><thead><tr><th>Country</th><th>Document</th><th>Size</th><th>Head height</th><th>Background</th><th>File size</th><th>Links</th></tr></thead><tbody>
{trs}
</tbody></table>
<p><small>Always confirm with the issuing authority before applying — rules change. Need a compliant photo? <a href="https://pixid.studio">Make a compliant photo online with PixID</a>.</small></p>
<script>document.getElementById('q').addEventListener('input',e=>{{const q=e.target.value.toLowerCase();for(const r of document.querySelectorAll('#t tbody tr'))r.style.display=r.textContent.toLowerCase().includes(q)?'':'none'}});</script>
</body></html>'''
(root/"docs/index.html").write_text(page)
print("docs ok")
