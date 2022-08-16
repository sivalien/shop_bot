import sqlite3
from typing import Dict

import telegram_bot.config as cfg

class Database():
    def __init__(self, db_name: str = cfg.DB_NAME) -> None:
        self.db_name = db_name
        self._create_table()

    def _create_table(self):
        with sqlite3.connect(self.db_name) as conn:
            query = """
                CREATE TABLE IF NOT EXISTS shop_item_number(
                userid INT,
                shop TEXT,
                item_number INT
                );
            """
            conn.execute(query)

    def add(self, id: int, shop: str, number: int) -> None:
        with sqlite3.connect(self.db_name) as conn:
            conn.execute(
                'INSERT INTO shop_item_number VALUES (?, ?, ?)',
                (id, shop, number)
            )

    def get_shop_item_numbers(self, id: int) -> Dict[str, int]:
         with sqlite3.connect(self.db_name) as conn:
            cur = conn.cursor()
            cur.execute(
                'SELECT shop, item_number FROM shop_item_number WHERE userid==?', 
                (id,),
            )
            return dict(cur.fetchall())