import os, sys, subprocess, asyncio
from pyrogram import Client, filters
from pyrogram.errors import SessionPasswordNeeded, PhoneCodeInvalid, PhoneCodeExpired
from pyrogram.types import Message
from config import API_ID, API_HASH
import fonts
import database as db

LOGIN = {}   # temp login state (in-memory)
RUNNING = {} # { uid: Popen }

os.makedirs("userbots", exist_ok=True)


USERBOT_TEMPLATE = '''\
import time
from pyrogram import Client, filters

SESSION   = "{session}"
API_ID    = {api_id}
API_HASH  = "{api_hash}"
OWNER     = "{owner}"

app   = Client("ub", api_id=API_ID, api_hash=API_HASH, session_string=SESSION)
START = time.time()

@app.on_message(filters.command("ping", prefixes=".") & filters.me)
async def ping(c, m):
    up = time.time() - START
    d, r = divmod(int(up), 86400); h, r = divmod(r, 3600); mi, s = divmod(r, 60)
    speed = round((time.time() - m.date.timestamp()) * 1000, 2)
    txt = (
        "╭━━━〔 ❖ 𝐙𝐔𝐃𝐎 ™ ╮ 〕━━━╮\\n"
        f"┣ • 𝐒ᴘᴇᴇᴅ   : {{speed}} ms\\n"
        "┣ • 𝐒ᴛᴀᴛᴜs  : ⚡ 𝐅ᴀsᴛ\\n"
        f"┣ • 𝐔ᴘᴛɪᴍᴇ  : {{d}}d {{h}}h {{mi}}m {{s}}s\\n"
        f"┣ • 𝐎ᴡɴᴇʀ   : @{{OWNER}}\\n"
        "╰━━━━━━━━━━━━━━━━━━╯"
    )
    await m.edit(txt)

print(f"✅ Userbot running for @{{OWNER}}")
app.run()
'''


def register(app):

    # ---------- /host ----------
    @app.on_message(filters.command("host") & filters.private)
    async def host_cmd(c, m: Message):
        uid = m.from_user.id

        if await db.get_hosted(uid):
            return await m.reply("⚠️ You already have a userbot. Use /logout first.")

        await db.set_stage(uid, "phone")
        await m.reply(fonts.ask_phone())

    # ---------- Login step router ----------
    @app.on_message(filters.private & filters.text, group=1)
    async def flow(c, m: Message):
        uid = m.from_user.id
        stage = await db.get_stage(uid)

        # ---- PHONE ----
        if stage == "phone":
            phone = m.text.replace(" ", "")
            cli = Client(name=f"temp_{uid}", api_id=API_ID, api_hash=API_HASH, in_memory=True)
            await cli.connect()
            try:
                sent = await cli.send_code(phone)
            except Exception as e:
                await db.clear_stage(uid)
                return await m.reply(f"❌ Failed: `{e}`\nTry /host again.")

            LOGIN[uid] = {
                "client": cli,
                "phone": phone,
                "hash": sent.phone_code_hash,
                "tries": 3,
            }
            await db.set_stage(uid, "otp")
            return await m.reply(fonts.ask_otp())

        # ---- OTP ----
        if stage == "otp":
            st = LOGIN.get(uid)
            if not st:
                await db.clear_stage(uid)
                return await m.reply("⚠️ Session expired. Use /host again.")

            otp = m.text.replace(" ", "")
            try:
                await st["client"].sign_in(st["phone"], st["hash"], otp)
            except SessionPasswordNeeded:
                await db.set_stage(uid, "2fa")
                return await m.reply(fonts.ask_2fa())
            except (PhoneCodeInvalid, PhoneCodeExpired) as e:
                return await m.reply(f"❌ Invalid OTP: `{e}`\nTry again.")
            except Exception as e:
                return await m.reply(f"❌ Error: `{e}`")

            session = await st["client"].export_session_string()
            await st["client"].disconnect()
            LOGIN.pop(uid, None)
            await db.clear_stage(uid)
            await deploy_userbot(m, uid, session)

        # ---- 2FA ----
        elif stage == "2fa":
            st = LOGIN.get(uid)
            if not st:
                await db.clear_stage(uid)
                return await m.reply("⚠️ Session expired. Use /host again.")

            try:
                await st["client"].check_password(m.text)
                session = await st["client"].export_session_string()
                await st["client"].disconnect()
                LOGIN.pop(uid, None)
                await db.clear_stage(uid)
                await deploy_userbot(m, uid, session)
            except Exception:
                st["tries"] -= 1
                if st["tries"] <= 0:
                    LOGIN.pop(uid, None)
                    await db.clear_stage(uid)
                    return await m.reply("❌ Too many wrong attempts. Use /host again.")
                return await m.reply(fonts.wrong_2fa(st["tries"]))


# ---------- Deploy helper ----------
async def deploy_userbot(m: Message, uid: int, session: str):
    await m.reply(fonts.hosting())

    owner = m.from_user.username or m.from_user.first_name.replace(" ", "_")
    path  = f"userbots/ub_{uid}.py"

    with open(path, "w", encoding="utf-8") as f:
        f.write(USERBOT_TEMPLATE.format(
            session=session,
            api_id=API_ID,
            api_hash=API_HASH,
            owner=owner,
        ))

    log  = open(f"userbots/ub_{uid}.log", "a", encoding="utf-8")
    proc = subprocess.Popen([sys.executable, path], stdout=log, stderr=log)
    RUNNING[uid] = proc

    await db.save_hosted(uid, session, owner, proc.pid)
    await db.save_user(m.from_user)

    await asyncio.sleep(3)

    if proc.poll() is not None:
        await db.delete_hosted(uid)
        await m.reply("❌ Userbot crashed on start. Check logs / try again.")
    else:
        await m.reply(fonts.success())
