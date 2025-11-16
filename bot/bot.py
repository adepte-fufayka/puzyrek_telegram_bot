from pyrogram import Client
import CONFIG

bot = Client(
    name="session",
    api_id=CONFIG.API_ID,
    api_hash=CONFIG.API_HASH,
    bot_token=CONFIG.TOKEN
)
