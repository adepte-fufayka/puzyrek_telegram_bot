from pyrogram import filters, Client
from pyrogram.types import Message

from FUNCTIONS.filters.check_lvl import is_allowed
from bot import bot

READ_THE_DOCS = 'https://teletype.in/@adepte_fufayka/erBErUcliyy'
READ_THE_OFFICER_DOCS = "https://teletype.in/@adepte_fufayka/i_EADwQy2Zk"


@bot.on_message(filters.command("help"))
async def help_command(_: Client, message: Message):
    await message.reply(
        f'Пользовательская документация:\n{READ_THE_DOCS}\n\n{f"Админская документация:\n{READ_THE_OFFICER_DOCS}" if is_allowed(2, message.from_user.id) else ""}')
