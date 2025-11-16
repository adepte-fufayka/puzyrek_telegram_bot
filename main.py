from pyrogram import idle

import FUNCTIONS
import HANDLERS
from bot import bot

async def main():
        await bot.start()
        await idle()
if __name__ == "__main__":
    print("Пузырек запущен!")
    bot.run(main())