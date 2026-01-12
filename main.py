import asyncio
import logging
from datetime import datetime
from aiogram import Bot, Dispatcher, types, F

# MA'LUMOTLAR
TOKEN = "8361596312:AAHPJiFL1iDnDkJ8cZzdxV9a34Au10ibiNo"
ADMIN_ID = 7759817899

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Kalit so'zlar
KEYWORDS = ["suv", "сув", "gaz", "газ", "svet", "свет", "elektr", "электр", "chiqindi", "чиқинди", "mahalla", "маҳалла", "hokimiyat", "ҳокимият", "diniy", "диний", "muammo", "муаммо", "shikoyat", "шикоят", "adminga", "админга"]

@dp.message(F.text)
async def monitor(message: types.Message):
    if message.chat.type in ['group', 'supergroup']:
        if any(word in message.text.lower() for word in KEYWORDS):
            vakt = datetime.now().strftime("%H:%M:%S")
            report = (
                f"🚨 <b>YANGI MUROJAAT</b>\n"
                f"━━━━━━━━━━━━━━━\n"
                f"⏰ <b>Vaqt:</b> {vakt}\n"
                f"🏢 <b>Guruh:</b> {message.chat.title}\n"
                f"👤 <b>Kimdan:</b> {message.from_user.full_name}\n"
                f"🆔 <b>ID:</b> <code>{message.from_user.id}</code>\n\n"
                f"💬 <b>Xabar:</b>\n"
                f"<blockquote>{message.text}</blockquote>"
            )
            try:
                await bot.send_message(chat_id=ADMIN_ID, text=report, parse_mode="HTML")
            except Exception as e:
                logging.error(f"Xato: {e}")

async def main():
    print("Bot Render-da ishlamoqda...")
    await dp.start_polling(bot)

if name == "main":
    asyncio.run(main())
