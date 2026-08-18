import os
import json
import uuid

def find_by_type(records, entity_type):
    return [r for r in records if r.get("entity_type") == entity_type]

def company_develops_tool(records):
    rels = []
    companies = find_by_type(records, "companies")
    tools = find_by_type(records, "tools") + find_by_type(records, "models")
    for company in companies:
        company_name = company.get("name", "").split()[0].lower() if company.get("name") else ""
        for tool in tools:
            tool_source = tool.get("source", {}).get("name", "").lower()
            tool_url = tool.get("url", "").lower()
            if company_name and (company_name in tool_source or company_name in tool_url):
                rels.append({
                    "id": str(uuid.uuid4()),
                    "from_id": company["id"],
                    "from_name": company["name"],
                    "relation": "develops",
                    "to_id": tool["id"],
                    "to_name": tool["name"],
                })
    return rels

def mcp_integrates_tool(records):
    rels = []
    mcps = find_by_type(records, "mcp")
    tools = find_by_type(records, "tools") + find_by_type(records, "repositories")
    for mcp in mcps:
        for tool in tools[:3]:
            rels.append({
                "id": str(uuid.uuid4()),
                "from_id": mcp["id"],
                "from_name": mcp["name"],
                "relation": "integrates_with",
                "to_id": tool["id"],
                "to_name": tool["name"],
            })
    return rels

def tool_solves_task(records):
    rels = []
    tools = find_by_type(records, "tools")
    for tool in tools:
        categories = tool.get("categories", [])
        for cat in categories:
            rels.append({
                "id": str(uuid.uuid4()),
                "from_id": tool["id"],
                "from_name": tool["name"],
                "relation": "solves",
                "to_id": None,
                "to_name": cat,
            })
    return rels

def main():
    data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))
    in_path = os.path.join(data_dir, "enriched.json")
    with open(in_path, "r", encoding="utf-8") as f:
        records = json.load(f)

    relationships = []
    relationships.extend(company_develops_tool(records))
    relationships.extend(mcp_integrates_tool(records))
    relationships.extend(tool_solves_task(records))

    out_path = os.path.join(data_dir, "relationships.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(relationships, f, indent=2, ensure_ascii=False)

    print(f"built {len(relationships)} relationships -> {out_path}")

if __name__ == "__main__":
    main()