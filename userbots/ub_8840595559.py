import time, asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.enums import ChatMemberStatus

SESSION   = "BQHqcIMAYPqzhepv5nhczSXmhufJRhLNtgdUJVcRkAMXjn4qkWzH4qeuoiD9EpdiTPcBXZVaax2sdLAqojIiIiHwPHWCB3A-aurb9lQ2oyxL8NOT0GAOLINNbOW2UlWNmzqLO4Pffg9ec5317SaNWIjtN2skTM2aEDUA2_JI5dzj8_dG2hCsa7aZRBBDOLr7B3ZPebys4B7h7a_GY3EUSMAWBTBxDz2PLTiiMI85cdvWrJ5VxyRP-a6S2_usL-wUFNzhuo8cWVBtS2k5O0ACbYj9ot2p3NjNo_opgIPGb-e7Vmo3Gcu_YnQ8quE-hkxbkUF9BAINBoQzEUkpGNgt1CfSZSSNiwAAAAIO8MhnAA"
API_ID    = 32141443
API_HASH  = "4f34a89257ac316505f5a47b237454cc"
OWNER     = "🦋"

app   = Client("ub", api_id=API_ID, api_hash=API_HASH, session_string=SESSION)
START = time.time()


# ---------------- .ping ----------------
@app.on_message(filters.command("ping", prefixes=".") & filters.me)
async def ping(c, m: Message):
    up = time.time() - START
    d, r = divmod(int(up), 86400); h, r = divmod(r, 3600); mi, s = divmod(r, 60)
    speed = round((time.time() - m.date.timestamp()) * 1000, 2)
    txt = (
        "╭━━━〔 ❖ 𝐓𝐇𝐎𝐑 ™ ╮ 〕━━━╮\n"
        f"┣ • 𝐒ᴘᴇᴇᴅ   : {speed} ms\n"
        "┣ • 𝐒ᴛᴀᴛᴜs  : ⚡ 𝐅ᴀsᴛ\n"
        f"┣ • 𝐔ᴘᴛɪᴍᴇ  : {d}d {h}h {mi}m {s}s\n"
        f"┣ • 𝐎ᴡɴᴇʀ   : @{OWNER}\n"
        "╰━━━━━━━━━━━━━━━━━━╯"
    )
    await m.edit(txt)


# ---------------- .alive ----------------
@app.on_message(filters.command("alive", prefixes=".") & filters.me)
async def alive(c, m: Message):
    txt = (
        "╭━━━〔 ❖ 𝐓𝐇𝐎𝐑 𝐀ʟɪᴠᴇ ╮ 〕━━━╮\n"
        f"┣ • 𝐎ᴡɴᴇʀ : @{OWNER}\n"
        "┣ • 𝐒ᴛᴀᴛᴜs : ✅ 𝐎ɴʟɪɴᴇ\n"
        "┣ • 𝐕ᴇʀsɪᴏɴ : v1.0\n"
        "╰━━━━━━━━━━━━━━━━━━╯"
    )
    await m.edit(txt)


# ---------------- .tagall ----------------
@app.on_message(filters.command("tagall", prefixes=".") & filters.me)
async def tagall(c, m: Message):
    if len(m.command) < 2 and not m.reply_to_message:
        return await m.edit("⚠️ Usage: `.tagall <message>`")
    msg = m.text.split(None, 1)[1] if len(m.command) > 1 else \
          (m.reply_to_message.text if m.reply_to_message else "Hey!")
    mentions, count = [], 0
    try:
        async for member in c.get_chat_members(m.chat.id):
            if member.user.is_bot or member.user.is_deleted:
                continue
            if member.status in (ChatMemberStatus.LEFT, ChatMemberStatus.BANNED):
                continue
            mentions.append(f"[{member.user.first_name}](tg://user?id={member.user.id})")
            count += 1
            if len(mentions) == 5:
                await c.send_message(m.chat.id, msg + "\n\n" + " ".join(mentions))
                mentions = []
                time.sleep(0.8)
        if mentions:
            await c.send_message(m.chat.id, msg + "\n\n" + " ".join(mentions))
        await m.edit(f"✅ Tagged {count} members.")
    except Exception as e:
        await m.edit(f"❌ Error: `{e}`")


# ---------------- .tagadmin ----------------
@app.on_message(filters.command("tagadmin", prefixes=".") & filters.me)
async def tagadmin(c, m: Message):
    msg = m.text.split(None, 1)[1] if len(m.command) > 1 else "Attention admins!"
    mentions = []
    try:
        async for member in c.get_chat_members(m.chat.id, filter="administrators"):
            if member.user.is_bot:
                continue
            mentions.append(f"[{member.user.first_name}](tg://user?id={member.user.id})")
        if mentions:
            await c.send_message(m.chat.id, msg + "\n\n" + " ".join(mentions))
            await m.edit(f"✅ Tagged {len(mentions)} admins.")
        else:
            await m.edit("❌ No admins found.")
    except Exception as e:
        await m.edit(f"❌ Error: `{e}`")


