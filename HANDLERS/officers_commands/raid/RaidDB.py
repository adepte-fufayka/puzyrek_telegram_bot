import sqlite3
from typing import Optional, List
from .RaidClass import Raid


class RaidDB:
    def __init__(self, db_path: str = "game_users.db"):
        self.db_path = db_path
        self._create_table()

    def _create_table(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS Raid (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                band_name TEXT,
                km TEXT,
                type TEXT,
                class TEXT
            )
            """)
            conn.commit()

    def save(self, r: Raid) -> bool:
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM Raid WHERE id = ?", (r.id,))
                exists = cursor.fetchone()
                if exists:
                    query = """
                                    UPDATE Raid SET
                                        band_name = ?,
                                        km = ?,
                                        type = ?,
                                        class = ?
                                    WHERE id = ?
                                    """
                    params = (r.band_name, r.km, r._type, r._class,r.id )
                else:
                    query = """
                    INSERT INTO Raid (
                        id, band_name, km, type, class
                    ) VALUES (?, ?, ?, ?, ?)
                    """
                    params = (r.id, r.band_name, r.km, r._type, r._class)
                cursor.execute(query, params)
                conn.commit()
                return True
        except sqlite3.Error as e:
            print(e)
            return False

    def find_by_name(self, name: str) -> List[Raid]:
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM Raid WHERE band_name = ?", (name,))
                rows = cursor.fetchall()
                r = []
                if rows:
                    for row in rows:
                        if row:
                            r.append(Raid(int(row["id"]), row["band_name"], row["km"], row["type"], row["class"]))
                    return r
                return []
        except sqlite3.Error as e:
            return []

    def find_by_id(self, id: int) -> Optional[Raid]:
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursos = conn.cursor()
                cursos.execute("SELECT * FROM Raid WHERE id = ?", (id,))
                row = cursos.fetchone()
                if row:
                    return Raid(row["id"], row["band_name"], row["km"], row["type"], row["class"])
                else:
                    return None
        except sqlite3.Error as e:
            return None

    def delete_all_by_name(self, band_name: str) -> bool:
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM Raid WHERE band_name = ?", (band_name,))
                conn.commit()
                return cursor.rowcount > 0
        except sqlite3.Error as e:
            return False

    def delete_by_id(self, _id: int) -> bool:
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM Raid WHERE id = ?", (_id,))
                conn.commit()
                return cursor.rowcount > 0
        except sqlite3.Error as e:
            return False
