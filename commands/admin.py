from pyrogram import filters
from pyrogram.types import Message
from config import OWNER_ID
import fonts
import database as db


def register(app):

    @app.on_message(filters.command("stats") & filters.private)
    async def stats(c, m: Message):
        if m.from_user.id != OWNER_ID:
            return await m.reply("🚫 Owner only!")

        total_users   = await db.users.count_documents({})
        total_hosted  = await db.hosted.count_documents({})

        await m.reply(
            f"📊 {fonts.bold('Bot Statistics')}\n\n"
            f"👥 Users: `{total_users}`\n"
            f"🚀 Hosted: `{total_hosted}`"
        )
