import time
from pyrogram import Client, filters
from pyrogram.types import Message, ChatPermissions
from pyrogram.enums import ChatMemberStatus

SESSION   = "BQHqcIMAnqdEliDWQSIzj_dNm_WBm-ERaUfX11wUaMqXeyGudw9nPaS3hwsZjaWCQXjnW5Bc_GZKcTDjYDD-w4dvy5KuNvHhWAJ4GxfBPzEYM5Q88vGLCsTBPGnTm924FyTqPN3hDHZWVuD96HVVCeD0_QPoq3GWi8CFFqetps1soq9LCvPQuZgH7kLEZ5dmnDkS4az0rL_pjqXthY6WumLUlq9QFtbrN7V5c-RnoPtHQzLnfqSLN3BbhQxi0FEJS94ny5Vwh5eDabuJQWOp7i4L6Wm6DePkUSgfM8QU52m3llxeZmUJvz7PzWsUW8COJKFPCu998J9D09RsjxSl32HgcdtLqAAAAAIO8MhnAA"
API_ID    = 32141443
API_HASH  = "4f34a89257ac316505f5a47b237454cc"
OWNER     = "🦋"

app   = Client("ub", api_id=API_ID, api_hash=API_HASH, session_string=SESSION)
START = time.time()

STOP_TAG = set()   # chat ids where tagall should stop


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
        f"┣ • 𝐎ᴡɴᴇʀ  : @{OWNER}\n"
        "┣ • 𝐒ᴛᴀᴛᴜs  : ✅ 𝐎ɴʟɪɴᴇ\n"
        "┣ • 𝐕ᴇʀsɪᴏɴ : v1.0\n"
        "╰━━━━━━━━━━━━━━━━━━╯"
    )
    await m.edit(txt)


# ---------------- .tagall + .stoptagall ----------------
@app.on_message(filters.command("stoptagall", prefixes=".") & filters.me)
async def stoptagall(c, m: Message):
    STOP_TAG.add(m.chat.id)
    await m.edit("🛑 Tagall stopped.")


@app.on_message(filters.command("tagall", prefixes=".") & filters.me)
async def tagall(c, m: Message):
    if len(m.command) < 2 and not m.reply_to_message:
        return await m.edit("⚠️ Usage: `.tagall <message>`")

    if len(m.command) > 1:
        msg = m.text.split(None, 1)[1]
    elif m.reply_to_message:
        msg = m.reply_to_message.text or m.reply_to_message.caption or "Hey!"
    else:
        msg = "Hey!"

    chat_id = m.chat.id
    STOP_TAG.discard(chat_id)

    await m.edit(f"📣 Tagging with: **{msg}**\nStop with `.stoptagall`")

    count = 0
    try:
        async for member in c.get_chat_members(chat_id):
            if chat_id in STOP_TAG:
                STOP_TAG.discard(chat_id)
                return await c.send_message(
                    chat_id,
                    f"🛑 Stopped. Tagged **{count}** members."
                )
            if member.user.is_bot or member.user.is_deleted:
                continue
            if member.status in (ChatMemberStatus.LEFT, ChatMemberStatus.BANNED):
                continue
            name = member.user.first_name or "User"
            mention = f"[{name}](tg://user?id={member.user.id})"
            try:
                await c.send_message(chat_id, f"{msg} {mention}")
                count += 1
            except Exception:
                pass
            time.sleep(0.6)

        await c.send_message(chat_id, f"✅ Done. Tagged **{count}** members.")
    except Exception as e:
        await c.send_message(chat_id, f"❌ Error: `{e}`")


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
            for i, men in enumerate(mentions):
                await c.send_message(m.chat.id, f"{msg} {men}")
                time.sleep(0.5)
            await m.edit(f"✅ Tagged {len(mentions)} admins.")
        else:
            await m.edit("❌ No admins found.")
    except Exception as e:
        await m.edit(f"❌ Error: `{e}`")


# ---------------- .info (no delete) ----------------
@app.on_message(filters.command("info", prefixes=".") & filters.me)
async def info(c, m: Message):
    u = m.reply_to_message.from_user if m.reply_to_message else m.from_user
    try:
        full = await c.get_chat(u.id)
        bio = getattr(full, "bio", None) or "N/A"
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
    # Send as reply, don't delete original
    await m.reply(txt)


