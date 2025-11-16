import re
from datetime import datetime

from pyrogram import Client, filters
from pyrogram.types import Message

import FUNCTIONS
import bot
from CONSTANTS import VIEW, MOSCOW
from DATABASE.UsersDB import UserProfileDB
from CONSTANTS import FRAC_CHAT_IDS

from CLASSES import UserProfile
from CONSTANTS import GOAT_BAND_NAMES

db= UserProfileDB()

async def is_in_goat(user:UserProfile):
    return user and user.gang_name in GOAT_BAND_NAMES

async def parse_view_data(message:Message, view_date:datetime):
    text = message.text
    detected_persons = re.findall(r'(?P<name>.*) \| 👤(?P<code>.*);( \n)?', text)
    match = VIEW.search(text)
    if not match:
        return None
    groups = match.groupdict()
    line=f'{groups["zone"]}{groups["kilometr"]} ⏳{(datetime(view_date.year,view_date.month, view_date.day, view_date.hour, view_date.minute, view_date.second, tzinfo=MOSCOW)).strftime("%H:%M:%S %d/%m")}\n'
    mims=re.search(r'(❔Неизвестный ×(?P<mimics_count>\d*))', text)
    found_mimics = mims.groupdict()['mimics_count'] if mims else []
    mimics = int(found_mimics if found_mimics else 0)
    not_mims=re.search(r"(\.\.\.И еще (?P<not_mimics>\d*) выживших\.)", text)
    found_not_mimics = not_mims.groupdict()['not_mimics'] if not_mims else []
    not_mimics = int(found_not_mimics if found_not_mimics else 0)
    all_count = mimics + not_mimics + len(detected_persons)+1
    line += f"Ситуация на точке:\n➖💉{mimics}/{all_count}\n"
    allies=[]
    enemies=[]
    for l in detected_persons:
        if (not ('⚙️' in l[0]) and message.chat.id in FRAC_CHAT_IDS)or (not message.chat.id in FRAC_CHAT_IDS and not(await is_in_goat(db.find_profile_name(l[0][1:].replace('\uFE0F', ''))))):
            enemies.append(l)
        else:
            allies.append(l)
    if enemies:
        line+='🔪Подрезать:\n' if '🚷' in text else '🥊Перчатку:\n'
    for l in enemies:
            line += f"➖<a href='https://t.me/WastelandWarsBot?text=/p_{l[1][3:]}'>{l[0]}</a>\n"
    if allies:
        line+='🍻Союзники:\n'
    for l in allies:
        line += f'➖{l[0]}\n'
    line+=f"Вью от {message.from_user.first_name}"
    return line

@bot.bot.on_message(filters.regex(VIEW) & FUNCTIONS.filters.from_ww_filter.ww_filter())
async def view(client: Client, message: Message):
    await bot.bot.send_message(message.chat.id, await parse_view_data(message, message.forward_date), disable_web_page_preview=True)
    await message.delete()