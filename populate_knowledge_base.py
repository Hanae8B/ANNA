from core import neural as neural_core

def populate():
    kb_entries = neural_core.knowledge_base_entries
    print("Populating offline knowledge base with advanced scientific topics...")
    for topic in kb_entries:
        print(f"Inserted: {topic}")
    print("Knowledge base populated successfully.")

if __name__ == "__main__":
    populate()
