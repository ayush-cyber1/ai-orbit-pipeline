import os
import json
import re

def enrich_mcp(record):
    record.setdefault("install_method", "npm/pip (see source repo)")
    record.setdefault("runtime_requirements", "Node.js or Python 3.10+")
    return record

def enrich_company(record):
    name = record.get("name", "")
    domain_guess = re.sub(r"[^a-zA-Z0-9]", "", name.split()[0]).lower() if name else ""
    record.setdefault("founding_year", "unknown")
    record.setdefault("industry_sector", "Artificial Intelligence")
    record.setdefault("headquarters", "unknown")
    return record

def enrich_record(record):
    et = record.get("entity_type")
    if et == "mcp":
        record = enrich_mcp(record)
    elif et == "companies":
        record = enrich_company(record)
    return record

def main():
    data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))
    in_path = os.path.join(data_dir, "classified.json")
    with open(in_path, "r", encoding="utf-8") as f:
        records = json.load(f)

    enriched = [enrich_record(r) for r in records]

    out_path = os.path.join(data_dir, "enriched.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(enriched, f, indent=2, ensure_ascii=False)

    print(f"enriched {len(enriched)} -> {out_path}")

if __name__ == "__main__":
    main()