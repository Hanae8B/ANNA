import sqlite3
import numpy as np

class KnowledgeBase:
    def __init__(self, db_path="knowledge.db"):
        self.conn = sqlite3.connect(db_path)
        self._create_table()

    def _create_table(self):
        c = self.conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS knowledge (
                topic TEXT PRIMARY KEY,
                explanation TEXT,
                embedding BLOB
            )
        """)
        self.conn.commit()

    def insert_knowledge(self, topic, explanation, embedding):
        c = self.conn.cursor()
        c.execute("""
            INSERT OR REPLACE INTO knowledge (topic, explanation, embedding)
            VALUES (?, ?, ?)
        """, (topic, explanation, embedding.tobytes() if isinstance(embedding, np.ndarray) else embedding))
        self.conn.commit()

    def get_all_entries(self):
        c = self.conn.cursor()
        c.execute("SELECT topic, explanation FROM knowledge")
        return dict(c.fetchall())

    def close(self):
        self.conn.close()
