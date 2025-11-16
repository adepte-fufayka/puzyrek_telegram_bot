from pyrogram import Client, filters
from pyrogram.types import Message

import bot
from CLASSES import UserSettings
from CONSTANTS import OWNER_ID
from DATABASE import UserSettingsDB
from FUNCTIONS.filters.check_lvl import is_allowed

settings_db= UserSettingsDB()

@bot.bot.on_message(filters.command(['set_role'])&filters.reply)
async def set_role(client: Client, message: Message):
    if is_allowed(2, message.from_user.id) or message.from_user.id in OWNER_ID :
        s = settings_db.find_by_id(message.reply_to_message.from_user.id)
        if s:
            t=message.text.split(" ")
            if len(t)>1:
                settings_db.save(UserSettings(user_id=s.user_id, role=int(t[1]), do_ping=s.do_ping, time_zone=s.time_zone))
                await client.send_message(message.chat.id, "Изменил его роль", reply_to_message_id=message.id)
            else:
                await client.send_message(message.chat.id,"Неправильно введена команда", reply_to_message_id=message.id)
        else:
            await client.send_message(message.chat.id, "Не нашел его у себя", reply_to_message_id=message.id)
    else:
        await client.send_message(message.chat.id, "Не того поля ягода", reply_to_message_id=message.id)

@bot.bot.on_message(filters.command(['set_ping'])&filters.reply)
async def set_role(client: Client, message: Message):
    if is_allowed(2, message.from_user.id) or message.from_user.id in OWNER_ID :
        s = settings_db.find_by_id(message.reply_to_message.from_user.id)
        if s:
                settings_db.save(UserSettings(user_id=s.user_id, role=s.role, do_ping=not s.do_ping, time_zone=s.time_zone))
                await client.send_message(message.chat.id, f"Теперь я его {"не" if s.do_ping else ""} пингую в общем запросе", reply_to_message_id=message.id)
        else:
            await client.send_message(message.chat.id, "Не нашел его у себя", reply_to_message_id=message.id)
    else:
        await client.send_message(message.chat.id, "Это могут делать только командиры!", reply_to_message_id=message.id)