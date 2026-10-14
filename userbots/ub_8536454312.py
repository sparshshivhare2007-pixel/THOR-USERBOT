import time
from pyrogram import Client, filters

SESSION   = "BQHqcIMAj3H1qU5f2GlgEPBKoVsdzikQBsVH-Z59cAuIP1flGwa3l-d1DbcGJhwET4FGyr-ZicIOQk5KWJhNQsMaousm3-rtCAHZ0UyqOPZJvPG51PH2IDNMn_FVbsbpwsNqt4XMNRE4DGg2MOI2HsYvXg8dfuBpzjDjGoPZ_mvy_qnJM6MAFa3UFmk4V_2Qn14Igw8pSuBAhNjoaa7PiDxTpmbsUuvc6_XEKX3-KJPa3CauCUxMmuIEz3OmUx8gqjolr6UNqkg12777ZdHtDnwgkowjcK-28Z0CMRIeYlQYmoXR-HEP9f7l9OqEvYZxXUvP0eTjT3okJZ0-WbkZAZ6ELEcCjAAAAAIO8MhnAA"
API_ID    = 32141443
API_HASH  = "4f34a89257ac316505f5a47b237454cc"
OWNER     = "N"

app   = Client("ub", api_id=API_ID, api_hash=API_HASH, session_string=SESSION)
START = time.time()

@app.on_message(filters.command("ping", prefixes=".") & filters.me)
async def ping(c, m):
    up = time.time() - START
    d, r = divmod(int(up), 86400); h, r = divmod(r, 3600); mi, s = divmod(r, 60)
    speed = round((time.time() - m.date.timestamp()) * 1000, 2)
    txt = (
        "╭━━━〔 ❖ 𝐙𝐔𝐃𝐎 ™ ╮ 〕━━━╮\n"
        f"┣ • 𝐒ᴘᴇᴇᴅ   : {speed} ms\n"
        "┣ • 𝐒ᴛᴀᴛᴜs  : ⚡ 𝐅ᴀsᴛ\n"
        f"┣ • 𝐔ᴘᴛɪᴍᴇ  : {d}d {h}h {mi}m {s}s\n"
        f"┣ • 𝐎ᴡɴᴇʀ   : @{OWNER}\n"
        "╰━━━━━━━━━━━━━━━━━━╯"
    )
    await m.edit(txt)

print(f"✅ Userbot running for @{OWNER}")
app.run()
