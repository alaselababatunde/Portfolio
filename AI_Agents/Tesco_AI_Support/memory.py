import sqlite3
import json
import logging
import os
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MemoryManager:
    def __init__(self, db_path="session_memory.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS messages (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        session_id TEXT NOT NULL,
                        role TEXT NOT NULL,
                        content TEXT NOT NULL,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_session_id ON messages(session_id)")
                conn.commit()
        except Exception as e:
            logger.error(f"Failed to init DB: {e}")

    def add_message(self, session_id, role, content):
        """Append a message to the session's history."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO messages (session_id, role, content) VALUES (?, ?, ?)",
                    (session_id, role, content)
                )
                conn.commit()
        except Exception as e:
            logger.error(f"Failed to add message: {e}")

    def get_history(self, session_id, limit=10):
        """Retrieve the last `limit` messages."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                # Get last N messages ordered by time ASC
                cursor.execute(
                    """
                    SELECT role, content FROM (
                        SELECT id, role, content, timestamp 
                        FROM messages 
                        WHERE session_id = ? 
                        ORDER BY id DESC 
                        LIMIT ?
                    ) ORDER BY id ASC
                    """,
                    (session_id, limit)
                )
                rows = cursor.fetchall()
                return [{"role": r["role"], "content": r["content"]} for r in rows]
        except Exception as e:
            logger.error(f"Failed to retrieve history: {e}")
            return []

    def clear_history(self, session_id):
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM messages WHERE session_id = ?", (session_id,))
                conn.commit()
        except Exception as e:
            logger.error(f"Failed to clear history: {e}")
