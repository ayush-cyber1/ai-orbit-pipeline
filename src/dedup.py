import os
import json
from rapidfuzz import fuzz

SIMILARITY_THRESHOLD = 85

def normalize_name(name):
    return (name or "").strip().lower()

def merge_records(primary, duplicate):
    if len(duplicate.get("description", "")) > len(primary.get("description", "")):
        primary["description"] = duplicate["description"]
    merged_categories = list(dict.fromkeys(primary.get("categories", []) + duplicate.get("categories", [])))
    primary["categories"] = merged_categories
    primary.setdefault("merged_sources", [primary["source"]["name"]])
    if duplicate["source"]["name"] not in primary["merged_sources"]:
        primary["merged_sources"].append(duplicate["source"]["name"])
    return primary

def deduplicate(records):
    result = []
    for record in records:
        match_found = False
        norm_name = normalize_name(record.get("name"))
        for existing in result:
            if existing.get("entity_type") != record.get("entity_type"):
                continue
            existing_norm = normalize_name(existing.get("name"))
            score = fuzz.ratio(norm_name, existing_norm)
            if score >= SIMILARITY_THRESHOLD:
                merge_records(existing, record)
                match_found = True
                break
        if not match_found:
            result.append(record)
    return result

def main():
    data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))
    in_path = os.path.join(data_dir, "normalized.json")
    with open(in_path, "r", encoding="utf-8") as f:
        records = json.load(f)

    deduped = deduplicate(records)

    out_path = os.path.join(data_dir, "deduped.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(deduped, f, indent=2, ensure_ascii=False)

    print(f"{len(records)} -> {len(deduped)} after dedup -> {out_path}")

if __name__ == "__main__":
    main()