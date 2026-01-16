import asyncio
import logging
import pytz
from datetime import datetime
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command

# --- KONFIGURATSIYA ---
API_TOKEN = '8361596312:AAEno_t8e5eN__bTkKCDcE7GseSrhYWh9cQ'
ADMIN_ID = 8319486490  # Yangilangan ID raqamingiz

# --- KALIT SO'ZLAR RO'YXATI ---
KEYWORDS = [
    "nasheed", "nashida", "нашида", "maruza", "ma'ruza", "маруза",
    "namoz", "намоз", "diniy muamo", "диний муаммо",
    "mahalla", "маҳалла", "gaz", "газ", "svet", "свет", "elektr", "электр",
    "xokimyat", "хокимят", "hokimiyat", "ҳокимият", 
    "murojat", "мурожат", "murojaat", "мурожаат",
    "vakant", "вакант", "ish", "иш", "suv", "сув", "suz"
]

active_groups = set()
logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# --- ADMIN STATISTIKA ---
@dp.message(Command("stats"))
async def get_stats(message: types.Message):
    if message.from_user.id == ADMIN_ID:
        await message.answer(
            f"📊 BOT STATISTIKASI\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"👥 Faol guruhlar: {len(active_groups)} ta\n"
            f"📡 Holat: Ishlamoqda ✅",
            parse_mode="Markdown"
        )

# --- ASOSIY FILTR VA DIZAYN ---
@dp.message(F.text)
async def filter_and_report(message: types.Message):
    if message.chat.type in ['group', 'supergroup']:
        active_groups.add(message.chat.id)

    text_lower = message.text.lower()
    if any(word in text_lower for word in KEYWORDS):
        uzb_tz = pytz.timezone('Asia/Tashkent')
        now = datetime.now(uzb_tz)
        
        full_name = message.from_user.full_name
        user_id = message.from_user.id
        username = f"@{message.from_user.username}" if message.from_user.username else "🚫 Mavjud emas"
        group_title = message.chat.title if message.chat.type != 'private' else "👤 Shaxsiy chat"
        
        msg_link = ""
        if message.chat.type in ['group', 'supergroup']:
            short_id = str(message.chat.id).replace("-100", "")
            msg_link = f"https://t.me/c/{short_id}/{message.message_id}"

        report_text = (
            f"🌟 YANGI MUROJAAT TOPILDI 🌟\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"📅 Sana: {now.strftime('%d.%m.%Y')}\n"
            f"⏰ Vaqt: {now.strftime('%H:%M:%S')}\n"
            f"📍 Guruh: {group_title}\n"
            f"📊 Bot faolligi: {len(active_groups)} guruhda\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"👤 Yuboruvchi: {full_name}\n"
            f"🆔 ID: {user_id}\n"
            f"🔗 Username: {username}\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"💬 Xabar:\n_« {message.text} »_\n"
        )

        buttons = []
        if msg_link:
            buttons.append([types.InlineKeyboardButton(text="🔎 Xabarni guruhda ko'rish", url=msg_link)])
        
        reply_markup = types.InlineKeyboardMarkup(inline_keyboard=buttons)

        await bot.send_message(
            ADMIN_ID, 
            report_text, 
            parse_mode="Markdown", 
            reply_markup=reply_markup if buttons else None
        )

async def main():
    print("Bot yangilangan ID bilan ishga tushdi...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        pass
