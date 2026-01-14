import logging
from aiogram import Bot, Dispatcher, executor, types
from datetime import datetime

# Bot ma'lumotlari
API_TOKEN = '8361596312:AAHPJiFL1iDnDkJ8cZzdxV9a34Au10ibiNo'
ADMIN_ID = 7759817899  # Sizning ID raqamingiz

# Loglarni sozlash
logging.basicConfig(level=logging.INFO)

# Bot va Dispatcherni ishga tushirish
bot = Bot(token=API_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)

@dp.message_handler(content_types=types.ContentTypes.ANY)
async def handle_incoming_messages(message: types.Message):
    # Faqat guruhlardan kelgan xabarlarni tutib olish (yoki hammasini)
    # Agar bot guruhda bo'lsa va sizga yuborishi kerak bo'lsa:
    
    now = datetime.now()
    sana = now.strftime("%d.%m.%Y")
    vaqt = now.strftime("%H:%M:%S")
    
    # Ma'lumotlarni yig'ish
    ism = message.from_user.full_name
    u_id = message.from_user.id
    username = f"@{message.from_user.username}" if message.from_user.username else "Mavjud emas"
    xabar_matni = message.text if message.text else "[Media xabar/Rasm]"
    
    # Havola yasash (Guruhlar uchun)
    msg_link = None
    guruh_nomi = "Shaxsiy chat"
    
    if message.chat.type in ['group', 'supergroup']:
        guruh_nomi = message.chat.title
        chat_id_short = str(message.chat.id).replace("-100", "")
        msg_link = f"https://t.me/c/{chat_id_short}/{message.message_id}"

    # Rasmga asoslangan dizayn
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
    keyboard = types.InlineKeyboardMarkup()
    if msg_link:
        url_button = types.InlineKeyboardButton(text="Guruhdagi xabarga o'tish ↗️", url=msg_link)
        keyboard.add(url_button)

    # Xabarni faqat sizga (Adminga) yuborish
    try:
        await bot.send_message(chat_id=ADMIN_ID, text=formatlangan_xabar, reply_markup=keyboard)
    except Exception as e:
        logging.error(f"Xabar yuborishda xatolik: {e}")

if __name__ == '__main__':
    print("Bot muvaffaqiyatli ishga tushdi...")
    executor.start_polling(dp, skip_updates=True)
