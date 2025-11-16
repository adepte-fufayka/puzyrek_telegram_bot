import random
import re
from csv import excel

from pyrogram import Client, filters
from pyrogram.enums import ParseMode
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from bot import bot
from CLASSES import Band
from CONSTANTS import GOAT_BAND_CHAT_IDS, GOAT_BAND_NAMES, SHAG_MESSAGE, BOT_WW_USERNAME, GOAT_BAND_NAMES_SHORT, \
    GOAT_BAND_NAMES_LATIN
from DATABASE import UserProfileDB, BandDB, UserSettingsDB
from FUNCTIONS.filters.check_lvl import is_allowed
ALLOWED_LVL=2

#handler say to someone by id
@bot.on_message(filters.regex("/say_(.*)"))
async def private_say(_, message:Message):
    if is_allowed(ALLOWED_LVL, message.from_user.id):
        try:
            t=message.text
            _id=int(t[t.index("_")+1:t.index(" ")])
            await bot.send_message(_id, t[t.index(" ")+1:])
            await message.reply_text('Доставил сообщение пользователю')
        except:
            await message.reply("Возникла ошибка, возможно введен неправильный id или текст")

class Say_Query:
    def __init__(self, string):
        self.is_with_ping=int(string.split('_')[0])
        self.user_id=int(string.split('_')[1])
        self.back_to_id=int(string.split('_')[2])
        self.band_name=GOAT_BAND_CHAT_IDS if string.split('_')[3]=='all' else [GOAT_BAND_CHAT_IDS[GOAT_BAND_NAMES_LATIN.index( string.split('_')[3])]]
#handler say to band_chat
@bot.on_message(filters.command("say"))
async def say(client:Client, message:Message):
    keyboard = InlineKeyboardMarkup(
        [[InlineKeyboardButton(GOAT_BAND_NAMES_SHORT[i], f"say_0_{message.from_user.id}_{message.chat.id}_{GOAT_BAND_NAMES_LATIN[i]}") for i in
          range(len(GOAT_BAND_NAMES_SHORT))], [InlineKeyboardButton('Всем бандам', f'say_0_{message.from_user.id}_{message.chat.id}_all')]])
    if is_allowed(ALLOWED_LVL, message.from_user.id):
        try:
            await message.reply(message.text[5:], reply_markup=keyboard)
        except:
            await message.reply("Возникла ошибка, возможно текст был указан неверно")
#handler say to band_chat with zakrep
@bot.on_message(filters.command("loud_say"))
async def say_with_ping(client:Client, message:Message):
    if is_allowed(ALLOWED_LVL, message.from_user.id):
        try:
            ping_keyboard = InlineKeyboardMarkup(
                [[InlineKeyboardButton(GOAT_BAND_NAMES_SHORT[i], f"say_1_{message.from_user.id}_{message.chat.id}_{GOAT_BAND_NAMES_LATIN[i]}") for i in
                  range(len(GOAT_BAND_NAMES_SHORT))], [InlineKeyboardButton('Всем бандам', f'say_1_{message.from_user.id}_{message.chat.id}_all')]])

            await message.reply(message.text[10:], reply_markup=ping_keyboard)
        except:
            await message.reply("Возникла ошибка, возможно текст был указан неверно")
@bot.on_callback_query(filters.regex("say_(.*)"))
async def say_query_handler(_, q: CallbackQuery):
    say_query = Say_Query(q.data[4:])
    if q.from_user.id ==say_query.user_id:
        try:
            for i in say_query.band_name:
                m= await bot.send_message(i, q.message.text)
                if say_query.is_with_ping:
                    await bot.pin_chat_message(m.chat.id, m.id)
            await q.edit_message_text("Выслал сообщение")
        except:
            await bot.send_message(say_query.back_to_id, "Нет доступа к какому то из чатов")
