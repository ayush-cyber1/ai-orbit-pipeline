import os
import json

VALID_TYPES = {
    "tools", "tasks", "companies", "news", "videos", "robots",
    "devices", "models", "repositories", "mcp", "collections",
    "personal", "creative"
}

CATEGORY_MAP = {
    "tool": "Tools", "tools": "Tools",
    "model": "Models", "models": "Models",
    "company": "Companies", "companies": "Companies",
    "news": "News",
    "video": "Videos", "videos": "Videos",
    "mcp": "MCP",
    "collection": "Collections", "collections": "Collections",
    "personal": "Personal",
    "creative": "Creative",
}

def normalize_entity_type(entity_type):
    et = (entity_type or "").strip().lower()
    return et if et in VALID_TYPES else "tools"

def normalize_categories(categories):
    seen = []
    for c in categories or []:
        key = c.strip().lower()
        mapped = CATEGORY_MAP.get(key, c.strip().title())
        if mapped not in seen:
            seen.append(mapped)
    return seen

def normalize_record(record):
    record["entity_type"] = normalize_entity_type(record.get("entity_type"))
    record["categories"] = normalize_categories(record.get("categories"))
    return record

def main():
    data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))
    in_path = os.path.join(data_dir, "cleaned.json")
    with open(in_path, "r", encoding="utf-8") as f:
        records = json.load(f)

    normalized = [normalize_record(r) for r in records]

    out_path = os.path.join(data_dir, "normalized.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(normalized, f, indent=2, ensure_ascii=False)

    print(f"normalized {len(normalized)} -> {out_path}")

if __name__ == "__main__":
    main()