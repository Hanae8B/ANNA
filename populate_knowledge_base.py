# populate_knowledge_base.py
import json
import os
from core import kb_entries, neural

DB_FILE = "kb_database.json"

def populate():
    db = {}
    for topic, description in kb_entries.kb_entries.items():
        entry = {"description": description}
        # Optional: create embedding if model is available
        if neural.model is not None:
            try:
                embedding = neural.model.encode([description], convert_to_tensor=True)
                entry["embedding"] = embedding.tolist()  # save as list
            except Exception as e:
                print(f"Embedding failed for topic '{topic}': {e}")
        db[topic] = entry

    # Save database to JSON
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(db, f, indent=2, ensure_ascii=False)

    print(f"Knowledge base updated: {len(db)} topics saved to {DB_FILE}")

if __name__ == "__main__":
    populate()
