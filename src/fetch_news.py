import os
import json
import feedparser
from schema import new_entity

FEEDS = [
    ("https://techcrunch.com/category/artificial-intelligence/feed/", "TechCrunch AI"),
    ("https://www.theverge.com/rss/ai-artificial-intelligence/index.xml", "The Verge AI"),
    ("https://venturebeat.com/category/ai/feed/", "VentureBeat AI"),
]

def fetch_feed(url, source_name, limit=15):
    parsed = feedparser.parse(url)
    records = []
    for entry in parsed.entries[:limit]:
        extra = {
            "published": entry.get("published", ""),
        }
        records.append(new_entity(
            "news", entry.get("title", ""), entry.get("summary", ""),
            entry.get("link", ""), ["News"], source_name, url, extra
        ))
    return records

def main():
    all_records = []
    for url, source_name in FEEDS:
        records = fetch_feed(url, source_name)
        print(f"{source_name}: {len(records)} records")
        all_records.extend(records)
    out_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "news_raw.json"))
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(all_records, f, indent=2, ensure_ascii=False)
    print(f"saved {len(all_records)} -> {out_path}")

if __name__ == "__main__":
    main()