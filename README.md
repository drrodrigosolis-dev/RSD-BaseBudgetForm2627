# RSD Budget Report 26 - FormIO Dropdown Data

This repository stores JSON files that FormIO can fetch for dropdown options.

## Source and output

- Source CSV: `Dropdowns.csv`
- Generated dropdown JSON files: `formio-options/*.json`
- Column-to-file map: `formio-options/index.json`
- Converter script: `scripts/csv_to_formio_json.py`

## JSON format (FormIO compatible)

Each dropdown file is a JSON array like:

```json
[
  { "label": "Not Indigenous", "value": "notIndigenous" },
  { "label": "Both", "value": "both" }
]
```

This structure is suitable for FormIO select components using `dataSrc: "url"` and `valueProperty: "value"`.

## Regenerate files

```bash
python3 scripts/csv_to_formio_json.py
```
