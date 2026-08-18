import os
import json
import time
import httpx

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

VALID_TYPES = [
    "tools", "tasks", "companies", "news", "videos", "robots",
    "devices", "models", "repositories", "mcp", "collections",
    "personal", "creative"
]

PROMPT_TEMPLATE = """Classify this AI ecosystem entity. Return ONLY valid JSON, no markdown.

Name: {name}
Description: {description}
Current type: {entity_type}

Valid entity_types: {valid_types}

Return JSON: {{"entity_type": "...", "categories": ["...", "..."]}}
Pick the most accurate entity_type from the valid list. Categories should be 1-3 relevant tags."""

def classify_record(client, record):
    prompt = PROMPT_TEMPLATE.format(
        name=record.get("name", ""),
        description=record.get("description", "")[:300],
        entity_type=record.get("entity_type", ""),
        valid_types=", ".join(VALID_TYPES),
    )
    body = {"contents": [{"parts": [{"text": prompt}]}]}
    try:
        resp = client.post(f"{GEMINI_URL}?key={GEMINI_API_KEY}", json=body, timeout=30)
        if resp.status_code != 200:
            return record
        text = resp.json()["candidates"][0]["content"]["parts"][0]["text"]
        text = text.strip().strip("```json").strip("```").strip()
        result = json.loads(text)
        if result.get("entity_type") in VALID_TYPES:
            record["entity_type"] = result["entity_type"]
        if result.get("categories"):
            record["categories"] = result["categories"]
    except Exception as e:
        print(f"skip ({record.get('name','')[:30]}): {e}")
    return record

def main():
    if not GEMINI_API_KEY:
        print("set GEMINI_API_KEY env var first")
        return

    data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))
    in_path = os.path.join(data_dir, "deduped.json")
    with open(in_path, "r", encoding="utf-8") as f:
        records = json.load(f)

    classified = []
    with httpx.Client() as client:
        for i, record in enumerate(records):
            record = classify_record(client, record)
            classified.append(record)
            if (i + 1) % 10 == 0:
                print(f"classified {i + 1}/{len(records)}")
            time.sleep(1)

    out_path = os.path.join(data_dir, "classified.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(classified, f, indent=2, ensure_ascii=False)

    print(f"classified {len(classified)} -> {out_path}")

if __name__ == "__main__":
    main()