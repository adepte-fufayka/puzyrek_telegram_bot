from pyrogram import Client, filters
from pyrogram.types import Message

import bot
from DATABASE import UserProfileDB
from CONSTANTS import NOT_IN_USER_DATABASE
db = UserProfileDB()

@bot.bot.on_message(filters.command(['me']) | filters.regex("^📟Пип-бой$"))
async def me(client:Client, message: Message):

    prof=db.find_profile_id(message.from_user.id)
    if prof:
        await client.send_message(chat_id=message.chat.id,text=str(prof),reply_to_message_id=message.id )
    else:
        await client.send_message(chat_id=message.chat.id,text=NOT_IN_USER_DATABASE, reply_to_message_id=message.id )