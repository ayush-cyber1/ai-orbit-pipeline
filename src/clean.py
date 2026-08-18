import os
import json
import re
import glob

def strip_html(text):
    return re.sub(r"<[^>]+>", "", text or "").strip()

def normalize_url(url):
    if not url:
        return ""
    url = url.strip()
    if url.startswith("http://"):
        url = "https://" + url[7:]
    return url.rstrip("/")

def is_valid(record):
    return bool(record.get("name")) and bool(record.get("url"))

def clean_record(record):
    record["name"] = strip_html(record.get("name", "")).strip()
    record["description"] = strip_html(record.get("description", "")).strip()
    record["url"] = normalize_url(record.get("url", ""))
    if record.get("source", {}).get("url"):
        record["source"]["url"] = normalize_url(record["source"]["url"])
    return record

def main():
    data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))
    raw_files = glob.glob(os.path.join(data_dir, "*_raw.json"))

    all_records = []
    for path in raw_files:
        with open(path, "r", encoding="utf-8") as f:
            all_records.extend(json.load(f))

    cleaned = []
    for record in all_records:
        record = clean_record(record)
        if is_valid(record):
            cleaned.append(record)

    out_path = os.path.join(data_dir, "cleaned.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(cleaned, f, indent=2, ensure_ascii=False)

    print(f"merged {len(all_records)} -> cleaned {len(cleaned)} -> {out_path}")

if __name__ == "__main__":
    main()