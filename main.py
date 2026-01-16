import asyncio
import logging
from datetime import datetime
import pytz
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command

# --- MA'LUMOTLAR ---
API_TOKEN = 'BU_YERGA_TOKENINGIZNI_YOZING'
ADMIN_ID = 831948490  # Sizning ID raqamingiz

# --- KALIT SO'ZLAR RO'YXATI (Lotin va Kirill) ---
KEYWORDS = [
    "nasheed", "nashida", "нашида", "maruza", "ma'ruza", "маруза",
    "namoz", "намоз", "diniy muamo", "диний муаммо",
    "mahalla", "маҳалла", "gaz", "газ", "svet", "свет", 
    "xokimyat", "хокимят", "hokimiyat", "ҳокимият", 
    "murojat", "мурожат", "murojaat", "мурожаат",
    "vakant", "вакант", "ish", "иш", "suv", "сув"
]

# Bot necha guruhda ekanini vaqtinchalik saqlash uchun
active_groups = set()

# Logging sozlamalari
logging.basicConfig(level=logging.INFO)

# Bot va Dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# --- ADMIN PANEL (STATISTIKA) ---
@dp.message(Command("stats"))
async def get_stats(message: types.Message):
    if message.from_user.id == ADMIN_ID:
        await message.answer(
            f"📊 BOT STATISTIKASI\n\n"
            f"👥 Faol guruhlar: {len(active_groups)} ta\n"
            f"✅ Holat: Ishlamoqda",
            parse_mode="Markdown"
        )

# --- ASOSIY XABARLARNI QAYTA ISHLASH ---
@dp.message(F.text) # FAQAT MATNLI XABARLARNI FILTRLAYDI
async def handle_creative_messages(message: types.Message):
    # Guruh ID sini saqlab borish
    if message.chat.type in ['group', 'supergroup']:
        active_groups.add(message.chat.id)

    # Xabarni kichik harfga o'tkazib tekshirish
    user_text = message.text.lower()
    
    # Kalit so'z bormi?
    if any(word in user_text for word in KEYWORDS):
        
        # O'zbekiston vaqti
        uzb_tz = pytz.timezone('Asia/Tashkent')
        now = datetime.now(uzb_tz)
        
        # Dizayn elementlari
        line = "✨ ━━━━━━━━━━━━━━━━━━ ✨"
        
        ism = message.from_user.full_name
        username = f"@{message.from_user.username}" if message.from_user.username else "Yashirin"
        guruh_nomi = message.chat.title if message.chat.title else "Shaxsiy chat"
        
        # Xabarga to'g'ridan-to'g'ri havola yasash
        msg_link = ""
        if message.chat.type in ['group', 'supergroup']:
            chat_id_short = str(message.chat.id).replace("-100", "")
            msg_link = f"https://t.me/c/{chat_id_short}/{message.message_id}"

        # Kreativ Report Dizayni
        report = (
            f"{line}\n"
            f"🚀 YANGI MUROJAAT TOPILDI\n\n"
            f"📅 Sana: {now.strftime('%d.%m.%Y')}\n"
            f"⏰ Vaqt: {now.strftime('%H:%M:%S')}\n"
            f"📍 Manba: {guruh_nomi}\n"
            f"📊 Jami faol guruhlar: {len(active_groups)}\n\n"
            f"👤 Yuboruvchi: {ism}\n"
            f"🆔 ID: {message.from_user.id}\n"
            f"🔗 Profil: {username}\n\n"
            f"💬 Xabar:\n« {message.text} »\n\n"
        )
        
        # Agar guruh bo'lsa, xabarga havola tugmasini qo'shish
        kb = []
        if msg_link:
            kb.append([types.InlineKeyboardButton(text="🔎 Xabarni ko'rish", url=msg_link)])
        
        keyboard = types.InlineKeyboardMarkup(inline_keyboard=kb)

        # Adminga yuborish
        await bot.send_message(
            ADMIN_ID, 
            report, 
            parse_mode="Markdown", 
            reply_markup=keyboard if kb else None
        )

# Botni ishga tushirish
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Bot to'xtatildi")
