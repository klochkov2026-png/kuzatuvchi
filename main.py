import asyncio
import logging
import os
import pytz
import re
import sqlite3
from datetime import datetime
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command, ChatMemberUpdatedFilter
from aiogram.types import ChatMemberUpdated
from aiohttp import web

# --- KONFIGURATSIYA ---
API_TOKEN = '8361596312:AAEno_t8e5eN__bTkKCDcE7GseSrhYWh9cQ'
ADMINS = [8319486490, 6554563734] 

KEYWORDS = [
    "nasheed", "nashida", "нашида", "maruza", "ma'ruza", "маруза",
    "namoz", "намоз", "diniy muamo", "диний муаммо",
    "mahalla", "маҳалла", "gaz", "газ", "svet", "свет", "elektr", "электр",
    "xokimyat", "хокимят", "hokimiyat", "ҳоқимият", 
    "murojat", "мурожат", "murojaat", "мурожаат",
    "suv", "сув", "suz"
]

# --- DATABASE BILAN ISHLASH ---
def init_db():
    conn = sqlite3.connect('aloqachi_data.db')
    cursor = conn.cursor()
    # Guruh ID va Nomini saqlash uchun jadval
    cursor.execute('CREATE TABLE IF NOT EXISTS groups (chat_id INTEGER PRIMARY KEY, title TEXT)')
    conn.commit()
    conn.close()

def update_group_in_db(chat_id, title):
    conn = sqlite3.connect('aloqachi_data.db')
    cursor = conn.cursor()
    cursor.execute('INSERT OR REPLACE INTO groups (chat_id, title) VALUES (?, ?)', (chat_id, title))
    conn.commit()
    conn.close()

def delete_group_from_db(chat_id):
    conn = sqlite3.connect('aloqachi_data.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM groups WHERE chat_id = ?', (chat_id,))
    conn.commit()
    conn.close()

def get_all_groups():
    conn = sqlite3.connect('aloqachi_data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT title FROM groups')
    rows = cursor.fetchall()
    conn.close()
    return [row[0] for row in rows]

init_db()
bot = Bot(token=API_TOKEN)
dp = Dispatcher()
logging.basicConfig(level=logging.INFO)

# Render uchun server
async def handle_render(request):
    return web.Response(text="Bot Professional Rejimda! 🚀")

async def start_server():
    app = web.Application()
    app.router.add_get("/", handle_render)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.environ.get("PORT", 8080))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()

# --- GURUHLARNI KUZATISH (Yangi qo'shilganda yoki chiqarilganda) ---
@dp.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=True))
async def on_my_chat_member_update(event: ChatMemberUpdated):
    chat_id = event.chat.id
    chat_title = event.chat.title
    if event.new_chat_member.status in ["member", "administrator"]:
        update_group_in_db(chat_id, chat_title)
    elif event.new_chat_member.status in ["left", "kicked"]:
        delete_group_from_db(chat_id)

# --- PROFESSIONAL STATISTIKA ---
@dp.message(Command("stats"))
async def get_stats(message: types.Message):
    if message.from_user.id in ADMINS:
        groups_list = get_all_groups()
        total = len(groups_list)
        
        if total == 0:
            res_text = "📭 Hozircha ulangan guruhlar yo'q."
        else:
            res_text = f"📊 <b>BOT ULANGAN GURUHLAR</b> (Jami: {total})\n"
            res_text += "⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n"
            for i, title in enumerate(groups_list, 1):
                res_text += f"{i}. {title}\n"
            res_text += "⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯"
        
        await message.answer(res_text, parse_mode="HTML")

# --- XABARLARNI FILTRLASH ---
@dp.message(F.text)
async def handle_messages(message: types.Message):
    if message.chat.type in ['group', 'supergroup']:
        update_group_in_db(message.chat.id, message.chat.title)

    text_lower = message.text.lower()
    if any(re.search(rf'\b{re.escape(word)}\b', text_lower) for word in KEYWORDS):
        uzb_tz = pytz.timezone('Asia/Tashkent')
        now = datetime.now(uzb_tz)
        
        report = (
            f"💠 <b>YANGI MUROJAAT</b>\n"
            f"⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n"
            f"👤 <b>Kimdan:</b> {message.from_user.full_name}\n"
            f"📍 <b>Guruh:</b> <code>{message.chat.title}</code>\n\n"
            f"📝 <b>Xabar:</b>\n<blockquote>{message.text}</blockquote>\n\n"
            f"📅 {now.strftime('%d.%m.%Y')} | ⏰ {now.strftime('%H:%M')}\n"
            f"⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯"
        )

        kb = [[types.InlineKeyboardButton(text="🔍 Xabarni ko'rish", url=f"https://t.me/c/{str(message.chat.id).replace('-100', '')}/{message.message_id}")]]
        
        for admin in ADMINS:
            try: await bot.send_message(admin, report, parse_mode="HTML", reply_markup=types.InlineKeyboardMarkup(inline_keyboard=kb))
            except: pass

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await asyncio.gather(start_server(), dp.start_polling(bot))

if __name__ == "__main__":
    asyncio.run(main())
