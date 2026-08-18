import os
import json
import httpx
from bs4 import BeautifulSoup
from schema import new_entity

SITES = [
    ("https://openai.com", "companies", ["Companies", "Tools"]),
    ("https://www.anthropic.com", "companies", ["Companies", "Tools"]),
    ("https://www.perplexity.ai", "tools", ["Tools"]),
    ("https://www.midjourney.com", "tools", ["Tools", "Creative"]),
    ("https://replit.com", "tools", ["Tools"]),
    ("https://www.notion.so", "tools", ["Tools", "Personal"]),
    ("https://elevenlabs.io", "tools", ["Tools", "Creative"]),
    ("https://www.runwayml.com", "tools", ["Tools", "Creative"]),
]

HEADERS = {"User-Agent": "Mozilla/5.0"}

def fetch_site(client, url, entity_type, categories):
    try:
        resp = client.get(url, headers=HEADERS, timeout=15, follow_redirects=True)
        if resp.status_code != 200:
            print(f"failed ({resp.status_code}): {url}")
            return None
        soup = BeautifulSoup(resp.text, "html.parser")
        title_tag = soup.find("title")
        name = title_tag.text.strip() if title_tag else url

        desc_tag = soup.find("meta", attrs={"name": "description"})
        if not desc_tag:
            desc_tag = soup.find("meta", attrs={"property": "og:description"})
        description = desc_tag.get("content", "").strip() if desc_tag else ""

        return new_entity(
            entity_type, name, description, url,
            categories, "Official Site", url
        )
    except Exception as e:
        print(f"error: {url} -> {e}")
        return None

def main():
    all_records = []
    with httpx.Client() as client:
        for url, entity_type, categories in SITES:
            record = fetch_site(client, url, entity_type, categories)
            if record:
                all_records.append(record)
                print(f"ok: {url}")
    out_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "productsites_raw.json"))
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(all_records, f, indent=2, ensure_ascii=False)
    print(f"saved {len(all_records)} -> {out_path}")

if __name__ == "__main__":
    main()