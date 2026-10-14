import os
from dotenv import load_dotenv

load_dotenv()

# ---------- Telegram ----------
API_ID    = int(os.getenv("API_ID"))
API_HASH  = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
OWNER_ID  = int(os.getenv("OWNER_ID"))

# ---------- MongoDB ----------
MONGO_URL = os.getenv("MONGO_URL")
DB_NAME   = "zudo_hoster"

# ---------- Force Join (optional) ----------
MUST_JOIN = []   # example: ["@YourChannel"]

# ---------- Branding ----------
BOT_NAME = "𝐙𝐔𝐃𝐎 𝐔𝐒𝐄𝐑𝐁𝐎𝐓 𝐇𝐎𝐒𝐓𝐄𝐑 🤖"
