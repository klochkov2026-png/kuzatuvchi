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

# Kalit so'zlar ro'yxati
KEYWORDS = [
    "suv", "сув", "gaz", "газ", "svet", "свет", "elektr", "электр",
    "chiqindi", "чиқинди", "axlat", "ахлат", "mahalla", "маҳалла",
    "hokimiyat", "хокимият", "xokimiyat", "ҳокимият", "diniy", "диний",
    "muammo", "муаммо", "shikoyat", "шикоят", "adminga", "админга"
]

@dp.message(F.text)
async def monitor_pro(message: types.Message):
    # Faqat guruhlarda ishlashi uchun
    if message.chat.type in ['group', 'supergroup']:
        text_lower = message.text.lower()
        
        # Kalit so'zlarni tekshirish
        if any(word in text_lower for word in KEYWORDS):
            # Vaqtni olish (O'zbekiston vaqti)
            vakt = datetime.now().strftime("%H:%M:%S")
            
            # Foydalanuvchi ma'lumotlari
            f_name = message.from_user.full_name
            u_id = message.from_user.id
            u_username = f"@{message.from_user.username}" if message.from_user.username else "yo'q"
            g_name = message.chat.title

            # Chiroyli hisobot matni (HTML formati)
            report = (
                f"📝 <b>YANGI MUROJAAT</b> 🚨\n"
                f"━━━━━━━━━━━━━━━\n\n"
                f"⏰ <b>Vaqt:</b> {vakt}\n"
                f"🏢 <b>Guruh:</b> {g_name}\n"
                f"👤 <b>Kimdan:</b> {f_name}\n"
                f"🆔 <b>ID:</b> <code>{u_id}</code>\n"
                f"🔗 <b>Username:</b> {u_username}\n\n"
                f"💬 <b>Xabar:</b>\n"
                f"<blockquote>{message.text}</blockquote>\n"
                f"━━━━━━━━━━━━━━━"
            )
            
            try:
                # Adminga yuborish
                await bot.send_message(chat_id=ADMIN_ID, text=report, parse_mode="HTML")
            except Exception as e:
                logging.error(f"Xatolik yuz berdi: {e}")

async def main():
    print("Bot Render-da muvaffaqiyatli ishga tushdi...")
    await dp.start_polling(bot)

# XATO SHU YERDA EDI - ENDI TO'G'IRLANDI:
if name == "main":
    asyncio.run(main())
