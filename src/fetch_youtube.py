import os
import json
import httpx
from schema import new_entity

YT_API = "https://www.googleapis.com/youtube/v3/search"
API_KEY = os.environ.get("YOUTUBE_API_KEY")

QUERIES = [
    ("AI tool tutorial", ["Videos", "Tools"]),
    ("AI model demo", ["Videos", "Models"]),
    ("AI startup review", ["Videos", "Companies"]),
]

def fetch_query(client, query, categories, max_results=15):
    params = {
        "part": "snippet",
        "q": query,
        "type": "video",
        "maxResults": max_results,
        "key": API_KEY,
    }
    resp = client.get(YT_API, params=params, timeout=30)
    if resp.status_code != 200:
        print(f"failed ({resp.status_code}): {query}")
        return []
    items = resp.json().get("items", [])
    records = []
    for item in items:
        video_id = item.get("id", {}).get("videoId")
        if not video_id:
            continue
        snippet = item.get("snippet", {})
        url = f"https://www.youtube.com/watch?v={video_id}"
        extra = {
            "channel": snippet.get("channelTitle", ""),
            "published": snippet.get("publishedAt", ""),
        }
        records.append(new_entity(
            "videos", snippet.get("title", ""), snippet.get("description", ""),
            url, categories, "YouTube", url, extra
        ))
    return records

def main():
    if not API_KEY:
        print("set YOUTUBE_API_KEY env var first")
        return
    all_records = []
    with httpx.Client() as client:
        for query, categories in QUERIES:
            records = fetch_query(client, query, categories)
            print(f"{query}: {len(records)} records")
            all_records.extend(records)
    out_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "youtube_raw.json"))
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(all_records, f, indent=2, ensure_ascii=False)
    print(f"saved {len(all_records)} -> {out_path}")

if __name__ == "__main__":
    main()