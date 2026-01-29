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

# Render serveri uchun veb-interfeys (Port xatosini oldini oladi)
async def handle_render(request):
    return web.Response(text="Bot is online and active!")

async def start_server():
    app = web.Application()
    app.router.add_get("/", handle_render)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.environ.get("PORT", 8080))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()

@dp.message(Command("stats"))
async def get_stats(message: types.Message):
    if message.from_user.id in ADMINS:
        await message.answer(f"📊 Statistika: {len(active_groups)} ta guruh faol.")

@dp.message(F.text)
async def handle_messages(message: types.Message):
    if message.chat.type in ['group', 'supergroup']:
        active_groups.add(message.chat.id)

    text_lower = message.text.lower()
    if any(word in text_lower for word in KEYWORDS):
        uzb_tz = pytz.timezone('Asia/Tashkent')
        now = datetime.now(uzb_tz)
        
        # HTML xatolaridan qochish uchun ismni tozalaymiz
        safe_full_name = message.from_user.full_name.replace('<', '').replace('>', '')
        
        report = (
            f"<b>🌟 YANGI MUROJAAT TOPILDI 🌟</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"📅 <b>Sana:</b> <code>{now.strftime('%d/%m/%Y')}</code>\n"
            f"⏰ <b>Vaqt:</b> <code>{now.strftime('%H:%M:%S')}</code>\n"
            f"📍 <b>Manba:</b> <code>{message.chat.title or 'Shaxsiy'}</code>\n"
            f"👤 <b>Foydalanuvchi:</b> {safe_full_name}\n"
            f"🆔 <b>ID:</b> <code>{message.from_user.id}</code>\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"💬 <b>Xabar:</b>\n<blockquote>{message.text}</blockquote>"
        )

        kb = []
        if message.chat.type in ['group', 'supergroup']:
            short_id = str(message.chat.id).replace("-100", "")
            url = f"https://t.me/c/{short_id}/{message.message_id}"
            kb.append([types.InlineKeyboardButton(text="🔎 Ko'rish", url=url)])

        for admin_id in ADMINS:
            try:
                await bot.send_message(admin_id, report, parse_mode="HTML", 
                                       reply_markup=types.InlineKeyboardMarkup(inline_keyboard=kb) if kb else None)
            except Exception as e:
                logging.error(f"ID {admin_id} ga yuborishda xato: {e}")

async def main():
    # Eski sessionlarni tozalash
    await bot.delete_webhook(drop_pending_updates=True)
    await asyncio.gather(start_server(), dp.start_polling(bot))

if __name__ == "__main__":
    asyncio.run(main())
