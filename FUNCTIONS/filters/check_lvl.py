from pyrogram.types import Message

from DATABASE import UserSettingsDB


def is_allowed(allowed_level:int,_id:int) -> bool:
    settings_db= UserSettingsDB()
    settings=settings_db.find_by_id(_id)
    return settings and settings.role>=allowed_level