# ---------------- .info ----------------
@app.on_message(filters.command("info", prefixes=".") & filters.me)
async def info(c, m: Message):
    u = m.reply_to_message.from_user if m.reply_to_message else m.from_user
    try:
        full = await c.get_chat(u.id)
        bio = full.bio if hasattr(full, "bio") else "N/A"
    except Exception:
        bio = "N/A"
    txt = (
        "╭━━━〔 ❖ 𝐓𝐇𝐎𝐑 𝐈ɴғᴏ ╮ 〕━━━╮\n"
        f"┣ • 𝐍ᴀᴍᴇ     : {u.first_name}\n"
        f"┣ • 𝐔sᴇʀɴᴀᴍᴇ : @{u.username if u.username else 'None'}\n"
        f"┣ • 𝐈ᴅ       : `{u.id}`\n"
        f"┣ • 𝐁ᴏᴛ      : {u.is_bot}\n"
        f"┣ • 𝐁ɪᴏ      : {bio}\n"
        "╰━━━━━━━━━━━━━━━━━━╯"
    )
    await m.edit(txt)


# ---------------- .id ----------------
@app.on_message(filters.command("id", prefixes=".") & filters.me)
async def get_id(c, m: Message):
    txt = f"💬 **Chat ID:** `{m.chat.id}`\n"
    if m.reply_to_message:
        txt += f"👤 **User ID:** `{m.reply_to_message.from_user.id}`"
    await m.edit(txt)


# ---------------- .spam ----------------
@app.on_message(filters.command("spam", prefixes=".") & filters.me)
async def spam(c, m: Message):
    if len(m.command) < 3:
        return await m.edit("⚠️ Usage: `.spam <count> <text>`")
    try:
        count = int(m.command[1])
        if count > 20:
            return await m.edit("⚠️ Max 20 messages allowed.")
    except ValueError:
        return await m.edit("⚠️ Count ek number hona chahiye.")
    text = m.text.split(None, 2)[2]
    await m.delete()
    for _ in range(count):
        await c.send_message(m.chat.id, text)
        time.sleep(0.5)


# ---------------- .purge ----------------
@app.on_message(filters.command("purge", prefixes=".") & filters.me)
async def purge(c, m: Message):
    if not m.reply_to_message:
        return await m.edit("⚠️ Reply kisi message pe then `.purge`")
    ids = list(range(m.reply_to_message.id, m.id + 1))
    try:
        await c.delete_messages(m.chat.id, ids)
    except Exception as e:
        await m.edit(f"❌ Error: `{e}`")


# ---------------- .kick ----------------
@app.on_message(filters.command("kick", prefixes=".") & filters.me)
async def kick(c, m: Message):
    if not m.reply_to_message:
        return await m.edit("⚠️ Reply karo jise kick karna hai")
    u = m.reply_to_message.from_user
    try:
        await c.ban_chat_member(m.chat.id, u.id)
        await c.unban_chat_member(m.chat.id, u.id)
        await m.edit(f"👢 Kicked {u.first_name}")
    except Exception as e:
        await m.edit(f"❌ Error: `{e}`")


# ---------------- .ban ----------------
@app.on_message(filters.command("ban", prefixes=".") & filters.me)
async def ban(c, m: Message):
    if not m.reply_to_message:
        return await m.edit("⚠️ Reply karo jise ban karna hai")
    u = m.reply_to_message.from_user
    try:
        await c.ban_chat_member(m.chat.id, u.id)
        await m.edit(f"🚫 Banned {u.first_name}")
    except Exception as e:
        await m.edit(f"❌ Error: `{e}`")


# ---------------- .unban ----------------
@app.on_message(filters.command("unban", prefixes=".") & filters.me)
async def unban(c, m: Message):
    if not m.reply_to_message:
        return await m.edit("⚠️ Reply karo jise unban karna hai")
    u = m.reply_to_message.from_user
    try:
        await c.unban_chat_member(m.chat.id, u.id)
        await m.edit(f"✅ Unbanned {u.first_name}")
    except Exception as e:
        await m.edit(f"❌ Error: `{e}`")


# ---------------- .promote ----------------
@app.on_message(filters.command("promote", prefixes=".") & filters.me)
async def promote(c, m: Message):
    if not m.reply_to_message:
        return await m.edit("⚠️ Reply karo jise promote karna hai")
    u = m.reply_to_message.from_user
    try:
        await c.promote_chat_member(
            m.chat.id, u.id,
            can_change_info=True,
            can_delete_messages=True,
            can_invite_users=True,
            can_restrict_members=True,
            can_pin_messages=True,
        )
        await m.edit(f"⭐ Promoted {u.first_name}")
    except Exception as e:
        await m.edit(f"❌ Error: `{e}`")


