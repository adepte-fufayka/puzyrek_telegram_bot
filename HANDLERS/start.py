from pyrogram import filters
from pyrogram.types import Message
import bot
@bot.bot.on_message(filters.command(['start']))
async def start(client, message: Message):
    await client.send_message(
            chat_id=message.chat.id,
            text="Привет и добро пожаловать!\nСкинь мне свой полный пип-бой в ЛС",
            reply_to_message_id=message.id
        )