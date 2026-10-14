# passport-photo-specs

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23321885.svg)](https://doi.org/10.5281/zenodo.23321885)

Open, machine-readable **passport, visa and ID photo requirements** — print size, pixel dimensions, head height, background colour, glasses/expression rules and digital upload limits — for **{{N}} documents in {{C}} countries**. Every non-null value comes from an **official government page** (`source_url`), checked on 2026-10-12. If a value could not be verified it is `null`; nothing is guessed.

- `data/specs.json` — canonical data · `data/specs.csv` — generated from JSON
- `schema/specs.schema.json` — JSON Schema (draft 2020-12)
- `scripts/validate.py` — schema + CSV sync + URL checks
- `docs/` — searchable GitHub Pages table

## Interactive demo

Try it on Hugging Face Spaces: [passport-photo-specs](https://huggingface.co/spaces/pablo2319/passport-photo-specs) — pick a country and see its official photo size, head size and background, with source links.

## Summary

| Country | Document | Size | Head height | Background | Source |
|---|---|---|---|---|---|
{{TABLE}}

`verification` tells you how each entry was checked: `official_text_read` (the official page/PDF text was read directly) or `official_search_extract` (values taken from the official page via search-indexed extracts; re-confirm before relying on them). Ranges are strings like `"32-36"`; pixel sizes are `"WIDTHxHEIGHT"`.

## Usage

Python:
```python
import json, urllib.request
url = "https://raw.githubusercontent.com/marfa77/passport-photo-specs/main/data/specs.json"
specs = json.load(urllib.request.urlopen(url))["entries"]
ca = next(s for s in specs if s["id"] == "ca-passport-print")
print(ca["width_mm"], ca["height_mm"], ca["head_height_mm"])  # 50 70 31-36
```

JavaScript:
```js
const { entries } = await (await fetch(
  "https://raw.githubusercontent.com/marfa77/passport-photo-specs/main/data/specs.json")).json();
const visas = entries.filter(e => /visa/i.test(e.document));
console.table(visas.map(({ country, document, width_mm, height_mm }) => ({ country, document, width_mm, height_mm })));
```

Validate locally: `pip install jsonschema && python scripts/validate.py` (`--no-net` skips URL checks, `--strict` fails on any non-200; by default 403/timeouts from bot-protected government sites are warnings).

## Contributing

Edit `scripts/build_data.py` (source of truth), run it to regenerate JSON/CSV, then `python scripts/make_docs.py` and `python scripts/validate.py`. PRs must cite an official government URL. Rules change often — corrections welcome.

## How to cite

> PixID (2026). *passport-photo-specs: Passport & visa photo specifications* (v1.0.0) [Data set]. https://github.com/marfa77/passport-photo-specs

See `CITATION.cff` (GitHub "Cite this repository"). A Zenodo DOI will be added on first release.

## License

Data (`data/`, `docs/` content): [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Code (`scripts/`, `schema/`): MIT. See `LICENSE` and `LICENSE-DATA`.

## Disclaimer

Not legal advice and not affiliated with any government. Always confirm with the issuing authority before applying.

Need a photo that meets these specs? [Make a compliant photo online](https://pixid.studio) with PixID.
