import asyncio
import logging
from datetime import datetime
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Bot ma'lumotlari
API_TOKEN = '8361596312:AAHPJiFL1iDnDkJ8cZzdxV9a34Au10ibiNo'
ADMIN_ID = 7759817899

# Loglarni sozlash
logging.basicConfig(level=logging.INFO)

# Bot va Dispatcherni ishga tushirish (aiogram 3.x)
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

@dp.message(F.text)
async def handle_incoming_messages(message: types.Message):
    # Hozirgi vaqt va sanani olish
    now = datetime.now()
    sana = now.strftime("%d.%m.%Y")
    vaqt = now.strftime("%H:%M:%S")
    
    # Ma'lumotlarni yig'ish
    ism = message.from_user.full_name
    u_id = message.from_user.id
    username = f"@{message.from_user.username}" if message.from_user.username else "Mavjud emas"
    xabar_matni = message.text
    
    # Havola yasash (Guruhlar uchun)
    msg_link = None
    guruh_nomi = "Shaxsiy chat"
    
    if message.chat.type in ['group', 'supergroup']:
        guruh_nomi = message.chat.title
        chat_id_short = str(message.chat.id).replace("-100", "")
        msg_link = f"https://t.me/c/{chat_id_short}/{message.message_id}"

    # Rasmda hohlagan dizayningiz (HTML formatida)
    formatlangan_xabar = (
        f"📝 <b>YANGI MUROJAAT</b> 🚨\n"
        f"────────────────────\n\n"
        f"📅 <b>Sana:</b> {sana}\n"
        f"⏰ <b>Vaqt:</b> {vaqt}\n"
        f"🏢 <b>Guruh:</b> {guruh_nomi}\n"
        f"👤 <b>Kimdan:</b> {ism}\n"
        f"🆔 <b>ID:</b> <code>{u_id}</code>\n"
        f"🔗 <b>Username:</b> {username}\n\n"
        f"💬 <b>Xabar:</b>\n"
        f"« <i>{xabar_matni}</i> »\n\n"
        f"────────────────────"
    )

    # Inline tugma
    keyboard = None
    if msg_link:
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Guruhdagi xabarga o'tish ↗️", url=msg_link)]
        ])

    # Xabarni Adminga yuborish
    try:
        await bot.send_message(
            chat_id=ADMIN_ID, 
            text=formatlangan_xabar, 
            reply_markup=keyboard,
            parse_mode="HTML"
        )
    except Exception as e:
        logging.error(f"Xatolik: {e}")

async def main():
    print("Bot ishga tushdi (aiogram 3.x)...")
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Bot to'xtatildi")
