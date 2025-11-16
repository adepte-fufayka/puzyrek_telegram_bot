import sqlite3
from datetime import datetime
from typing import Optional, List
from CONSTANTS import LINE_SPLITTER
from CLASSES import Band, Bandit


class BandDB:
    def __init__(self, db_path: str = "game_users.db"):
        self.db_path = db_path
        self._create_table()
        self._update_table()
    def _update_table(self):
        """Добавляет новые столбцы, если они отсутствуют"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                # Убираем PRIMARY KEY constraint с band_chat_id
                cursor.execute("PRAGMA foreign_keys=off")

                # Создаем временную таблицу с новой структурой
                cursor.execute("""
                                    CREATE TABLE IF NOT EXISTS band_new (
                                        band_chat_id INTEGER,
                                        band_name TEXT,
                                        band_members TEXT,
                                        update_date TEXT
                                    )
                                """)

                # Переносим данные из старой таблицы
                cursor.execute("""
                                    INSERT INTO band_new (band_chat_id, band_name, band_members, update_date)
                                    SELECT band_chat_id, band_name, band_members, update_date FROM band
                                """)

                # Удаляем старую таблицу и переименовываем новую
                cursor.execute("DROP TABLE IF EXISTS band")
                cursor.execute("ALTER TABLE band_new RENAME TO band")
                cursor.execute("PRAGMA foreign_keys=on")
                conn.commit()
        except sqlite3.OperationalError as e:
            if "duplicate column name" in str(e):
                print("Столбец уже существует - пропускаем")
            else:
                print(f"Ошибка обновления таблицы: {e}")
    def _create_table(self):
        """Создает таблицу, если она не существует"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS band (
                band_chat_id INTEGER,
                band_name TEXT,
                band_members TEXT,
                update_date TEXT DEFAULT '2025-06-27 03:57:24'
            )
            """)
            conn.commit()

    def save_band(self, band: Band) -> bool:
        """Сохраняет или обновляет профиль пользователя"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                updated_at_str = band.update_date.strftime('%Y-%m-%d %H:%M:%S')
                cursor.execute("SELECT 1 FROM band WHERE band_name = ? AND update_date = ?", (band.band_name,updated_at_str))

                exists = cursor.fetchone()
                if exists:
                    return False
                # Создание нового профиля
                query = """
                INSERT INTO band (
                    band_chat_id, band_name, band_members, update_date
                ) VALUES (?, ?, ?, ?)
                """

                params = (
                    band.band_id, band.band_name, str(band), updated_at_str
                )
                cursor.execute(query, params)
                conn.commit()
                return True

        except sqlite3.Error as e:
            print(e)
            return False

    def find_all_band_name(self, name: str) -> List [Band]:
        """Загружает профиль пользователя по ID"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()

                cursor.execute("SELECT * FROM band WHERE band_name = ?", (name,))
                rows = cursor.fetchall()
                arr=[]
                for row in rows:
                    if row:
                        updated_at = datetime.strptime(row["update_date"], "%Y-%m-%d %H:%M:%S")
                        c=row["band_members"].split(LINE_SPLITTER)
                        arr.append( Band(
                            band_id=row["band_chat_id"],
                            band_name=row["band_name"],
                            band_members=[Bandit(c[0+i], int(c[1+i]), c[2+i]=='True'
                        )for i in range(0,len(c)-2, 3)],
                            update_date=updated_at
                        ))
                return arr

        except sqlite3.Error as e:
            return []