# ---------------- .demote ----------------
@app.on_message(filters.command("demote", prefixes=".") & filters.me)
async def demote(c, m: Message):
    if not m.reply_to_message:
        return await m.edit("⚠️ Reply karo jise demote karna hai")
    u = m.reply_to_message.from_user
    try:
        await c.promote_chat_member(
            m.chat.id, u.id,
            can_change_info=False,
            can_delete_messages=False,
            can_invite_users=False,
            can_restrict_members=False,
            can_pin_messages=False,
        )
        await m.edit(f"⬇️ Demoted {u.first_name}")
    except Exception as e:
        await m.edit(f"❌ Error: `{e}`")


# ---------------- .mute ----------------
@app.on_message(filters.command("mute", prefixes=".") & filters.me)
async def mute(c, m: Message):
    if not m.reply_to_message:
        return await m.edit("⚠️ Reply karo jise mute karna hai")
    u = m.reply_to_message.from_user
    try:
        from pyrogram.types import ChatPermissions
        await c.restrict_chat_member(m.chat.id, u.id, ChatPermissions())
        await m.edit(f"🔇 Muted {u.first_name}")
    except Exception as e:
        await m.edit(f"❌ Error: `{e}`")


# ---------------- .unmute ----------------
@app.on_message(filters.command("unmute", prefixes=".") & filters.me)
async def unmute(c, m: Message):
    if not m.reply_to_message:
        return await m.edit("⚠️ Reply karo jise unmute karna hai")
    u = m.reply_to_message.from_user
    try:
        from pyrogram.types import ChatPermissions
        perms = ChatPermissions(
            can_send_messages=True,
            can_send_media_messages=True,
            can_send_other_messages=True,
            can_add_web_page_previews=True,
        )
        await c.restrict_chat_member(m.chat.id, u.id, perms)
        await m.edit(f"🔊 Unmuted {u.first_name}")
    except Exception as e:
        await m.edit(f"❌ Error: `{e}`")


# ---------------- .pin ----------------
@app.on_message(filters.command("pin", prefixes=".") & filters.me)
async def pin(c, m: Message):
    if not m.reply_to_message:
        return await m.edit("⚠️ Reply karo jise pin karna hai")
    try:
        await c.pin_chat_message(m.chat.id, m.reply_to_message.id)
        await m.edit("📌 Pinned!")
    except Exception as e:
        await m.edit(f"❌ Error: `{e}`")


# ---------------- .del ----------------
@app.on_message(filters.command("del", prefixes=".") & filters.me)
async def delete(c, m: Message):
    if not m.reply_to_message:
        return await m.edit("⚠️ Reply karo jise delete karna hai")
    try:
        await m.reply_to_message.delete()
        await m.delete()
    except Exception as e:
        await m.edit(f"❌ Error: `{e}`")


# ---------------- .gcast ----------------
@app.on_message(filters.command("gcast", prefixes=".") & filters.me)
async def gcast(c, m: Message):
    if len(m.command) < 2:
        return await m.edit("⚠️ Usage: `.gcast <message>`")
    msg = m.text.split(None, 1)[1]
    sent, failed = 0, 0
    await m.edit("📢 Broadcasting...")
    async for d in c.get_dialogs():
        try:
            await c.send_message(d.chat.id, msg)
            sent += 1
            time.sleep(0.5)
        except Exception:
            failed += 1
    await m.edit(f"✅ Sent: {sent}\n❌ Failed: {failed}")


# ---------------- .help ----------------
@app.on_message(filters.command("help", prefixes=".") & filters.me)
async def help_userbot(c, m: Message):
    txt = (
        "╭━━━〔 ❖ 𝐓𝐇𝐎𝐑 𝐂ᴍᴅs ╮ 〕━━━╮\n"
        "┣ • .ping — Speed check\n"
        "┣ • .alive — Bot status\n"
        "┣ • .info — User info\n"
        "┣ • .id — Chat/User ID\n"
        "┣ • .tagall <msg>\n"
        "┣ • .tagadmin <msg>\n"
        "┣ • .spam <n> <msg>\n"
        "┣ • .purge (reply)\n"
        "┣ • .kick / .ban / .unban\n"
        "┣ • .mute / .unmute\n"
        "┣ • .promote / .demote\n"
        "┣ • .pin / .del\n"
        "┣ • .gcast <msg>\n"
        "╰━━━━━━━━━━━━━━━━━━╯"
    )
    await m.edit(txt)


print(f"✅ Userbot running for @{OWNER}")
app.run()
