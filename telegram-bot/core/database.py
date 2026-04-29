import sqlite3
import os

class Database:
    """
    Simple persistence layer for user preferences and registered wallets.
    """
    def __init__(self, db_path="bot_data.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    default_wallet TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()

    def set_default_wallet(self, user_id, wallet_id):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "INSERT OR REPLACE INTO users (user_id, default_wallet) VALUES (?, ?)",
                (user_id, wallet_id)
            )
            conn.commit()

    def get_default_wallet(self, user_id):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("SELECT default_wallet FROM users WHERE user_id = ?", (user_id,))
            row = cursor.fetchone()
            return row[0] if row else None
