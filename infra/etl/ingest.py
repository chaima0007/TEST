#!/usr/bin/env python3
"""
ETL skeleton — Ingest external HR DDH sources into KB format.
Usage: python3 infra/etl/ingest.py --source ecovadis --output data/knowledge_base/companies/
"""
from __future__ import annotations
import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

SCHEMA_VERSION = "1.0.0"

def normalize_company(raw: dict, source: str) -> dict:
    """Normalize raw data from any source into KB company schema."""
    return {
        "id": raw.get("slug", raw.get("id", "unknown")),
        "slug": raw.get("slug", "unknown"),
        "name": raw.get("name", ""),
        "country": raw.get("country", ""),
        "city": raw.get("city", ""),
        "sector": raw.get("sector", ""),
        "size": {
            "revenue_bn_eur": raw.get("revenue", 0),
            "employees": raw.get("employees", 0),
            "index": raw.get("stock_index", ""),
        },
        "regulatory_exposure": {
            "csddd": raw.get("csddd", False),
            "csrd": raw.get("csrd", False),
            "lksg": raw.get("lksg", False),
        },
        "pain_points": raw.get("pain_points", []),
        "observed_failures": raw.get("failures", []),
        "signals_of_risk": raw.get("risks", []),
        "signals_of_trust": raw.get("trust", []),
        "recommended_actions": [],
        "local_tone": raw.get("tone", ""),
        "cultural_notes": raw.get("culture", ""),
        "priority": raw.get("priority", 3),
        "last_updated": datetime.now().strftime("%Y-%m-%d"),
        "source_links": raw.get("sources", []),
        "_meta": {
            "schema_version": SCHEMA_VERSION,
            "ingested_from": source,
            "ingested_at": datetime.now().isoformat(),
        },
    }

def ingest(source: str, input_file: str, output_dir: str) -> None:
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    raw_data: list[dict] = []
    with open(input_file, encoding="utf-8") as fh:
        raw_data = json.load(fh)

    for raw in raw_data:
        normalized = normalize_company(raw, source)
        slug = normalized["slug"]
        dest = out / f"{slug}.json"
        dest.write_text(json.dumps(normalized, ensure_ascii=False, indent=2))
        print(f"  v {slug} -> {dest}")

    print(f"\nIngested {len(raw_data)} records from {source}")

def main() -> None:
    p = argparse.ArgumentParser(description="Caelum KB ETL ingest")
    p.add_argument("--source", required=True, help="Source name (ecovadis, msci, manual)")
    p.add_argument("--input", required=True, help="Input JSON file")
    p.add_argument("--output", default="data/knowledge_base/companies/", help="Output dir")
    args = p.parse_args()
    ingest(args.source, args.input, args.output)

if __name__ == "__main__":
    main()
