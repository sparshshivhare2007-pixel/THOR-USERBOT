import os, sys, re, subprocess, asyncio
from pyrogram import Client, filters
from pyrogram.errors import SessionPasswordNeeded, PhoneCodeInvalid, PhoneCodeExpired
from pyrogram.types import Message
from config import API_ID, API_HASH
import fonts
import database as db

LOGIN   = {}
RUNNING = {}

os.makedirs("userbots", exist_ok=True)


# ============================================================
# USERBOT TEMPLATE  (runs on user's account)
# ============================================================
USERBOT_TEMPLATE = '''\
import time
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.enums import ChatMemberStatus

SESSION   = "{session}"
API_ID    = {api_id}
API_HASH  = "{api_hash}"
OWNER     = "{owner}"

app   = Client("ub", api_id=API_ID, api_hash=API_HASH, session_string=SESSION)
START = time.time()


# ---------------- .ping ----------------
@app.on_message(filters.command("ping", prefixes=".") & filters.me)
async def ping(c, m: Message):
    up = time.time() - START
    d, r = divmod(int(up), 86400); h, r = divmod(r, 3600); mi, s = divmod(r, 60)
    speed = round((time.time() - m.date.timestamp()) * 1000, 2)
    txt = (
        "╭━━━〔 ❖ 𝐓𝐇𝐎𝐑 ™ ╮ 〕━━━╮\\n"
        f"┣ • 𝐒ᴘᴇᴇᴅ   : {{speed}} ms\\n"
        "┣ • 𝐒ᴛᴀᴛᴜs  : ⚡ 𝐅ᴀsᴛ\\n"
        f"┣ • 𝐔ᴘᴛɪᴍᴇ  : {{d}}d {{h}}h {{mi}}m {{s}}s\\n"
        f"┣ • 𝐎ᴡɴᴇʀ   : @{{OWNER}}\\n"
        "╰━━━━━━━━━━━━━━━━━━╯"
    )
    await m.edit(txt)


# ---------------- .tagall ----------------
@app.on_message(filters.command("tagall", prefixes=".") & filters.me)
async def tagall(c, m: Message):
    if len(m.command) < 2 and not m.reply_to_message:
        return await m.edit("⚠️ Usage: `.tagall <message>`")
    msg = m.text.split(None, 1)[1] if len(m.command) > 1 else \\
          (m.reply_to_message.text if m.reply_to_message else "Hey!")
    mentions, count = [], 0
    try:
        async for member in c.get_chat_members(m.chat.id):
            if member.user.is_bot or member.user.is_deleted:
                continue
            if member.status in (ChatMemberStatus.LEFT, ChatMemberStatus.BANNED):
                continue
            mentions.append(f"[{{member.user.first_name}}](tg://user?id={{member.user.id}})")
            count += 1
            if len(mentions) == 5:
                await c.send_message(m.chat.id, msg + "\\n\\n" + " ".join(mentions))
                mentions = []
                time.sleep(0.8)
        if mentions:
            await c.send_message(m.chat.id, msg + "\\n\\n" + " ".join(mentions))
        await m.edit(f"✅ Tagged {{count}} members.")
    except Exception as e:
        await m.edit(f"❌ Error: `{{e}}`")


# ---------------- .tagadmin ----------------
@app.on_message(filters.command("tagadmin", prefixes=".") & filters.me)
async def tagadmin(c, m: Message):
    msg = m.text.split(None, 1)[1] if len(m.command) > 1 else "Attention admins!"
    mentions = []
    try:
        async for member in c.get_chat_members(m.chat.id, filter="administrators"):
            if member.user.is_bot:
                continue
            mentions.append(f"[{{member.user.first_name}}](tg://user?id={{member.user.id}})")
        if mentions:
            await c.send_message(m.chat.id, msg + "\\n\\n" + " ".join(mentions))
            await m.edit(f"✅ Tagged {{len(mentions)}} admins.")
        else:
            await m.edit("❌ No admins found.")
    except Exception as e:
        await m.edit(f"❌ Error: `{{e}}`")


print(f"✅ Userbot running for @{{OWNER}}")
app.run()
'''


