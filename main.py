import asyncio
import logging
import os
from datetime import datetime
import pytz
from aiogram import Bot, Dispatcher, types, F
from aiohttp import web

# MA'LUMOTLAR
TOKEN = "8361596312:AAHPJiFL1iDnDkJ8cZzdxV9a34Au10ibiNo"
ADMIN_ID = 7759817899

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Render-da uxlab qolmaslik va PORT xatosini yo'qotish uchun veb-server
async def handle(request):
    return web.Response(text="Bot ishlayapti!")

async def start_web_server():
    app = web.Application()
    app.router.add_get("/", handle)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.environ.get("PORT", 8080))
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()

KEYWORDS = ["suv", "сув", "gaz", "газ", "svet", "свет", "elektr", "электр", "chiqindi", "чиқинди", "mahalla", "маҳалла", "hokimiyat", "ҳокимият", "diniy", "диний", "muammo", "муаммо", "shikoyat", "шикоят", "adminga", "админга"]

@dp.message(F.text)
async def monitor(message: types.Message):
    if message.chat.type in ['group', 'supergroup']:
        if any(word in message.text.lower() for word in KEYWORDS):
            uz_tz = pytz.timezone('Asia/Tashkent')
            vakt = datetime.now(uz_tz).strftime("%H:%M:%S")
            sana = datetime.now(uz_tz).strftime("%d.%m.%Y")
            report = (
                f"📝 <b>YANGI MUROJAAT</b>\n"
                f"📅 Sana: {sana}\n"
                f"⏰ Vaqt: {vakt}\n"
                f"🏢 Guruh: {message.chat.title}\n"
                f"👤 Kimdan: {message.from_user.full_name}\n"
                f"💬 Xabar: <blockquote>{message.text}</blockquote>"
            )
            await bot.send_message(chat_id=ADMIN_ID, text=report, parse_mode="HTML")

async def main():
    asyncio.create_task(start_web_server()) # Serverni ishga tushirish
    await bot.delete_webhook(drop_pending_updates=True) # Konfliktni tozalash
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
