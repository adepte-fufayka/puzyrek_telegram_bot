from typing import List

from pyrogram.types import InlineKeyboardButton
from CONSTANTS import *

raid_types=["ОСНОВА","ЗАПАСКА"]
raid_classes=["💉МИМИКРИРУЕМ", "✅МОЖНО ВСТАТЬ СРАЗУ", "⏰ТАЙМИНГИ"]

class Raid:
    def __init__(self,_id:int, band_name: str, km: str,  _type:str, _class:str):
        """Имя банды, Километр рейда
        тип рейда: ОСНОВА | ЗАПАСКА
        класс рейда: МИМИКРИРУЕМ/МОЖНО ВСТАТЬ СРАЗУ | ТАЙМИНГИ
"""
        self.id=_id
        self.band_name = band_name
        self.km = km
        self._type = _type
        self._class=_class
    def __str__(self):
        return f"""{self._type}
{self.km}
{self._class}
"""
    def to_button(self):
        return InlineKeyboardButton(f"{GOAT_BAND_NAMES_SHORT[GOAT_BAND_NAMES.index(self.band_name)]}:{self._type} {self.km} ", callback_data=f"raid_pin_{self.id}")
    def get_data(self):
        return f"{GOAT_BAND_NAMES.index(self.band_name)}_{LONG_RAID_KMS.index(self.km)}_{raid_types.index(self._type)}_{raid_classes.index(self._class)}"