import asyncio
import logging
import os
import pytz
import re
from datetime import datetime
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiohttp import web

# --- KONFIGURATSIYA ---
API_TOKEN = '8361596312:AAEno_t8e5eN__bTkKCDcE7GseSrhYWh9cQ'
ADMINS = [8319486490, 6554563734] 

KEYWORDS = [
    "nasheed", "nashida", "нашида", "maruza", "ma'ruza", "маруза",
    "namoz", "намоз", "diniy muamo", "диний муаммо",
    "mahalla", "маҳалла", "gaz", "газ", "svet", "свет", "elektr", "электр",
    "xokimyat", "хокимят", "hokimiyat", "ҳокимият", 
    "murojat", "мурожат", "murojaat", "мурожаат",
    "suv", "сув", "suz"
]

active_groups = set()
logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

async def handle_render(request):
    return web.Response(text="Bot Premium Mode: Active 🌟")

async def start_server():
    app = web.Application()
    app.router.add_get("/", handle_render)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.environ.get("PORT", 8080))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()

# Xabarni o'chirish tugmasi uchun handler (tozalash)
@dp.callback_query(F.data == "done")
async def process_done(callback: types.CallbackQuery):
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.answer("Murojaat bajarildi deb belgilandi ✅")

@dp.message(Command("stats"))
async def get_stats(message: types.Message):
    if message.from_user.id in ADMINS:
        await message.answer(
            f"💠 <b>TIZIM MONITORINGI</b>\n"
            f"⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n"
            f"👥 Faol ulanishlar: <code>{len(active_groups)} ta</code>\n"
            f"🛠 Adminlar soni: <code>{len(ADMINS)} ta</code>\n"
            f"🔋 Server holati: <code>Stabil</code>\n"
            f"⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯", 
            parse_mode="HTML"
        )

@dp.message(F.text)
async def handle_messages(message: types.Message):
    if message.chat.type in ['group', 'supergroup']:
        active_groups.add(message.chat.id)

    text_lower = message.text.lower()
    is_found = any(re.search(rf'\b{re.escape(word)}\b', text_lower) for word in KEYWORDS)

    if is_found:
        uzb_tz = pytz.timezone('Asia/Tashkent')
        now = datetime.now(uzb_tz)
        
        full_name = message.from_user.full_name.replace('<', '').replace('>', '')
        chat_title = message.chat.title or "Shaxsiy"

        # PREMIUM DIZAYN FORMATI
        report = (
            f"🔔 <b>YANGI MUROJAAT</b>\n"
            f"⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n"
            f"📂 <b>Ma'lumotlar:</b>\n"
            f"┣ 👤 <b>Kimdan:</b> {full_name}\n"
            f"┣ 🆔 <b>ID:</b> <code>{message.from_user.id}</code>\n"
            f"┗ 📍 <b>Manba:</b> <code>{chat_title}</code>\n"
            f"\n"
            f"📝 <b>Xabar mazmuni:</b>\n"
            f"<blockquote>{message.text}</blockquote>\n"
            f"\n"
            f"📅 <code>{now.strftime('%d.%m.%Y')}</code> | ⏰ <code>{now.strftime('%H:%M')}</code>\n"
            f"⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n"
            f"⚡️ <i>Bot avtomatik filtrlash rejimida</i>"
        )

        # Tugmalar paneli
        kb = []
        # Asliy xabarga havola (faqat guruh bo'lsa)
        if message.chat.type in ['group', 'supergroup']:
            short_id = str(message.chat.id).replace("-100", "")
            url = f"https://t.me/c/{short_id}/{message.message_id}"
            kb.append([types.InlineKeyboardButton(text="🔍 Xabarni ko'rish", url=url)])
        
        # Bajarildi tugmasi
        kb.append([types.InlineKeyboardButton(text="✅ Bajarildi", callback_data="done")])

        for admin_id in ADMINS:
            try:
                await bot.send_message(
                    admin_id, 
                    report, 
                    parse_mode="HTML", 
                    reply_markup=types.InlineKeyboardMarkup(inline_keyboard=kb)
                )
            except Exception as e:
                logging.error(f"Error: {e}")
    else:
        return

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await asyncio.gather(start_server(), dp.start_polling(bot))

if __name__ == "__main__":
    asyncio.run(main())
