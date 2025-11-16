from pyrogram import filters
from pyrogram.types import Message

from CONSTANTS import BOT_WW_ID


def ww_filter():
    async def func(_, __, query: Message):
        return query.forward_from and query.forward_from.id == BOT_WW_ID

    return filters.create(func)