# ---------------- .id ----------------
@app.on_message(filters.command("id", prefixes=".") & filters.me)
async def get_id(c, m: Message):
    txt = f"💬 **Chat ID:** `{m.chat.id}`\n"
    if m.reply_to_message:
        txt += f"👤 **User ID:** `{m.reply_to_message.from_user.id}`"
    await m.reply(txt)


# ---------------- .spam ----------------
@app.on_message(filters.command("spam", prefixes=".") & filters.me)
async def spam(c, m: Message):
    if len(m.command) < 3:
        return await m.edit("⚠️ Usage: `.spam <count> <text>`")
    try:
        count = int(m.command[1])
        if count > 20:
            return await m.edit("⚠️ Max 20 messages.")
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
        await m.reply(f"👢 Kicked {u.first_name}")
    except Exception as e:
        await m.reply(f"❌ Error: `{e}`")


# ---------------- .ban ----------------
@app.on_message(filters.command("ban", prefixes=".") & filters.me)
async def ban(c, m: Message):
    if not m.reply_to_message:
        return await m.edit("⚠️ Reply karo jise ban karna hai")
    u = m.reply_to_message.from_user
    try:
        await c.ban_chat_member(m.chat.id, u.id)
        await m.reply(f"🚫 Banned {u.first_name}")
    except Exception as e:
        await m.reply(f"❌ Error: `{e}`")


# ---------------- .unban ----------------
@app.on_message(filters.command("unban", prefixes=".") & filters.me)
async def unban(c, m: Message):
    if not m.reply_to_message:
        return await m.edit("⚠️ Reply karo jise unban karna hai")
    u = m.reply_to_message.from_user
    try:
        await c.unban_chat_member(m.chat.id, u.id)
        await m.reply(f"✅ Unbanned {u.first_name}")
    except Exception as e:
        await m.reply(f"❌ Error: `{e}`")


# ---------------- .mute ----------------
@app.on_message(filters.command("mute", prefixes=".") & filters.me)
async def mute(c, m: Message):
    if not m.reply_to_message:
        return await m.edit("⚠️ Reply karo jise mute karna hai")
    u = m.reply_to_message.from_user
    try:
        await c.restrict_chat_member(m.chat.id, u.id, ChatPermissions())
        await m.reply(f"🔇 Muted {u.first_name}")
    except Exception as e:
        await m.reply(f"❌ Error: `{e}`")


# ---------------- .unmute ----------------
@app.on_message(filters.command("unmute", prefixes=".") & filters.me)
async def unmute(c, m: Message):
    if not m.reply_to_message:
        return await m.edit("⚠️ Reply karo jise unmute karna hai")
    u = m.reply_to_message.from_user
    try:
        perms = ChatPermissions(
            can_send_messages=True,
            can_send_media_messages=True,
            can_send_other_messages=True,
            can_add_web_page_previews=True,
        )
        await c.restrict_chat_member(m.chat.id, u.id, perms)
        await m.reply(f"🔊 Unmuted {u.first_name}")
    except Exception as e:
        await m.reply(f"❌ Error: `{e}`")


# ---------------- .promote full / half ----------------
@app.on_message(filters.command("promote", prefixes=".") & filters.me)
async def promote(c, m: Message):
    if not m.reply_to_message:
        return await m.edit("⚠️ Reply karo jise promote karna hai")

    mode = "half"
    if len(m.command) > 1:
        arg = m.command[1].lower()
        if arg not in ("full", "half"):
            return await m.edit("⚠️ Usage: `.promote full` or `.promote half`")
        mode = arg

    u = m.reply_to_message.from_user

    if mode == "full":
        perms = dict(
            can_change_info=True,
            can_delete_messages=True,
            can_invite_users=True,
            can_restrict_members=True,
            can_pin_messages=True,
            can_promote_members=True,
            can_manage_chat=True,
            can_manage_video_chats=True,
        )
        title = "⭐ Promoted FULL"
    else:
        # Half: no add admin, no change info
        perms = dict(
            can_change_info=False,
            can_delete_messages=True,
            can_invite_users=True,
            can_restrict_members=True,
            can_pin_messages=True,
            can_promote_members=False,
            can_manage_chat=False,
            can_manage_video_chats=False,
        )
        title = "⭐ Promoted HALF"

    try:
        await c.promote_chat_member(m.chat.id, u.id, **perms)
        await m.reply(f"{title} — {u.first_name}")
    except Exception as e:
        await m.reply(f"❌ Error: `{e}`")


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
            can_promote_members=False,
            can_manage_chat=False,
            can_manage_video_chats=False,
        )
        await m.reply(f"⬇️ Demoted {u.first_name}")
    except Exception as e:
        await m.reply(f"❌ Error: `{e}`")


