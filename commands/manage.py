import os, sys, time, signal, subprocess
from pyrogram import filters
from pyrogram.types import Message
from config import API_ID, API_HASH
import fonts
import database as db
from commands.host import USERBOT_TEMPLATE, RUNNING


def register(app):

    # ---------- /status ----------
    @app.on_message(filters.command("status") & filters.private)
    async def status(c, m: Message):
        doc = await db.get_hosted(m.from_user.id)
        if not doc:
            return await m.reply("❌ No userbot hosted. Use /host.")
        uptime = int(time.time() - doc.get("started_at", 0))
        d, r = divmod(uptime, 86400); h, r = divmod(r, 3600); mi, s = divmod(r, 60)
        await m.reply(
            f"🟢 {fonts.bold('Running')}\n"
            f"👤 Owner: @{doc.get('owner')}\n"
            f"🆔 PID: `{doc.get('pid')}`\n"
            f"⏱ Uptime: {d}d {h}h {mi}m {s}s"
        )

    # ---------- /logout ----------
    @app.on_message(filters.command("logout") & filters.private)
    async def logout(c, m: Message):
        uid = m.from_user.id
        doc = await db.get_hosted(uid)
        if not doc:
            return await m.reply("❌ Nothing to log out.")

        # Kill process
        pid = doc.get("pid")
        try:
            os.kill(pid, signal.SIGTERM)
        except Exception:
            pass

        # Remove file
        try:
            os.remove(f"userbots/ub_{uid}.py")
        except Exception:
            pass

        await db.delete_hosted(uid)
        RUNNING.pop(uid, None)
        await m.reply("👋 Logged out successfully.")

    # ---------- /restart ----------
    @app.on_message(filters.command("restart") & filters.private)
    async def restart(c, m: Message):
        uid = m.from_user.id
        doc = await db.get_hosted(uid)
        if not doc:
            return await m.reply("❌ No userbot hosted. Use /host.")

        # Kill old
        try:
            os.kill(doc.get("pid"), signal.SIGTERM)
        except Exception:
            pass

        # Re-launch from saved session
        path = f"userbots/ub_{uid}.py"
        log  = open(f"userbots/ub_{uid}.log", "a", encoding="utf-8")
        proc = subprocess.Popen([sys.executable, path], stdout=log, stderr=log)
        RUNNING[uid] = proc

        await db.save_hosted(uid, doc["session"], doc["owner"], proc.pid)
        await m.reply("♻️ Userbot restarted.")
