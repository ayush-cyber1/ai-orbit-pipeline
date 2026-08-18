import os
import json

data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))

with open(os.path.join(data_dir, "enriched.json"), "r", encoding="utf-8") as f:
    records = json.load(f)

required_fields = ["id", "entity_type", "name", "url", "categories", "source"]
valid = []
invalid = 0

for r in records:
    ok = True
    for field in required_fields:
        if field not in r or r[field] in [None, "", []]:
            ok = False
    if not r.get("url", "").startswith("http"):
        ok = False
    if ok:
        valid.append(r)
    else:
        invalid += 1

with open(os.path.join(data_dir, "final_entities.json"), "w", encoding="utf-8") as f:
    json.dump(valid, f, indent=2, ensure_ascii=False)

print(f"total: {len(records)}, valid: {len(valid)}, invalid: {invalid}")
print(f"saved -> data/final_entities.json")