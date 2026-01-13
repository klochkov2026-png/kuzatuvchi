import asyncio
import logging
import os
from datetime import datetime
import pytz  # Vaqt mintaqasi uchun
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
        text_lower = message.text.lower()
        if any(word in text_lower for word in KEYWORDS):
            # O'zbekiston vaqtini sozlash
            toshkent_vakti = pytz.timezone('Asia/Tashkent')
            vakt = datetime.now(toshkent_vakti).strftime("%H:%M:%S")
            sana = datetime.now(toshkent_vakti).strftime("%d.%m.%Y")

            report = (
                f"📝 <b>YANGI MUROJAAT</b> 🚨\n"
                f"━━━━━━━━━━━━━━━\n\n"
                f"📅 <b>Sana:</b> {sana}\n"
                f"⏰ <b>Vaqt:</b> {vakt}\n"
                f"🏢 <b>Guruh:</b> {message.chat.title}\n"
                f"👤 <b>Kimdan:</b> {message.from_user.full_name}\n"
                f"🆔 <b>ID:</b> <code>{message.from_user.id}</code>\n"
                f"🔗 <b>Username:</b> @{message.from_user.username if message.from_user.username else 'yoq'}\n\n"
                f"💬 <b>Xabar:</b>\n"
                f"<blockquote>{message.text}</blockquote>\n"
                f"━━━━━━━━━━━━━━━"
            )
            try:
                await bot.send_message(chat_id=ADMIN_ID, text=report, parse_mode="HTML")
            except Exception as e:
                logging.error(f"Yuborishda xato: {e}")

async def main():
    # Eski ulanishlarni o'chirib yuborish (Conflict xatosini oldini olish uchun)
    await bot.delete_webhook(drop_pending_updates=True)
    print("Bot Toshkent vaqti bilan Render-da ishga tushdi!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
