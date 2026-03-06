#!/usr/bin/env python3
"""Convert a CSV file into FormIO dropdown JSON files (one per column)."""

from __future__ import annotations

import csv
import json
import re
import unicodedata
from collections import OrderedDict
from pathlib import Path


OUTPUT_DIR = Path("formio-options")
INDEX_FILE = OUTPUT_DIR / "index.json"
SOURCE_CANDIDATES = [
    Path("dropdoewns/Dropdowns.csv"),
    Path("dropdowns/Dropdowns.csv"),
    Path("Dropdowns.csv"),
]


def normalize_ascii(text: str) -> str:
    return unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")


def to_slug(text: str) -> str:
    normalized = normalize_ascii(text).strip().lower()
    slug = re.sub(r"[^a-z0-9]+", "-", normalized).strip("-")
    return slug or "unnamed-column"


def to_camel_value(label: str) -> str:
    normalized = normalize_ascii(label.replace("&", " and "))
    tokens = re.findall(r"[A-Za-z0-9]+", normalized)
    if not tokens:
        return "option"
    head = tokens[0].lower()
    tail = "".join(token.capitalize() for token in tokens[1:])
    return f"{head}{tail}"


def dedupe_labels(values: list[str]) -> list[str]:
    unique = OrderedDict()
    for value in values:
        cleaned = value.strip()
        if cleaned:
            unique.setdefault(cleaned, None)
    return list(unique.keys())


def build_options(labels: list[str]) -> list[dict[str, str]]:
    options: list[dict[str, str]] = []
    used_values: dict[str, int] = {}
    for label in labels:
        base_value = to_camel_value(label)
        count = used_values.get(base_value, 0)
        used_values[base_value] = count + 1
        value = base_value if count == 0 else f"{base_value}{count + 1}"
        options.append({"label": label, "value": value})
    return options


def main() -> None:
    source_csv = next((path for path in SOURCE_CANDIDATES if path.exists()), None)
    if source_csv is None:
        checked = ", ".join(str(path) for path in SOURCE_CANDIDATES)
        raise FileNotFoundError(f"CSV not found. Checked: {checked}")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    with source_csv.open("r", newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        fieldnames = reader.fieldnames or []
        column_data: dict[str, list[str]] = {column: [] for column in fieldnames if column.strip()}

        for row in reader:
            for column in column_data:
                column_data[column].append((row.get(column) or "").strip())

    index: list[dict[str, str | int]] = []
    used_filenames: dict[str, int] = {}

    for column_name, raw_values in column_data.items():
        labels = dedupe_labels(raw_values)
        options = build_options(labels)

        base_name = to_slug(column_name)
        duplicate_count = used_filenames.get(base_name, 0)
        used_filenames[base_name] = duplicate_count + 1
        filename = (
            f"{base_name}.json"
            if duplicate_count == 0
            else f"{base_name}-{duplicate_count + 1}.json"
        )

        output_file = OUTPUT_DIR / filename
        with output_file.open("w", encoding="utf-8") as handle:
            json.dump(options, handle, ensure_ascii=False, indent=2)
            handle.write("\n")

        index.append(
            {
                "columnName": column_name,
                "file": filename,
                "itemCount": len(options),
            }
        )

    with INDEX_FILE.open("w", encoding="utf-8") as handle:
        json.dump(index, handle, ensure_ascii=False, indent=2)
        handle.write("\n")

    print(f"Created {len(index)} dropdown files in {OUTPUT_DIR} from {source_csv}")


if __name__ == "__main__":
    main()
