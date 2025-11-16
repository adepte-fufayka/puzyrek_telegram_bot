import pyrogram
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

import bot
from DATABASE import UserProfileDB
from FUNCTIONS.filters.check_lvl import is_allowed

db=UserProfileDB()

@bot.bot.on_message(filters.command(['who']) &filters.reply)
async def who(client: Client, message: Message):
    if is_allowed(2, message.from_user.id):
        user=db.find_profile_id(message.reply_to_message.from_user.id)
        if user:
            keyboard=InlineKeyboardMarkup([[InlineKeyboardButton("👀", f"get_short_profile_{user.user_id}")]])
            await message.reply(f"{user.nickname} ID:{user.user_id}",reply_markup=keyboard)
        else:
            await message.reply("Не нашел его у себя в базе данных!")
    else:
        await message.reply("Не того поля ягодка")
@bot.bot.on_callback_query(
    filters.regex("^get_short_profile_(.*)"))
async def get_short_profile(client: Client, query: CallbackQuery):
    user_id=int(query.data.split("_")[3])
    user = db.find_profile_id(user_id
    )
    if is_allowed(2,query.from_user.id):
        if user:
            await query.answer(f"{user.nickname}\nID:{user.user_id}\nБМ:{user.bm()} 🏵{user.zen}\n❤️💪{user.max_hp+user.strength}",  show_alert=True)
        else:
            await query.answer("Не нашел его у себя в базе данных!", show_alert=True)
    else:
        await query.answer("Не того поля ягодка", show_alert=True)