# passport-photo-specs

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23321885.svg)](https://doi.org/10.5281/zenodo.23321885)

Open, machine-readable **passport, visa and ID photo requirements** — print size, pixel dimensions, head height, background colour, glasses/expression rules and digital upload limits — for **22 documents in 15 countries**. Every non-null value comes from an **official government page** (`source_url`), checked on 2026-10-12. If a value could not be verified it is `null`; nothing is guessed.

- `data/specs.json` — canonical data · `data/specs.csv` — generated from JSON
- `schema/specs.schema.json` — JSON Schema (draft 2020-12)
- `scripts/validate.py` — schema + CSV sync + URL checks
- `docs/` — searchable GitHub Pages table

## Interactive demo

Try it on Hugging Face Spaces: [passport-photo-specs](https://huggingface.co/spaces/pablo2319/passport-photo-specs) — pick a country and see its official photo size, head size and background, with source links.

## Summary

| Country | Document | Size | Head height | Background | Source |
|---|---|---|---|---|---|
| United States | Passport | 51×51 mm | 25-35 mm | plain white or off-white | [official](https://travel.state.gov/content/travel/en/passports/how-apply/photos.html) |
| United States | Visa (DS-160 nonimmigrant) | 51×51 mm | 22-35 mm | plain white or off-white | [official](https://travel.state.gov/content/travel/en/us-visas/visa-information-resources/photos/digital-image-requirements.html) |
| United States | Diversity Visa (DV Lottery) | 600×600 px | 22-35 mm | plain white or off-white | [official](https://travel.state.gov/content/travel/en/us-visas/visa-information-resources/photos.html) |
| United Kingdom | Passport (online) | ≥600x750 px | — | plain light-coloured, clear contrast | [official](https://www.gov.uk/photos-for-passports) |
| Canada | Passport (print) | 50×70 mm | 31-36 mm | plain white or light-coloured | [official](https://www.canada.ca/en/immigration-refugees-citizenship/services/canadian-passports/photos.html) |
| Canada | Passport (online renewal) | ≥1200x1800 px | 45-50 % | plain white or light-coloured | [official](https://www.canada.ca/en/immigration-refugees-citizenship/services/canadian-passports/photos.html) |
| Canada | Visa (IRCC temporary resident) | 35×45 mm | 31-36 mm | plain white or light-coloured | [official](https://www.canada.ca/en/immigration-refugees-citizenship/services/application/application-forms-guides/temporary-resident-visa-application-photograph-specifications.html) |
| Australia | Passport | 35-40×45-50 mm | 32-36 mm | — | [official](https://www.passports.gov.au/help/passport-photos) |
| India | Passport (Passport Seva upload) | 630×810 px | 80-85 (face) % | white | [official](https://mportal.passportindia.gov.in/pdf/Guidelines_for_ICAO_Compliant_Photographs_for_Passport_Applications.pdf) |
| Nigeria | Passport (online upload) | 600×800 px | — | white | [official](https://passport.immigration.gov.ng/image-compliance) |
| Germany | Passport | 35×45 mm | 32-36 mm | — | [official](https://www.bundesdruckerei-gmbh.de/files/dokumente/pdf/fotomustertafel-300dpi.pdf) |
| Germany | ID card (Personalausweis) | 35×45 mm | 32-36 mm | — | [official](https://www.bundesdruckerei-gmbh.de/files/dokumente/pdf/fotomustertafel.pdf) |
| France | Passport | 35×45 mm | 32-36 mm | — | [official](https://www.service-public.gouv.fr/particuliers/vosdroits/F10619) |
| France | ID card (CNI) | 35×45 mm | 32-36 mm | — | [official](https://www.service-public.gouv.fr/particuliers/vosdroits/F10619) |
| Netherlands | Passport / ID card | 35×45 mm | 26-30 mm | light grey, light blue or white; uniform | [official](https://www.rijksoverheid.nl/themas/migratie-en-reizen/paspoort-en-identiteitskaart/eisen-pasfoto-paspoort-id-kaart) |
| China | Visa | 33×48 mm | 28-33 mm | white or close to white, no frame | [official](https://www.visaforchina.cn/SYD4_EN/qianzhengyewu/jichuzhishi/changjianwenti/552371235904950309.html) |
| Brazil | Visa (e-Visa, consular) | 51×51 mm | — | white | [official](https://www.gov.br/mre/pt-br/embaixada-viena/vistos/e-visa) |
| Ireland | Passport (print) | 35-38×45-50 mm | — | — | [official](https://www.ireland.ie/en/dfa/passports/photo-guidelines/) |
| Ireland | Passport (online) | ≥715x951 px | — | — | [official](https://www.ireland.ie/en/dfa/passports/photo-guidelines/) |
| New Zealand | Passport (digital) | ≥900x1200 px | — | plain, light-coloured | [official](https://passports.govt.nz/passport-photos/check-your-photo-meets-the-technical-requirements) |
| Singapore | Passport / IC (e-Services) | 400×514 px | — | — | [official](https://www.ica.gov.sg/photo-guidelines) |
| Saudi Arabia | Visa (tourist eVisa) | 200×200 px | 70-80 (face) % | white, no pattern | [official](https://visa.visitsaudi.com/Home/PhotoSpecifications) |

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
