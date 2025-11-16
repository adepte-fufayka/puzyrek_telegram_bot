import sqlite3
from typing import Optional, List
from CLASSES import Cupon

class CuponDB:
    def __init__(self, db_path: str = "game_users.db"):
        self.db_path = db_path
        self._create_table()
    def _create_table(self):
        """Создает таблицу, если она не существует"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS Cupon (
                code TEXT ,
                value TEXT,
                used INTEGER
            )
            """)
            conn.commit()
    def save(self, US: Cupon) -> bool:
        """Сохраняет или обновляет профиль пользователя"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT 1 FROM Cupon WHERE code = ?", (US.code,
                                                                          ))
                exists = cursor.fetchone()
                if exists:
                    return False
                else:
                    # Создание нового профиля
                    query = """
                    INSERT INTO Cupon (
                        code, value, used
                    ) VALUES (?, ?, ?)
                    """

                    params = (
                        US.code, US.value, int(US.used)
                    )
                cursor.execute(query, params)
                conn.commit()
                return True

        except sqlite3.Error as e:
            print(e)
            return False
    def find_by_value(self, value:str) -> Optional[Cupon]:
        """Загружает профиль пользователя по ID"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()

                cursor.execute("SELECT * FROM Cupon WHERE value = ?", (value,))
                row = cursor.fetchone()
                if row:
                    return Cupon(
                        value=row["value"],
                        used=bool(row["used"]),
                        code=row["code"]
                    )
                return None

        except sqlite3.Error as e:
            return None
    def delete(self, code: str) -> bool:
        """Удаляет профиль пользователя"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM Cupon WHERE code = ?", (code,))
                conn.commit()
                return cursor.rowcount > 0
        except sqlite3.Error as e:
            return False
    def get_all_values_of_cupons(self)->List[str]:
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                query = "SELECT DISTINCT value FROM Cupon"
                cursor.execute(query)
                return list(set([row[0] for row in cursor.fetchall()]))
        except Exception as e:
            print(f"Ошибка: {e}")
            return []