# ============================================================
# HELPERS
# ============================================================
def clean_phone(p: str) -> str:
    return re.sub(r"[^\d+]", "", p)


def is_valid_phone(p: str) -> bool:
    return bool(re.match(r"^\+\d{10,15}$", p))


# ============================================================
# REGISTER HANDLERS
# ============================================================
def register(app):

    # ---------- /host ----------
    @app.on_message(filters.command("host") & filters.private)
    async def host_cmd(c, m: Message):
        uid = m.from_user.id
        if await db.get_hosted(uid):
            return await m.reply("⚠️ You already have a userbot. Use /logout first.")
        await db.set_stage(uid, "phone")
        await m.reply(fonts.ask_phone())

    # ---------- Login flow router ----------
    @app.on_message(filters.private & filters.text, group=1)
    async def flow(c, m: Message):
        uid = m.from_user.id
        stage = await db.get_stage(uid)

        # ================= PHONE =================
        if stage == "phone":
            phone = clean_phone(m.text.strip())

            if not phone.startswith("+") or not is_valid_phone(phone):
                return await m.reply(
                    "❌ **Invalid phone number!**\n\n"
                    "Sahi format: `+919876543210`\n"
                    "Country code zaroori hai (e.g. +91, +1, +62)\n\n"
                    "Phir se bhejo:"
                )

            cli = Client(
                name=f"temp_{uid}",
                api_id=API_ID, api_hash=API_HASH,
                in_memory=True
            )
            await cli.connect()

            try:
                sent = await cli.send_code(phone)
            except Exception as e:
                await cli.disconnect()
                await db.clear_stage(uid)

                err = str(e).upper()

                if "PHONE_NUMBER_INVALID" in err:
                    return await m.reply(
                        "❌ **Telegram says phone invalid!**\n\n"
                        "Check karo:\n"
                        "• Country code sahi? (`+91` India, `+62` Indonesia)\n"
                        "• Extra zero ya space nahi?\n"
                        "• Number active hai?\n\n"
                        "Sahi format: `+919876543210`\n\n"
                        "Try /host again."
                    )
                elif "PHONE_NUMBER_BANNED" in err:
                    return await m.reply("🚫 Ye number Telegram pe banned hai.\nTry another number.")
                elif "FLOOD_WAIT" in err:
                    secs = re.search(r"FLOOD_WAIT_(\d+)", err)
                    w = secs.group(1) if secs else "kuch"
                    return await m.reply(f"⏳ Flood wait! {w} sec baad try karo.")
                else:
                    return await m.reply(f"❌ Failed: `{e}`\nTry /host again.")

            LOGIN[uid] = {
                "client": cli,
                "phone": phone,
                "hash": sent.phone_code_hash,
                "tries": 3,
            }
            await db.set_stage(uid, "otp")
            return await m.reply(fonts.ask_otp())

        # ================= OTP =================
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
            except PhoneCodeInvalid:
                return await m.reply("❌ **OTP galat!** Phir se bhejo:")
            except PhoneCodeExpired:
                LOGIN.pop(uid, None)
                await db.clear_stage(uid)
                return await m.reply("❌ **OTP expire!** /host se dobara try karo.")
            except Exception as e:
                return await m.reply(f"❌ Error: `{e}`")

            # Success (no 2FA)
            session = await st["client"].export_session_string()
            await st["client"].disconnect()
            LOGIN.pop(uid, None)
            await db.clear_stage(uid)
            await deploy_userbot(m, uid, session)

        # ================= 2FA =================
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
                    return await m.reply(
                        "❌ **Too many wrong 2FA attempts.**\n"
                        "Use /host again."
                    )
                return await m.reply(fonts.wrong_2fa(st["tries"]))


# ============================================================
# DEPLOY USERBOT
# ============================================================
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
        await m.reply(
            "❌ **Userbot crashed on start.**\n\n"
            "Check `userbots/ub_" + str(uid) + ".log` for details.\n"
            "Try /logout then /host again."
        )
    else:
        await m.reply(fonts.success())