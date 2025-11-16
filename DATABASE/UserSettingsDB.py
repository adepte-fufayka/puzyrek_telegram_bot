import sqlite3
from typing import Optional
from CLASSES import UserSettings

class UserSettingsDB:
    def __init__(self, db_path: str = "game_users.db"):
        self.db_path = db_path
        self._create_table()
    def _create_table(self):
        """Создает таблицу, если она не существует"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS UserSettings (
                id INTEGER PRIMARY KEY,
                role INTEGER,
                time_zone INTEGER,
                do_ping TEXT
            )
            """)
            conn.commit()
    def save(self, US: UserSettings) -> bool:
        """Сохраняет или обновляет профиль пользователя"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT 1 FROM UserSettings WHERE id = ?", (US.user_id,
                                                                          ))
                exists = cursor.fetchone()
                if exists:
                    query = """
                    UPDATE UserSettings SET
                        id = ?,
                        role = ?,
                        time_zone = ?,
                        do_ping = ?
                    WHERE id = ?
                    """
                    params = (
                        US.user_id, US.role, US.time_zone, str(US.do_ping),US.user_id
                    )
                else:
                    # Создание нового профиля
                    query = """
                    INSERT INTO UserSettings (
                        id, role, time_zone, do_ping
                    ) VALUES (?, ?, ?, ?)
                    """

                    params = (
                        US.user_id, US.role, US.time_zone, str(US.do_ping)
                    )
                cursor.execute(query, params)
                conn.commit()
                return True

        except sqlite3.Error as e:
            print(e)
            return False
    def find_by_id(self, n_id:int) -> Optional[UserSettings]:
        """Загружает профиль пользователя по ID"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()

                cursor.execute("SELECT * FROM UserSettings WHERE id = ?", (n_id,))
                row = cursor.fetchone()

                if row:
                    return UserSettings(
                        user_id=row["id"],
                        role=row["role"],
                        time_zone=row["time_zone"],
                        do_ping=row["do_ping"] == "True"
                    )
                return None

        except sqlite3.Error as e:
            return None
    def delete(self, id: int) -> bool:
        """Удаляет профиль пользователя"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM UserSettings WHERE id = ?", (id,))
                conn.commit()
                return cursor.rowcount > 0
        except sqlite3.Error as e:
            return False