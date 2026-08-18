import os
import json
import httpx
from bs4 import BeautifulSoup
from schema import new_entity

DIRECTORIES = [
    ("https://theresanaiforthat.com", "AI Directory"),
    ("https://www.futurepedia.io", "AI Directory"),
]

HEADERS = {"User-Agent": "Mozilla/5.0"}

def fetch_directory(client, url, source_name, limit=20):
    try:
        resp = client.get(url, headers=HEADERS, timeout=15, follow_redirects=True)
        if resp.status_code != 200:
            print(f"failed ({resp.status_code}): {url}")
            return []
        soup = BeautifulSoup(resp.text, "html.parser")
        records = []
        links = soup.find_all("a", href=True)
        seen = set()
        for link in links:
            text = link.get_text(strip=True)
            href = link["href"]
            if not text or len(text) < 3 or len(text) > 80:
                continue
            if href in seen:
                continue
            if not href.startswith("http"):
                continue
            seen.add(href)
            records.append(new_entity(
                "tools", text, "", href,
                ["Tools", "Collections"], source_name, url
            ))
            if len(records) >= limit:
                break
        return records
    except Exception as e:
        print(f"error: {url} -> {e}")
        return []

def main():
    all_records = []
    with httpx.Client() as client:
        for url, source_name in DIRECTORIES:
            records = fetch_directory(client, url, source_name)
            print(f"{url}: {len(records)} records")
            all_records.extend(records)
    out_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "directories_raw.json"))
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(all_records, f, indent=2, ensure_ascii=False)
    print(f"saved {len(all_records)} -> {out_path}")

if __name__ == "__main__":
    main()