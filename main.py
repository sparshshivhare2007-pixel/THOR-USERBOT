from pyrogram import Client
from config import API_ID, API_HASH, BOT_TOKEN
import commands

app = Client("zudo_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Register all command modules
commands.start.register(app)
commands.host.register(app)
commands.manage.register(app)
commands.admin.register(app)


if __name__ == "__main__":
    print("🤖 ZUDO Hoster Bot starting...")
    app.run()
