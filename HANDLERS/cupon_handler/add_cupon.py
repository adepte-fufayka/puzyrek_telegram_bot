import re

import pyrogram.enums
from pyrogram import Client, filters, types
from pyrogram.types import Message, InlineKeyboardButton, CallbackQuery

import bot
from CLASSES import Cupon
from CONSTANTS import RUKOVODSTVO_CHAT_ID, NOT_IN_USER_DATABASE
from DATABASE import CuponDB
from DATABASE import UserProfileDB, UserSettingsDB
from FUNCTIONS.filters.check_lvl import is_allowed

db=CuponDB()
user_db=UserProfileDB()
settings=UserSettingsDB()
@bot.bot.on_message(filters.private & filters.command(["add_cupon"]))
async def add_cupon(c: Client, m: Message):
    detected_persons = re.findall(r'/gcard(?P<code>.*) 💈×(?P<value>\d*)', m.text)
    a=[db.save(Cupon(code=i[0], value=i[1], used=False)) for i in detected_persons]
    if all(a):
        await m.reply("записал все купоны")
    else:
        text='Возникла ошибка при записи следующих купонов:\n'
        for i in range(len(a)):
            if not a[i]:
               text+=f'/gcard{detected_persons[i][0]}\n'
        await m.reply(text)
@bot.bot.on_message(filters.command(["get_cupon"]))
async def get_cupon(c: Client, m: Message):
    if user_db.find_profile_id(m.from_user.id):
        values_of_cupon = db.get_all_values_of_cupons()
        if values_of_cupon:
            keyboard = types.InlineKeyboardMarkup([[InlineKeyboardButton(i, f"get_cupon_{i}_{m.from_user.id}") for i in values_of_cupon], [InlineKeyboardButton('Отмена','cancel')]])
            await m.reply(f'Комментарий к запросу: {m.text[10:] if m.text[10:] else "-"}\nВыбери сколько пупсов хочешь получить:', reply_markup=keyboard)
        else:
            await m.reply("Купонов нет в наличии")
    else:
        await m.reply(NOT_IN_USER_DATABASE)
@bot.bot.on_callback_query(filters.regex("get_cupon_(.*)"))
async def get_cupon_query(_, q: CallbackQuery):
    cupon_value=q.data.split('_')[2]
    _id=int(q.data.split('_')[3])
    if q.from_user.id != _id:
        return
    try:
        keyboard=types.InlineKeyboardMarkup([[InlineKeyboardButton('✅',f'cupon_accept_{_id}_{cupon_value}'),InlineKeyboardButton('⛔️',f'cupon_decline_{_id}_{cupon_value}')]])
        await bot.bot.send_message(RUKOVODSTVO_CHAT_ID, f'{user_db.find_profile_id(_id).nickname}:{_id}\nЗапрашивает {cupon_value}💈\nКомментарий: {re.split('Комментарий к запросу: |Выбери сколько пупсов хочешь получить:',q.message.text)[1]}', reply_markup=keyboard)
        await q.edit_message_text("Запрос успешно отправлен руководству!")
    except Exception as e:
        await q.edit_message_text("Возникла ошибка(вероятная причина - Флю лох!)")
@bot.bot.on_callback_query(filters.regex("cupon_decline_(.*)"))
async def cupon_decline(_, q: CallbackQuery):
    if is_allowed(3, q.from_user.id):
        cupon_value=q.data.split('_')[3]
        _id=int(q.data.split('_')[2])
        try:
            user=user_db.find_profile_id(_id)
            if user:
                await bot.bot.send_message(_id, f"К сожалению руководство отклонило твою заявку на купон в {cupon_value} пупсов💈")
                await q.edit_message_text(f"Запрос от игрока на {cupon_value}💈 отклонен\n{user.nickname}\nID:{_id}")
            else:
                await q.edit_message_text("Пользователя нет в базе данных")
        except Exception as e:
            await bot.bot.send_message(RUKOVODSTVO_CHAT_ID, f"Не смог доставить сообщение пользователю {_id}")
@bot.bot.on_callback_query(filters.regex("cupon_accept_(.*)"))
async def cupon_accept(_, q: CallbackQuery):
    if  is_allowed(3, q.from_user.id):
        cupon_value=q.data.split('_')[3]
        _id=int(q.data.split('_')[2])
        try:
            c=db.find_by_value(cupon_value)
            if c:
                user=user_db.find_profile_id(_id)
                if user:
                    await bot.bot.send_message(_id, f"Купон по запросу: <a href='https://t.me/WastelandWarsBot?text=/gcard{c.code}'>/gcard{c.code}</a>", parse_mode=pyrogram.enums.ParseMode.HTML, disable_web_page_preview=True)
                    await q.edit_message_text(f'#купон на {c.value} выдан игроку\n{user.nickname}\nID:{_id}')
                    db.delete(c.code)
                else:
                    await q.edit_message_text("Пользователь был удален из базы данных")
                    await bot.bot.send_message(_id, NOT_IN_USER_DATABASE)
            else:
                await bot.bot.send_message(_id, f"К сожалению купоны с такой стоимостью закончились, попробуй выбрать какой нибудь другой")
        except Exception as e:
            await bot.bot.send_message(RUKOVODSTVO_CHAT_ID, f"Не смог доставить сообщение пользователю {_id}")
