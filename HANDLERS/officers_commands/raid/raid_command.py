import random
import re
from datetime import datetime

from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from bot import bot
from CONSTANTS import *
from .RaidDB import RaidDB
from .RaidClass import Raid, raid_types, raid_classes

raid_db = RaidDB()
from FUNCTIONS.filters.check_lvl import is_allowed

ALLOWED_LVL = 2


async def get_text_and_buttons_from_database():
    now_time = datetime.now(tz=MOSCOW)
    morning = (((now_time.timestamp() - datetime(now_time.year, now_time.month, now_time.day, 9, now_time.minute,
                                                 now_time.second, tzinfo=MOSCOW).timestamp()) < 0)
               and ((now_time.timestamp() - datetime(now_time.year, now_time.month, now_time.day, 1, now_time.minute,
                                                     now_time.second, tzinfo=MOSCOW).timestamp()) > 0))
    text = f"Пины козла {GOAT_NAME} на {'09:00' if morning else '01:00'} {now_time.strftime('%d.%m.%Y')}\n"
    keyboard_buttons = []
    for band_names in GOAT_BAND_NAMES:
        band_pins = ""
        this_band_pins = raid_db.find_by_name(band_names)
        for i in this_band_pins:
            band_pins += str(i) + "\n"
            keyboard_buttons.append([i.to_button()])
        if band_pins:
            text += band_names + '\n' + band_pins + '\n'
        else:
            text += f"Для {band_names} пинов не нашел\n\n"
    keyboard_buttons.append([InlineKeyboardButton("Добавить пин", f"add_pin")])
    keyboard_buttons.append([InlineKeyboardButton("Разослать пины", f"send_pins")])
    return text, keyboard_buttons


@bot.on_message((filters.command('raid') | filters.regex(r"^{CREATE_PIN}")) & filters.private)
async def raid(_: Client, message: Message):
    if is_allowed(allowed_level=ALLOWED_LVL, _id=message.from_user.id):
        text, keyboard_buttons = await get_text_and_buttons_from_database()
        await message.reply(text, reply_markup=InlineKeyboardMarkup(keyboard_buttons))
    else:
        await message.reply("<UNK> <UNK> <UNK> <UNK> <UNK> <UNK>")


@bot.on_callback_query(filters.regex(r"^send_pins"))
async def send_pins(_, q: CallbackQuery):
    kb = [[InlineKeyboardButton("✅ДА", f"apply_raid_send")],
          [InlineKeyboardButton("❌НЕТ", "decline_raid_send")]]
    await q.edit_message_text("Уверен, что надо отправить пины?", reply_markup=InlineKeyboardMarkup(kb))


@bot.on_callback_query(filters.regex(r"^apply_raid_send"))
async def apply_raid_send(_, q: CallbackQuery):
    await q.edit_message_text("Отправляю пины...")
    now_time = datetime.now(tz=MOSCOW)
    morning = (((now_time.timestamp() - datetime(now_time.year, now_time.month, now_time.day, 9, now_time.minute,
                                                 now_time.second, tzinfo=MOSCOW).timestamp()) < 0)
               and ((now_time.timestamp() - datetime(now_time.year, now_time.month, now_time.day, 1, now_time.minute,
                                                     now_time.second, tzinfo=MOSCOW).timestamp()) > 0))
    for band_names in GOAT_BAND_NAMES:
        band_pins = ""
        this_band_pins = raid_db.find_by_name(band_names)
        for i in this_band_pins:
            band_pins += str(i) + "\n"
        if band_pins:
            m=await bot.send_message(GOAT_BAND_CHAT_IDS[GOAT_BAND_NAMES.index(band_names)], f"КОЗЛОВЫЙ ПИН({'09:00' if morning else '01:00'})\n{band_pins}")
            await bot.pin_chat_message(m.chat.id, m.id)
    await q.edit_message_text("Пины разосланы!")


@bot.on_callback_query(filters.regex(r"^decline_raid_send"))
async def decline_raid_send(_, q: CallbackQuery):
    text, keyboard = await get_text_and_buttons_from_database()
    await q.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))


@bot.on_callback_query(filters.regex(r"^raid_pin"))
async def update_raid_pin(_: Client, q: CallbackQuery):
    _id = int(q.data.split("_")[2])
    raid_pin = raid_db.find_by_id(_id)
    if raid_pin:
        buttons = [
            [InlineKeyboardButton("✅Пин готов!", f"done|temporary_raid_pin_{raid_pin.id}_5_{raid_pin.get_data()}")],
            [InlineKeyboardButton("🔙Назад", f"temporary_raid_pin_{raid_pin.id}_3_{raid_pin.get_data()}")],
            [InlineKeyboardButton("🗑Удалить пин", f"cancel_raid_pin_{raid_pin.id}")], ]
        await q.edit_message_text(f"{raid_pin.band_name}\n{str(raid_pin)}",
                                  reply_markup=InlineKeyboardMarkup(buttons))
    else:
        text, keyboard = await get_text_and_buttons_from_database()
        await q.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))


class TemporaryRaidQuery:
    def __init__(self, string: str):
        """temporary_raid_pin_АЙДИ ПИНА_СТАДИЯ_ИМЯ БАНДЫ_КИЛОМЕТР_ТИП_КЛАСС"""
        splitted = string.split('_')
        self.id = int(splitted[3])
        self.stage = int(splitted[4])
        self.data = "_".join(splitted[5:5 + self.stage]) if self.stage else ""
        self.band = int(splitted[5]) if len(splitted) >= 6 else None
        self.km = int(splitted[6]) if len(splitted) >= 7 else None
        self.type = int(splitted[7]) if len(splitted) >= 8 else None
        self._class = int(splitted[8]) if len(splitted) >= 9 else None


