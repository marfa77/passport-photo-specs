---
license: cc-by-4.0
pretty_name: Passport & Visa Photo Specifications
language: [en]
size_categories: [n<1K]
task_categories: [tabular-classification]
tags: [passport, visa, photo-requirements, biometrics, icao, government, open-data]
configs:
  - config_name: default
    data_files:
      - split: train
        path: specs.csv
---

# Passport & Visa Photo Specifications

Machine-readable passport, visa and ID photo requirements for 22 documents in 15 countries: print size (mm), pixel dimensions, dpi, head height, background, glasses and expression rules, digital file format/size limits. Each row has a `source_url` pointing to an official government page and `source_checked` = 2026-10-12. Unverified values are null — nothing is guessed. `verification` = `official_text_read` or `official_search_extract`.

**Source & updates:** https://github.com/marfa77/passport-photo-specs

**Columns:** id, country, iso2, document, width_mm, height_mm, width_px, height_px, min_px, max_px, dpi, head_height_mm, head_height_pct, eye_line, background, glasses, expression, digital_format, file_size, source_url, source_checked, pixid_guide_url, verification, notes.

**Limitations:** requirements change and vary by mission/consulate; always confirm with the issuing authority. Not legal advice.

**Citation:** PixID (2026). passport-photo-specs (v1.0.0) [Data set].

Maintained by [PixID](https://pixid.studio).