# ---------------- .pin ----------------
@app.on_message(filters.command("pin", prefixes=".") & filters.me)
async def pin(c, m: Message):
    if not m.reply_to_message:
        return await m.edit("⚠️ Reply karo jise pin karna hai")
    try:
        await c.pin_chat_message(m.chat.id, m.reply_to_message.id)
        await m.reply("📌 Pinned!")
    except Exception as e:
        await m.reply(f"❌ Error: `{e}`")


# ---------------- .del ----------------
@app.on_message(filters.command("del", prefixes=".") & filters.me)
async def delete(c, m: Message):
    if not m.reply_to_message:
        return await m.edit("⚠️ Reply karo jise delete karna hai")
    try:
        await m.reply_to_message.delete()
        await m.delete()
    except Exception as e:
        await m.reply(f"❌ Error: `{e}`")


# ---------------- .gcast / .gcast -d ----------------
@app.on_message(filters.command("gcast", prefixes=".") & filters.me)
async def gcast(c, m: Message):
    args = m.text.split(None, 1)
    to_dm = False

    if len(args) > 1 and args[1].startswith("-d"):
        to_dm = True
        msg = args[1][2:].strip()
    else:
        msg = args[1] if len(args) > 1 else None

    if not msg and m.reply_to_message:
        msg = m.reply_to_message.text or m.reply_to_message.caption

    if not msg:
        return await m.edit(
            "⚠️ Usage:\n"
            "• `.gcast <msg>` — groups\n"
            "• `.gcast -d <msg>` — DMs"
        )

    target = "DMs" if to_dm else "Groups"
    await m.edit(f"📢 Broadcasting to **{target}**...")

    sent, failed = 0, 0
    async for dialog in c.get_dialogs():
        chat_type = str(dialog.chat.type).lower()
        is_group = "group" in chat_type
        is_private = "private" in chat_type

        if to_dm and not is_private:
            continue
        if not to_dm and not is_group:
            continue

        try:
            await c.send_message(dialog.chat.id, msg)
            sent += 1
            time.sleep(0.7)
        except Exception:
            failed += 1

    await m.edit(
        f"✅ **Broadcast Done** ({target})\n"
        f"📤 Sent: {sent}\n"
        f"❌ Failed: {failed}"
    )


# ---------------- .help ----------------
@app.on_message(filters.command("help", prefixes=".") & filters.me)
async def help_userbot(c, m: Message):
    txt = (
        "╭━━━〔 ❖ 𝐓𝐇𝐎𝐑 𝐂ᴍᴅs ╮ 〕━━━╮\n"
        "┣ • .ping — Speed\n"
        "┣ • .alive — Status\n"
        "┣ • .info — User info\n"
        "┣ • .id — Chat/User ID\n"
        "┣ • .tagall <msg>\n"
        "┣ • .stoptagall — Stop\n"
        "┣ • .tagadmin <msg>\n"
        "┣ • .spam <n> <msg>\n"
        "┣ • .purge (reply)\n"
        "┣ • .kick / .ban / .unban\n"
        "┣ • .mute / .unmute\n"
        "┣ • .promote full/half\n"
        "┣ • .demote\n"
        "┣ • .pin / .del\n"
        "┣ • .gcast <msg>\n"
        "┣ • .gcast -d <msg>\n"
        "╰━━━━━━━━━━━━━━━━━━╯"
    )
    await m.reply(txt)


print(f"✅ Userbot running for @{OWNER}")
app.run()
