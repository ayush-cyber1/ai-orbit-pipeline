import asyncio
import os
import json
import httpx
from schema import new_entity

GITHUB_API = "https://api.github.com/search/repositories"
TOKEN = os.environ.get("GITHUB_TOKEN")

HEADERS = {"Accept": "application/vnd.github+json"}
if TOKEN:
    HEADERS["Authorization"] = f"Bearer {TOKEN}"

QUERIES = [
    ("machine learning framework stars:>500", "repositories", ["Models", "Tools"]),
    ("mcp server model context protocol", "mcp", ["MCP"]),
    ("llm agent framework stars:>300", "repositories", ["Tools", "Personal"]),
    ("computer vision stars:>300", "repositories", ["Models", "Tools"]),
    ("ai robotics stars:>200", "robots", ["Robots"]),
    ("mcp tool integration", "mcp", ["MCP"]),
]

async def fetch_query(client, query, entity_type, categories, per_page=20):
    params = {"q": query, "sort": "stars", "order": "desc", "per_page": per_page}
    resp = await client.get(GITHUB_API, params=params, headers=HEADERS, timeout=30)
    if resp.status_code != 200:
        print(f"failed ({resp.status_code}): {query}")
        return []
    items = resp.json().get("items", [])
    records = []
    for repo in items:
        extra = {
            "stars": repo.get("stargazers_count"),
            "primary_language": repo.get("language"),
            "last_updated": repo.get("updated_at"),
        }
        records.append(new_entity(
            entity_type, repo.get("full_name"), repo.get("description") or "",
            repo.get("html_url"), categories, "GitHub", repo.get("html_url"), extra
        ))
    return records

async def main():
    all_records = []
    async with httpx.AsyncClient() as client:
        for query, entity_type, categories in QUERIES:
            records = await fetch_query(client, query, entity_type, categories)
            print(f"{entity_type}: {len(records)} records")
            all_records.extend(records)
            await asyncio.sleep(1)
    out_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "github_raw.json"))
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(all_records, f, indent=2, ensure_ascii=False)
    print(f"saved {len(all_records)} -> {out_path}")

if __name__ == "__main__":
    asyncio.run(main())