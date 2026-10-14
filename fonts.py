# Bold unicode map
_BOLD  = "𝗮𝗯𝗰𝗱𝗲𝗳𝗴𝗵𝗶𝗷𝗸𝗹𝗺𝗻𝗼𝗽𝗾𝗿𝘀𝘁𝘂𝘃𝘄𝘅𝘆𝘇𝗔𝗕𝗖𝗗𝗘𝗙𝗚𝗛𝗜𝗝𝗞𝗟𝗠𝗡𝗢𝗣𝗤𝗥𝗦𝗧𝗨𝗩𝗪𝗫𝗬𝗭𝟬𝟭𝟮𝟯𝟰𝟱𝟲𝟳𝟴𝟵"
_PLAIN = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"


def bold(t: str) -> str:
    return t.translate(str.maketrans(_PLAIN, _BOLD))


# ---------- ZUDO Messages ----------

def ask_phone():
    return "📱 " + bold("Enter Phone Number") + " (+91xxxxxxxxxx):"


def ask_otp():
    return "🔑 " + bold("Enter OTP") + " (e.g., 1 2 3 4 5): Hurry, expires in 1-2 min!"


def ask_2fa():
    return "🔒 " + bold("Enter 2FA Password") + ":"


def wrong_2fa(left: int):
    return bold("Your 2FA password is incorrect.") + \
           f" Please re-enter the password (only {left} tries left)."


def hosting():
    return "🚖 " + bold("Hosting userbot, please wait...")


def success():
    return bold("Success Userbot Hosted!") + "\nUse .ping to check."


def ping_box(speed, uptime, owner):
    return (
        "╭━━━〔 ❖ " + bold("ZUDO") + " ™ ╮ 〕━━━╮\n"
        f"┣ • {bold('Speed')}   : {speed} ms\n"
        f"┣ • {bold('Status')}  : ⚡ {bold('Fast')}\n"
        f"┣ • {bold('Uptime')}  : {uptime}\n"
        f"┣ • {bold('Owner')}   : {owner}\n"
        "╰━━━━━━━━━━━━━━━━━━╯"
    )
