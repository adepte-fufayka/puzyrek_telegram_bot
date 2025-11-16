import sqlite3
from datetime import datetime
from typing import Optional

from CLASSES import UserProfile


class UserProfileDB:
    def __init__(self, db_path: str = "game_users.db"):
        self.db_path = db_path
        self._create_table()

    def _create_table(self):
        """Создает таблицу, если она не существует"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_profiles (
                user_id INTEGER PRIMARY KEY,
                nickname TEXT NOT NULL UNIQUE,
                fraction_emoji TEXT DEFAULT '⚔️',
                fraction_name TEXT DEFAULT 'Без фракции',
                gang_name TEXT DEFAULT 'Одиночка',
                max_hp INTEGER DEFAULT 5,
                damage INTEGER DEFAULT 1,
                armor INTEGER DEFAULT 0,
                strength INTEGER DEFAULT 5,
                accuracy INTEGER DEFAULT 2,
                charisma INTEGER DEFAULT 5,
                dexterity INTEGER DEFAULT 5,
                max_energy INTEGER DEFAULT 22,
                zen INTEGER DEFAULT 0,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """)
            conn.commit()

    def save_profile(self, profile: UserProfile) -> bool:
        """Сохраняет или обновляет профиль пользователя"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                # Форматируем дату для SQLite
                updated_at_str = profile.updated_at.strftime("%Y-%m-%d %H:%M:%S")

                # Проверяем существование пользователя
                cursor.execute("SELECT 1 FROM user_profiles WHERE user_id = ?", (profile.user_id,))
                exists = cursor.fetchone()

                if exists:
                    # Обновление существующего профиля
                    query = """
                    UPDATE user_profiles SET
                        nickname = ?,
                        fraction_emoji = ?,
                        fraction_name = ?,
                        gang_name = ?,
                        max_hp = ?,
                        damage = ?,
                        armor = ?,
                        strength = ?,
                        accuracy = ?,
                        charisma = ?,
                        dexterity = ?,
                        max_energy = ?,
                        zen = ?,
                        updated_at = ?
                    WHERE user_id = ?
                    """
                    params = (
                        profile.nickname,
                        profile.fraction_emoji,
                        profile.fraction_name,
                        profile.gang_name,
                        profile.max_hp,
                        profile.damage,
                        profile.armor,
                        profile.strength,
                        profile.accuracy,
                        profile.charisma,
                        profile.dexterity,
                        profile.max_energy,
                        profile.zen,
                        updated_at_str,
                        profile.user_id
                    )
                else:
                    # Создание нового профиля
                    query = """
                    INSERT INTO user_profiles (
                        user_id, nickname, fraction_emoji, fraction_name, gang_name,
                        max_hp, damage, armor, strength, accuracy, charisma, dexterity,
                        max_energy, zen, updated_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """
                    params = (
                        profile.user_id,
                        profile.nickname,
                        profile.fraction_emoji,
                        profile.fraction_name,
                        profile.gang_name,
                        profile.max_hp,
                        profile.damage,
                        profile.armor,
                        profile.strength,
                        profile.accuracy,
                        profile.charisma,
                        profile.dexterity,
                        profile.max_energy,
                        profile.zen,
                        updated_at_str
                    )

                cursor.execute(query, params)
                conn.commit()
                return True

        except sqlite3.Error as e:
            return False

    def find_profile_id(self, user_id: int) -> Optional[UserProfile]:
        """Загружает профиль пользователя по ID"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()

                cursor.execute("SELECT * FROM user_profiles WHERE user_id = ?", (user_id,))
                row = cursor.fetchone()

                if row:
                    # Конвертируем строку даты в объект datetime
                    updated_at = datetime.strptime(row["updated_at"], "%Y-%m-%d %H:%M:%S")

                    return UserProfile(
                        user_id=row["user_id"],
                        nickname=row["nickname"],
                        fraction_emoji=row["fraction_emoji"],
                        fraction_name=row["fraction_name"],
                        gang_name=row["gang_name"],
                        max_hp=row["max_hp"],
                        damage=row["damage"],
                        armor=row["armor"],
                        strength=row["strength"],
                        accuracy=row["accuracy"],
                        charisma=row["charisma"],
                        dexterity=row["dexterity"],
                        max_energy=row["max_energy"],
                        zen=row["zen"],
                        updated_at=updated_at
                    )
                return None

        except sqlite3.Error as e:
            return None

    def find_profile_name(self, user_id: str) -> Optional[UserProfile]:
        """Загружает профиль пользователя по ID"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()

                cursor.execute("SELECT * FROM user_profiles WHERE nickname = ?", (user_id,))
                row = cursor.fetchone()

                if row:
                    # Конвертируем строку даты в объект datetime
                    updated_at = datetime.strptime(row["updated_at"], "%Y-%m-%d %H:%M:%S")

                    return UserProfile(
                        user_id=row["user_id"],
                        nickname=row["nickname"],
                        fraction_emoji=row["fraction_emoji"],
                        fraction_name=row["fraction_name"],
                        gang_name=row["gang_name"],
                        max_hp=row["max_hp"],
                        damage=row["damage"],
                        armor=row["armor"],
                        strength=row["strength"],
                        accuracy=row["accuracy"],
                        charisma=row["charisma"],
                        dexterity=row["dexterity"],
                        max_energy=row["max_energy"],
                        zen=row["zen"],
                        updated_at=updated_at
                    )
                return None

        except sqlite3.Error as e:
            return None

    def delete_profile(self, user_id: int) -> bool:
        """Удаляет профиль пользователя"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM user_profiles WHERE user_id = ?", (user_id,))
                conn.commit()
                return cursor.rowcount > 0
        except sqlite3.Error as e:
            return False