@bot.on_callback_query(filters.regex(r"^add_pin") | filters.regex(r"^temporary_raid_pin_(\d+)_0"))
async def add_new_pin_or_temporary_raid_pin_stage_0(_: Client, q: CallbackQuery):
    if "temporary_raid_pin_" in q.data:
        _id = int(q.data.split("_")[2])
    else:
        _id = 0
    buttons = [[InlineKeyboardButton(GOAT_BAND_NAMES_SHORT[i], f"temporary_raid_pin_{_id}_1_{i}")] for i in
               range(len(GOAT_BAND_NAMES))]
    buttons.append([InlineKeyboardButton("🗑Удалить пин", f"cancel_raid_pin_{_id}")])
    keyboard = InlineKeyboardMarkup(buttons)
    await q.edit_message_text("Выбери банду:", reply_markup=keyboard)


@bot.on_callback_query(filters.regex(r"^temporary_raid_pin_(\d+)_1_(.*)"))
async def temporary_raid_pin_stage_1(client: Client, q: CallbackQuery):
    raid_data = TemporaryRaidQuery(q.data)
    buttons = [[InlineKeyboardButton(RAID_KMS[i], f"temporary_raid_pin_{raid_data.id}_2_{raid_data.data}_{i}")] for i in
               range(len(RAID_KMS))]
    buttons.append([InlineKeyboardButton("🔙Назад", f"temporary_raid_pin_{raid_data.id}_0")])
    buttons.append([InlineKeyboardButton("🗑Удалить пин", f"cancel_raid_pin_{raid_data.id}")])
    keyboard = InlineKeyboardMarkup(buttons)
    await q.edit_message_text("Выбери километр рейда:", reply_markup=keyboard)


@bot.on_callback_query(filters.regex(r"^temporary_raid_pin_(\d+)_2_(.*)"))
async def temporary_raid_pin_stage_2(_: Client, q: CallbackQuery):
    raid_data = TemporaryRaidQuery(q.data)
    buttons = [[InlineKeyboardButton(f"{raid_types[i]}", f"temporary_raid_pin_{raid_data.id}_3_{raid_data.data}_{i}")] for
               i in range(len(raid_types))]
    buttons.append([InlineKeyboardButton("🔙Назад", f"temporary_raid_pin_{raid_data.id}_1_{raid_data.data}")])
    buttons.append([InlineKeyboardButton("🗑Удалить пин", f"cancel_raid_pin_{raid_data.id}")])
    await q.edit_message_text("Выбери тип рейда:", reply_markup=InlineKeyboardMarkup(buttons))


@bot.on_callback_query(filters.regex(r"^temporary_raid_pin_(\d+)_3_(.*)"))
async def temporary_raid_pin_stage_3(_: Client, q: CallbackQuery):
    raid_data = TemporaryRaidQuery(q.data)
    buttons = [[InlineKeyboardButton(f"{raid_classes[i]}", f"temporary_raid_pin_{raid_data.id}_4_{raid_data.data}_{i}")] for
               i in range(len(raid_classes))]
    buttons.append([InlineKeyboardButton("🔙Назад", f"temporary_raid_pin_{raid_data.id}_2_{raid_data.data}")])
    buttons.append([InlineKeyboardButton("🗑Удалить пин", f"cancel_raid_pin_{raid_data.id}")])
    await q.edit_message_text("Выбери класс рейда:", reply_markup=InlineKeyboardMarkup(buttons))


@bot.on_callback_query(filters.regex(r"^temporary_raid_pin_(\d+)_4_(.*)"))
async def temporary_raid_pin_stage_4(_: Client, q: CallbackQuery):
    raid_data = TemporaryRaidQuery(q.data)
    fresh_raid = Raid(raid_data.id, band_name=GOAT_BAND_NAMES[raid_data.band], km=LONG_RAID_KMS[raid_data.km],
                      _type=raid_types[raid_data.type], _class=raid_classes[raid_data._class])
    buttons = [[InlineKeyboardButton("✅Пин готов!", f"done|temporary_raid_pin_{raid_data.id}_5_{raid_data.data}")],
               [InlineKeyboardButton("🔙Назад", f"temporary_raid_pin_{raid_data.id}_3_{raid_data.data}")],
               [InlineKeyboardButton("🗑Удалить пин", f"cancel_raid_pin_{raid_data.id}")], ]
    await q.edit_message_text(f"{fresh_raid.band_name}\n{str(fresh_raid)}", reply_markup=InlineKeyboardMarkup(buttons))


@bot.on_callback_query(filters.regex(r"^done|temporary_raid_pin_(\d+)_5_(.*)"))
async def done(_: Client, q: CallbackQuery):
    raid_data = TemporaryRaidQuery(q.data)
    fresh_raid = Raid(raid_data.id if raid_data.id else None, band_name=GOAT_BAND_NAMES[raid_data.band],
                      km=LONG_RAID_KMS[raid_data.km],
                      _type=raid_types[raid_data.type], _class=raid_classes[raid_data._class])
    raid_db.save(fresh_raid)
    text, keyboard = await get_text_and_buttons_from_database()
    await q.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))


@bot.on_callback_query(filters.regex(r"^cancel_raid_pin_(\d+)"))
async def cancel_raid_pin(_: Client, q: CallbackQuery):
    _id=int(q.data.split('_')[3])
    if _id:
        raid_db.delete_by_id(_id)
    text, keyboard = await get_text_and_buttons_from_database()
    await q.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))
