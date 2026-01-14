import logging
from aiogram import Bot, Dispatcher, executor, types
from datetime import datetime

# Bot tokeningizni shu yerga yozing
API_TOKEN = 'TOKEN_SHU_YERGA_YOZILADI'

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)

@dp.message_handler(content_types=types.ContentTypes.ANY)
async def handle_all_messages(message: types.Message):
    now = datetime.now()
    sana = now.strftime("%d.%m.%Y")
    vaqt = now.strftime("%H:%M:%S")
    
    # Ma'lumotlarni yig'ish
    ism = message.from_user.full_name
    user_id = message.from_user.id
    username = f"@{message.from_user.username}" if message.from_user.username else "Mavjud emas"
    xabar_matni = message.text if message.text else "[Media xabar]"
    
    # Guruh va xabar havolasini yasash
    if message.chat.type in ['group', 'supergroup']:
        guruh_nomi = message.chat.title
        # Chat ID'dan -100 ni olib tashlash kerak (havola uchun)
        chat_id_short = str(message.chat.id).replace("-100", "")
        # Xabarga to'g'ridan-to'g'ri havola
        msg_link = f"https://t.me/c/{chat_id_short}/{message.message_id}"
    else:
        guruh_nomi = "Shaxsiy chat"
        msg_link = None

    # Formatlangan xabar
    formatlangan_xabar = (
        f"📝 <b>YANGI MUROJAAT</b> 🚨\n"
        f"━━━━━━━━━━━━━━━━━━\n\n"
        f"📅 <b>Sana:</b> {sana}\n"
        f"⏰ <b>Vaqt:</b> {vaqt}\n"
        f"🏢 <b>Guruh:</b> {guruh_nomi}\n"
        f"👤 <b>Kimdan:</b> {ism}\n"
        f"🆔 <b>ID:</b> <code>{user_id}</code>\n"
        f"🔗 <b>Username:</b> {username}\n\n"
        f"💬 <b>Xabar:</b>\n"
        f"« <i>{xabar_matni}</i> »\n\n"
        f"━━━━━━━━━━━━━━━━━━"
    )

    # Inline tugma yaratish (Xabarga o'tish uchun)
    keyboard = types.InlineKeyboardMarkup()
    if msg_link:
        url_button = types.InlineKeyboardButton(text="Original xabarga o'tish ↗️", url=msg_link)
        keyboard.add(url_button)

    # Admin ID ni kiriting (o'zingizning ID raqamingiz)
    # await bot.send_message(ADMIN_ID, formatlangan_xabar, reply_markup=keyboard)
    
    # Hozircha xabarni o'sha joyning o'ziga yuboramiz (tekshirish uchun)
    await message.answer(formatlangan_xabar, reply_markup=keyboard)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
