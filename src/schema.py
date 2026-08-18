import uuid
from datetime import datetime, timezone

def new_entity(entity_type, name, description, url, categories, source_name, source_url, extra=None):
    record = {
        "id": str(uuid.uuid4()),
        "entity_type": entity_type,
        "name": name.strip() if name else "",
        "description": (description or "").strip(),
        "url": url,
        "categories": categories or [],
        "source": {"name": source_name, "url": source_url},
        "ingested_at": datetime.now(timezone.utc).isoformat(),
    }
    if extra:
        record.update(extra)
    return record