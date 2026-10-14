from pyrogram import filters
from pyrogram.types import Message
from config import BOT_NAME
import fonts
import database as db


def register(app):

    @app.on_message(filters.command("start") & filters.private)
    async def start_cmd(c, m: Message):
        await db.save_user(m.from_user)
        await m.reply(
            f"🌟 {fonts.bold('Welcome ' + m.from_user.first_name)}! 🌟\n\n"
            f"🤖 {BOT_NAME}\n"
            "Deploy your own userbot in seconds.\n\n"
            "👉 Use /host to begin."
        )

    @app.on_message(filters.command("help") & filters.private)
    async def help_cmd(c, m: Message):
        await m.reply(
            f"🌟 {fonts.bold('Commands')} 🌟\n\n"
            "🔹 /start - Launch bot\n"
            "🔹 /host  - Deploy your userbot\n"
            "🔹 /status - Check your userbot\n"
            "🔹 /logout - Stop your userbot\n"
            "🔹 /help  - Show this menu\n\n"
            f"After hosting, send `.ping` in your userbot DM."
        )
