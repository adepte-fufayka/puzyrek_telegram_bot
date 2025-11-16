import random
import re
from typing import List

from pyrogram import Client, filters
from pyrogram.enums import ParseMode
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

import bot
from CLASSES import Band
from CONSTANTS import GOAT_BAND_CHAT_IDS, GOAT_BAND_NAMES, GOAT_BAND_NAMES_SHORT, GOAT_BAND_NAMES_LATIN, RAID_KMS
from DATABASE import UserProfileDB, BandDB, UserSettingsDB
from FUNCTIONS.filters.check_lvl import is_allowed

user_db = UserProfileDB()
band_db = BandDB()
ALLOWED_LEVEL=2
goat_bands = [InlineKeyboardButton(GOAT_BAND_NAMES_SHORT[i], f"RAID_TRACKER_{GOAT_BAND_NAMES_LATIN[i]}") for i in
              range(len(GOAT_BAND_NAMES))]
goat_bands_short = [InlineKeyboardButton(GOAT_BAND_NAMES_SHORT[i]+"👊", f"RAID_TRACKER_{GOAT_BAND_NAMES_LATIN[i]}_SHORT") for i in
              range(len(GOAT_BAND_NAMES))]
keyboard = InlineKeyboardMarkup([goat_bands, [InlineKeyboardButton('Все банды', f"RAID_TRACKER_ALL"), InlineKeyboardButton('Рейд-Точки', f"RAID_TRACKER_ALL_SHORT")], goat_bands_short])

@bot.bot.on_message(filters.command('raid_tracker'))
async def raid_tracker(_, message:Message):
    if is_allowed(ALLOWED_LEVEL, message.from_user.id):
        await message.reply("Флю лох", reply_markup=keyboard)
    else:
        await message.reply("Не того поля ягодка!")

def _band_to_tracker(chosen:str)-> str:
    short="SHORT" in chosen
    chosen=chosen.replace("_SHORT","")
    arr=[band_db.find_all_band_name(GOAT_BAND_NAMES[GOAT_BAND_NAMES_LATIN.index(chosen)])[-1]] if chosen in GOAT_BAND_NAMES_LATIN else [band_db.find_all_band_name(i)[-1] for i in GOAT_BAND_NAMES]
    kms=RAID_KMS if short else [i for i in range(152)]
    text='Рейд трекер:\n\n'
    for km in kms:
        cnt, bm, zen = 0, 0, 0
        pr_cnt, pr_bm, pr_zen = 0, 0, 0
        on_raid = ''
        for band in arr:
            for bandit in band.band_members:
                if km==bandit.km or short and int(km[1:]) == bandit.km:
                    if short:
                        if bandit.voevat_suda:
                            prof = user_db.find_profile_name(bandit.name)
                            pr_cnt += 1
                            cnt += 1
                            zen += prof.zen if prof else 0
                            pr_zen += prof.zen if prof else 0
                            pr_bm += prof.bm() if prof else 0
                            bm += prof.bm() if prof else 0
                            on_raid += f"{cnt}. {bandit.name} 👊{str(prof.bm()) if prof else ''} {'🏵' + str(prof.zen) if prof else ''}\n"
                        else:
                            prof = user_db.find_profile_name(bandit.name)
                            cnt += 1
                            bm += prof.bm() if prof else 0
                            zen += prof.zen if prof else 0
                            on_raid += f"{cnt}. {bandit.name} 📍{str(prof.bm()) if prof else ''} {'🏵' + str(prof.zen) if prof else ''}\n"
                    else:
                        if cnt:
                            on_raid+=f"{' '*2*(len(str(km))+3)}|{bandit.name}\n"
                            cnt += 1
                        else:
                            on_raid += f"{km}📍|{bandit.name}\n"
                            cnt += 1
        if on_raid:
            text+=f"{f'{km} 👥{pr_cnt}/{cnt} 👊{pr_bm}/{bm} 🏵{pr_zen}/{zen}\n{on_raid}\n' if short else f'{on_raid}'}"
    return text
@bot.bot.on_callback_query(filters.regex("^RAID_TRACKER_(.*)"))
async def raid_tracker(_, query: CallbackQuery):
    if is_allowed(ALLOWED_LEVEL, query.from_user.id ):
        chosen=query.data[13:]
        text=_band_to_tracker(chosen)
        await query.message.edit(text=text,reply_markup=keyboard ,disable_web_page_preview=True)