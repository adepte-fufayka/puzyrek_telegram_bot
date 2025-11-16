from imghdr import test_xbm

from pyrogram import Client, filters
from pyrogram.types import Message

import FUNCTIONS
import bot

import datetime

from pyrogram import Client
from pyrogram.types import Message
from DATABASE import UserProfileDB, UserSettingsDB

db = UserProfileDB()
user_db = UserSettingsDB()

from CLASSES import UserProfile, UserSettings
from CONSTANTS import FULL_PROFILE, MOSCOW
from CONSTANTS import PROFILE_DELTA


def text_to_class(text:str, time:datetime.datetime)-> UserProfile:
    d=datetime.datetime(time.year, time.month, time.day, time.hour, time.minute, time.second, tzinfo=MOSCOW)
    data=FULL_PROFILE.match(text)
    zen_value = 0
    if data['zen']:
        zen_value = int(data['zen'])-1

    return UserProfile(            user_id=int(data['user_id']),
            nickname=data['nickname'].strip(),
            fraction_emoji=data['fraction_emoji'],
            fraction_name=data['fraction_name'].strip(),
            gang_name=data['gang_name'].strip(),
            max_hp=int(data['max_hp']),
            damage=int(data['damage']),
            armor=int(data['armor']),
            strength=int(data['strength']),
            accuracy=int(data['accuracy']),
            charisma=int(data['charisma']),
            dexterity=int(data['dexterity']),
            max_energy=int(data['max_energy']),
            zen=int(zen_value) if zen_value else 0,
                                   updated_at=d)


def diff_user_profiles(old: UserProfile, new: UserProfile) -> str:
    diff_list = []

    # Обработка строковых полей
    if old.nickname != new.nickname:
        diff_list.append(f"Сменил имя на '{new.nickname}'")

    if old.fraction_emoji != new.fraction_emoji:
        diff_list.append(f"Сменил фракцию на '{new.fraction_emoji}'")

    if old.gang_name != new.gang_name:
        diff_list.append(f"Сменил банду на '{new.gang_name}'")

    # Обработка целочисленных полей

    if old.max_hp != new.max_hp:
        diff = new.max_hp - old.max_hp
        sign = "+" if diff > 0 else ""
        diff_list.append(f"❤️ {sign}{diff}")

    if old.damage != new.damage:
        diff = new.damage - old.damage
        sign = "+" if diff > 0 else ""
        diff_list.append(f"⚔️ {sign}{diff}")

    if old.armor != new.armor:
        diff = new.armor - old.armor
        sign = "+" if diff > 0 else ""
        diff_list.append(f"🛡 {sign}{diff}")

    if old.strength != new.strength:
        diff = new.strength - old.strength
        sign = "+" if diff > 0 else ""
        diff_list.append(f"💪 {sign}{diff}")

    if old.accuracy != new.accuracy:
        diff = new.accuracy - old.accuracy
        sign = "+" if diff > 0 else ""
        diff_list.append(f"🎯 {sign}{diff}")

    if old.charisma != new.charisma:
        diff = new.charisma - old.charisma
        sign = "+" if diff > 0 else ""
        diff_list.append(f"🗣 {sign}{diff}")

    if old.dexterity != new.dexterity:
        diff = new.dexterity - old.dexterity
        sign = "+" if diff > 0 else ""
        diff_list.append(f"🤸🏽‍♂️ {sign}{diff}")

    if old.max_energy != new.max_energy:
        diff = new.max_energy - old.max_energy
        sign = "+" if diff > 0 else ""
        diff_list.append(f"🔋 {sign}{diff}")

    if old.zen != new.zen:
        diff = new.zen - old.zen
        sign = "+" if diff > 0 else ""
        diff_list.append(f"🏵 {sign}{diff}")



    return '\n'.join(diff_list)
@bot.bot.on_message(filters.regex(FULL_PROFILE) & FUNCTIONS.filters.from_ww_filter.ww_filter())
async def get_full_profile(client: Client, message: Message):

    user_profile=text_to_class(message.text, message.forward_date)
    if user_profile.user_id != message.from_user.id:
        await client.send_message(chat_id=message.chat.id, text="Не твой 📟Пип-бой, записывать не буду!", reply_to_message_id=message.id)
        return
    if int(datetime.datetime.now().timestamp())-int(message.forward_date.timestamp())<PROFILE_DELTA:
        pred_profile=db.find_profile_id(user_profile.user_id)
        if pred_profile:
            updates=diff_user_profiles(pred_profile, user_profile)
            db.save_profile(user_profile)
            await client.send_message(chat_id=message.chat.id, text=f"📟Пип-бой обновлен!\n{updates}", reply_to_message_id=message.id)
            return
        db.save_profile(user_profile)
        user_db.save(UserSettings(user_profile.user_id, 3, 0, True))
        await client.send_message(chat_id=message.chat.id, text=f"Сохранил твой 📟Пип-бой, не забывай обновлять его как можно чаще!", reply_to_message_id=message.id)
        return
    await client.send_message(chat_id=message.chat.id, text="Слишком медленно присылаешь", reply_to_message_id=message.id)
    return