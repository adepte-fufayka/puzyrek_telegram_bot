import random
import re
from typing import List

from pyrogram import Client, filters
from pyrogram.enums import ParseMode
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

import bot
from CLASSES import Band
from CONSTANTS import *
from DATABASE import UserProfileDB, BandDB, UserSettingsDB
from FUNCTIONS.filters.check_lvl import is_allowed

user_db = UserProfileDB()
band_db = BandDB()
settings_db = UserSettingsDB()


async def do_you_sleep(client: Client, bands: List[Band], allowed_kms, comment=''):
    for band in bands:
        count = 0
        fl = True
        not_found = ''
        pingulina = comment+'\n\n'
        for i in band.band_members:
            found_user = user_db.find_profile_name(i.name)
            if found_user:
                found_settings = settings_db.find_by_id(found_user.user_id)
                if i.km not in allowed_kms and found_settings.do_ping:
                    pingulina += f'<a href="tg://user?id={found_user.user_id}">{found_user.nickname}</a>{", " + SHAG_MESSAGE[random.randint(0, len(SHAG_MESSAGE) - 1)] + "!\n" if not comment else ", " if count < 4 else ""}'
                    count += 1
                if count == 5:
                    fl = False
                    count = 0
                    pingulina += f"\n{BOT_WW_USERNAME}"
                    await client.send_message(band.band_id, pingulina, parse_mode=ParseMode.HTML)
                    pingulina = comment+'\n\n'
            else:
                not_found += i.name + '\n'
        if count > 0:
            fl = False
            pingulina=pingulina[:-1]
            pingulina += f"\n{BOT_WW_USERNAME}"
            await client.send_message(band.band_id, pingulina, parse_mode=ParseMode.HTML)
        if fl:
            await client.send_message(band.band_id, 'Все на своих местах')
        if not_found:
            not_found = 'Не нашел у себя:\n' + not_found
            await client.send_message(band.band_id, not_found)


async def get_allowed_km(text: str):
    a = []
    comment=text.split(';')[1] if ';' in text else ''
    if len(text) > 5:
        s = text[5:]
        kms = re.split(',', s)
        for km in kms:
            z = km.split(' ')
            l = []
            for i in z:
                if i:
                    l.append(i)
            if len(l) == 1:
                a.append(int(l[0]))
            if len(l) == 2:
                for i in range(int(l[0]), int(l[1]) + 1):
                    a.append(i)
    return a, comment


@bot.bot.on_message(filters.command(['ping']))
async def ping(client: Client, message: Message):
    if is_allowed(2, message.from_user.id):
        if message.chat.id in GOAT_BAND_CHAT_IDS:
            b_name = GOAT_BAND_NAMES[GOAT_BAND_CHAT_IDS.index(message.chat.id)]
            if band_db.find_all_band_name(b_name):
                band = sorted(band_db.find_all_band_name(b_name), key=lambda x: x.update_date)[-1]
                allowed_kms, comment = await get_allowed_km(message.text)
                await do_you_sleep(client, [band], allowed_kms, comment)
        else:
            keyboard = InlineKeyboardMarkup(
                [[InlineKeyboardButton(GOAT_BAND_NAMES[i], f"ping_command {message.from_user.id} {i}") for i in
                  range(len(GOAT_BAND_NAMES))],
                 [InlineKeyboardButton('Все банды', f'ping_command {message.from_user.id} all')]])
            await bot.bot.send_message(message.chat.id, 'Выбери банду:', reply_markup=keyboard, reply_to_message_id=message.id)
    else:
        await message.reply("Не того поля ягодка")


class PingCommandQuery:
    def __init__(self, string):
        data = string.split(' ')
        self.id = int(data[1])
        self.isAll = data[2] == 'all'
        self.band = GOAT_BAND_NAMES[int(data[2])] if not self.isAll else ""



@bot.bot.on_callback_query(filters.regex('^ping_command'))
async def ping_command(client: Client, query: CallbackQuery):
    q = PingCommandQuery(query.data)
    if q.id == query.from_user.id:
        if is_allowed(2, q.id):
            original_message = await bot.bot.get_messages(query.message.chat.id, query.message.reply_to_message_id)
            text=original_message.text
            allowed_kms, comment = await get_allowed_km(text)
            if q.isAll:
                bands=[sorted(band_db.find_all_band_name(name), key=lambda x: x.update_date)[-1] for name in GOAT_BAND_NAMES]
                await do_you_sleep(client, bands, allowed_kms, comment)
            else:
                if band_db.find_all_band_name(q.band):
                    band = sorted(band_db.find_all_band_name(q.band), key=lambda x: x.update_date)[-1]
                    await do_you_sleep(client, [band], allowed_kms, comment)
