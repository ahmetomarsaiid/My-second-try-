from pyrogram import filters
from pyromod import Client
from pyrogram.types import Message
from utilsdf.db import Database
from utilsdf.functions import (
    anti_bots_telegram,
    get_bin_info,
    get_cc,
    antispam,
    get_text_from_pyrogram,
    user_not_premium,
)
from utilsdf.vars import PREFIXES
from gates.adriana import adriana
from time import perf_counter


@Client.on_message(filters.command("adr", PREFIXES))
async def adr(client: Client, m: Message):
    user_id = m.from_user.id
    with Database() as db:
        if not db.is_premium(user_id):
            await user_not_premium(m)
            return
        user_info = db.get_info_user(user_id)
        is_free_user = user_info["MEMBERSHIP"]
        is_free_user = is_free_user.lower() == "free user"
        if is_free_user:
            captcha = await anti_bots_telegram(m, client)
            if not captcha:
                return
    text = get_text_from_pyrogram(m)
    ccs = get_cc(text)
    if not ccs:
        return await m.reply(
            "ððð©ðð¬ðð® <code>ðð±ð¿ð¶ð®ð»ð® â»ï¸ -Â» $3</code>\nðð¤ð§ð¢ðð© -Â» <code>/adr cc|month|year|cvc</code>",
            quote=True,
        )
    ini = perf_counter()
    cc = ccs[0]
    mes = ccs[1]
    ano = ccs[2]
    cvv = ccs[3]

    
    # check antispam
    antispam_result = antispam(user_id, user_info["ANTISPAM"], is_free_user)
    if antispam_result != False:
        return await m.reply(
            f"ðð¡ððð¨ð ðððð©... -Â» <code>{antispam_result}'s</code>", quote=True
        )
    msg_to_edit = await m.reply("ðð¡ððð¨ð ðððð©...", quote=True)
    cc_formatted = f"{cc}|{mes}|{ano}|{cvv}"

    status, result = await adriana(cc, mes, ano, cvv)

    final = perf_counter() - ini
    with Database() as db:
        db.increase_checks(user_id)

    text_ = f"""<b>ã¢ ð¾ð¾ -Â» <code>{cc_formatted}</code>
ã« ðð©ðð©ðªð¨ -Â» <code>{status}</code>
ã ððð¨ðªð¡ð© -Â» <code>{result}</code>

ã­ ð½ðð£ -Â» <code></code> - <code></code> - <code></code>
æ± ð½ðð£ð  -Â» <code></code>
é¶ ð¾ð¤ðªð£ð©ð§ð® -Â» <code></code> 

â¸ ððð©ðð¬ðð® -Â» <code>ðð±ð¿ð¶ð®ð»ð® -Â» $3</code>
ê« ððð¢ð -Â» <code>{final:0.3}'s</code>
á¥«á­¡ ð¾ðððð ðð ðð® -Â» <a href='tg://user?id={m.from_user.id}'>{m.from_user.first_name}</a> []</b>"""

    await msg_to_edit.edit(text_)
