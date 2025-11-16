import re
from datetime import datetime

from pyrogram import Client, filters
from pyrogram.types import Message

import FUNCTIONS
import bot
from CLASSES import Band, Bandit
from CONSTANTS import BAND_PANEL
from CONSTANTS import GOAT_BAND_NAMES, GOAT_BAND_CHAT_IDS
from DATABASE import BandDB, UserSettingsDB

band_db=BandDB()
settings_db=UserSettingsDB()

def text_to_band(message)->Band:
    text = message.text
    data = BAND_PANEL.match(text)
    bandits = re.findall(r'(?P<place>.{1,3}) (?P<name>.*)👂(?P<raiting>\d+) (?P<press>.?)(?P<km>\d+)km(\n)?', text)
    arr=[]
    for b in bandits:
        arr.append(Bandit(b[1],int(b[4]), b[3]=='👊'))
    return Band(band_name=data['nickname'], band_id=GOAT_BAND_CHAT_IDS[GOAT_BAND_NAMES.index(data['nickname'])] if data['nickname'] in GOAT_BAND_NAMES else -1, band_members=arr, update_date=message.forward_date)

@bot.bot.on_message(filters.regex(BAND_PANEL) & FUNCTIONS.filters.from_ww_filter.ww_filter())
async def band_panel_processing(client:Client, message:Message):
    this_band=text_to_band(message)
    if FUNCTIONS.filters.check_lvl.is_allowed(2, message.from_user.id):
        if this_band.band_name in GOAT_BAND_NAMES:
            if band_db.save_band(this_band):
                await client.send_message(message.chat.id, f'Записал положение банды {this_band.band_name}', reply_to_message_id=message.id)
            else:
                await client.send_message(message.chat.id, 'Возникла ошибка', reply_to_message_id=message.id)
        else:
            await client.send_message(message.chat.id, 'Это не банда из Острых Пузырей, не приму!', reply_to_message_id=message.id)