import asyncio
import logging
import os
import pytz
from datetime import datetime
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiohttp import web

# --- KONFIGURATSIYA ---
API_TOKEN = '8361596312:AAEno_t8e5eN__bTkKCDcE7GseSrhYWh9cQ'

# ADMINLAR RO'YXATI
ADMINS = [8319486490, 6554563734] 

# Kalit so'zlar (Bandlik olib tashlangan)
KEYWORDS = [
    "nasheed", "nashida", "нашида", "maruza", "ma'ruza", "маруза",
    "namoz", "намоз", "diniy muamo", "диний муаммо",
    "mahalla", "маҳалла", "gaz", "газ", "svet", "свет", "elektr", "электр",
    "xokimyat", "хокимят", "hokimiyat", "ҳоқимият", 
    "murojat", "мурожат", "murojaat", "мурожаат",
    "suv", "сув", "suz"
]

active_groups = set()
logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Render serveri uchun veb-interfeys
async def handle_render(request):
    return web.Response(text="Bot faol va 2 admin nazoratida!")

async def start_server():
    app = web.Application()
    app.router.add_get("/", handle_render)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.environ.get("PORT", 8080))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()

# --- ADMIN STATISTIKA ---
@dp.message(Command("stats"))
async def get_stats(message: types.Message):
    if message.from_user.id in ADMINS:
        count = len(active_groups)
        await message.answer(
            f"📊 <b>Bot Statistikasi</b>\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"👥 <b>Ulanishlar:</b> <code>{count} ta guruh</code>\n"
            f"📡 <b>Holat:</b> Faol ✅",
            parse_mode="HTML"
        )

# --- ASOSIY FILTR VA DIZAYN ---
@dp.message(F.text)
async def handle_messages(message: types.Message):
    if message.chat.type in ['group', 'supergroup']:
        active_groups.add(message.chat.id)

    text_lower = message.text.lower()
    is_found = any(word in text_lower for word in KEYWORDS)

    if is_found:
        uzb_tz = pytz.timezone('Asia/Tashkent')
        now = datetime.now(uzb_tz)
        
        username = f"@{message.from_user.username}" if message.from_user.username else "Mavjud emas"
        manba = message.chat.title if message.chat.type != 'private' else "Shaxsiy xabar"

        report = (
            f"<b>💎 YANGI MUROJAAT TOPILDI 💎</b>\n"
            f"<i>━━━━━━━━━━━━━━━━━━━━━━</i>\n\n"
            f"<b>📅 Sana:</b> <code>{now.strftime('%d/%m/%Y')}</code>\n"
            f"<b>⏰ Vaqt:</b> <code>{now.strftime('%H:%M:%S')}</code>\n"
            f"<b>📍 Manba:</b> <code>{manba}</code>\n"
            f"<b>📊 Jami guruhlar:</b> <code>{len(active_groups)} ta</code>\n\n"
            f"<b>👤 Foydalanuvchi:</b> {message.from_user.full_name}\n"
            f"<b>🆔 ID:</b> <code>{message.from_user.id}</code>\n"
            f"<b>🔗 Username:</b> {username}\n\n"
            f"<b>💬 Xabar mazmuni:</b>\n"
            f"<blockquote>{message.text}</blockquote>"
        )

        kb = []
        if message.chat.type in ['group', 'supergroup']:
            short_id = str(message.chat.id).replace("-100", "")
            url = f"https://t.me/c/{short_id}/{message.message_id}"
            kb.append([types.InlineKeyboardButton(text="🔎 Xabarni ko'rish", url=url)])

        # Har bir adminga yuborish
        for admin_id in ADMINS:
            try:
                await bot.send_message(
                    admin_id, 
                    report, 
                    parse_mode="HTML", 
                    reply_markup=types.InlineKeyboardMarkup(inline_keyboard=kb) if kb else None
                )
            except Exception as e:
                logging.error(f"ID {admin_id} ga yuborishda xato: {e}")

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await asyncio.gather(start_server(), dp.start_polling(bot))

if __name__ == "__main__":
    asyncio.run(main())
