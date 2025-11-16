
from bot import bot
from pyrogram import Client, filters
from pyrogram.types import Message

ADMIN_CHAT=-1002857571240
class MessageInfo:
    def __init__(self, text:str):
        data=text.split('\n')
        self.chat_id=int(data[1])
        self.message_id=int(data[2])
        self.text="\n".join(data[4:])

@bot.on_message()
async def spam(_, message:Message):
    if message.chat.id != ADMIN_CHAT:
        try:
            await bot.send_message(ADMIN_CHAT, f"{message.chat.title if message.chat.title else '#лс'}\n{message.chat.id}\n{message.id}\n{message.from_user.first_name} {message.from_user.last_name if message.from_user.last_name else ''}\n{message.text}")
        except Exception as e:

            print(e)
