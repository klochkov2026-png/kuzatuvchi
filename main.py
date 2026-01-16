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
ADMIN_ID = 8319486490

KEYWORDS = [
    "nasheed", "nashida", "нашида", "maruza", "ma'ruza", "маруза",
    "namoz", "намоз", "diniy muamo", "диний муаммо",
    "mahalla", "маҳалла", "gaz", "газ", "svet", "свет", "elektr", "электр",
    "xokimyat", "хокимят", "hokimiyat", "ҳокимият", 
    "murojat", "мурожат", "murojaat", "мурожаат", "ish", "иш", "suv", "сув"
]

active_groups = set()
logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# --- RENDER PORT XATOSI UCHUN SERVER ---
async def handle_render(request):
    return web.Response(text="Bot is running smoothly!")

async def start_server():
    app = web.Application()
    app.router.add_get("/", handle_render)
    runner = web.AppRunner(app)
    await runner.setup()
    # Render PORT muhit o'zgaruvchisini avtomatik beradi
    port = int(os.environ.get("PORT", 8080))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()

# --- ADMIN STATISTIKA ---
@dp.message(Command("stats"))
async def get_stats(message: types.Message):
    if message.from_user.id == ADMIN_ID:
        await message.answer(f"📊 Statistika:\nJami faol guruhlar: {len(active_groups)} ta", parse_mode="Markdown")

# --- ASOSIY FILTR ---
@dp.message(F.text)
async def handle_messages(message: types.Message):
    if message.chat.type in ['group', 'supergroup']:
        active_groups.add(message.chat.id)

    text_lower = message.text.lower()
    if any(word in text_lower for word in KEYWORDS):
        uzb_tz = pytz.timezone('Asia/Tashkent')
        now = datetime.now(uzb_tz)
        
        # Markdown xatosini oldini olish uchun xabarni tozalash
        # Maxsus belgilarni olib tashlaymiz yoki o'zgartiramiz
        safe_text = message.text.replace("_", " ").replace("*", "").replace("", "")
        
        report = (
            f"🌟 *YANGI MUROJAAT* 🌟\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"📅 *Sana:* {now.strftime('%d.%m.%Y')}\n"
            f"⏰ *Vaqt:* {now.strftime('%H:%M:%S')}\n"
            f"📍 *Manba:* {message.chat.title or 'Shaxsiy'}\n"
            f"👤 *Yuboruvchi:* {message.from_user.full_name}\n"
            f"🆔 *ID:* {message.from_user.id}`\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"💬 *Xabar:*\n{safe_text}"
        )

        kb = []
        if message.chat.type in ['group', 'supergroup']:
            short_id = str(message.chat.id).replace("-100", "")
            url = f"https://t.me/c/{short_id}/{message.message_id}"
            kb.append([types.InlineKeyboardButton(text="🔎 Ko'rish", url=url)])

        try:
            await bot.send_message(
                ADMIN_ID, 
                report, 
                parse_mode="Markdown", 
                reply_markup=types.InlineKeyboardMarkup(inline_keyboard=kb) if kb else None
            )
        except Exception as e:
            logging.error(f"Xabar yuborishda xato: {e}")

async def main():
    # Bir vaqtda server va botni ishga tushirish
    await asyncio.gather(start_server(), dp.start_polling(bot))

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        pass
