import os
import json
import httpx
from schema import new_entity

HF_API = "https://huggingface.co/api/models"

QUERIES = [
    ("text-generation", ["Models", "Tools"]),
    ("text-to-image", ["Models", "Creative"]),
    ("automatic-speech-recognition", ["Models"]),
    ("image-classification", ["Models"]),
    ("text-to-speech", ["Models", "Creative"]),
]

def fetch_query(client, task, categories, limit=20):
    params = {"pipeline_tag": task, "sort": "downloads", "direction": -1, "limit": limit}
    resp = client.get(HF_API, params=params, timeout=30)
    if resp.status_code != 200:
        print(f"failed ({resp.status_code}): {task}")
        return []
    items = resp.json()
    records = []
    for m in items:
        model_id = m.get("id", "")
        url = f"https://huggingface.co/{model_id}"
        extra = {
            "license": (m.get("cardData") or {}).get("license", "unknown"),
            "modalities": [task],
            "provider": model_id.split("/")[0] if "/" in model_id else "unknown",
            "downloads": m.get("downloads"),
        }
        records.append(new_entity(
            "models", model_id, f"{task} model on Hugging Face",
            url, categories, "Hugging Face", url, extra
        ))
    return records

def main():
    all_records = []
    with httpx.Client() as client:
        for task, categories in QUERIES:
            records = fetch_query(client, task, categories)
            print(f"{task}: {len(records)} records")
            all_records.extend(records)
    out_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "huggingface_raw.json"))
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(all_records, f, indent=2, ensure_ascii=False)
    print(f"saved {len(all_records)} -> {out_path}")

if __name__ == "__main__":
    main()