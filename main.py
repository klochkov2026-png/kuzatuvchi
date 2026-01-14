import asyncio
import logging
import os
from datetime import datetime
import pytz  # Vaqt mintaqasi uchun
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiohttp import web

# Ma'lumotlar
API_TOKEN = '8361596312:AAEno_t8e5eN__bTkKCDcE7GseSrhYWh9cQ'
ADMIN_ID = 8319486490

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Render port xatosi uchun server
async def handle_render(request):
    return web.Response(text="Aloqachi Bot is active!")

@dp.message()
async def handle_messages(message: types.Message):
    # O'zbekiston vaqtini olish
    uzb_tz = pytz.timezone('Asia/Tashkent')
    now = datetime.now(uzb_tz)
    sana = now.strftime("%d.%m.%Y")
    vaqt = now.strftime("%H:%M:%S")
    
    # Ma'lumotlarni yig'ish
    ism = message.from_user.full_name
    u_id = message.from_user.id
    username = f"@{message.from_user.username}" if message.from_user.username else "mavjud emas"
    xabar_matni = message.text if message.text else "[Media/Fayl]"
    guruh_nomi = message.chat.title if message.chat.type != 'private' else "Shaxsiy chat 👤"

    # Xabar havolasini yasash
    msg_link = None
    if message.chat.type != 'private':
        chat_id_short = str(message.chat.id).replace("-100", "")
        msg_link = f"https://t.me/c/{chat_id_short}/{message.message_id}"

    # Yanada chiroyliroq va zamonaviy dizayn
    dizaynli_xabar = (
        f"🌟 <b>YANGI MUROJAAT</b> 🌟\n"
        f"━━━━━━━━━━━━━━━━━━\n\n"
        f"📅 <b>Sana:</b> <code>{sana}</code>\n"
        f"⏰ <b>Vaqt:</b> <code>{vaqt}</code> (Tashkent)\n"
        f"🏢 <b>Manba:</b> <i>{guruh_nomi}</i>\n\n"
        f"👤 <b>Yuboruvchi:</b> {ism}\n"
        f"🆔 <b>ID:</b> <code>{u_id}</code>\n"
        f"🔗 <b>Username:</b> {username}\n\n"
        f"💬 <b>Xabar mazmuni:</b>\n"
        f"« <b>{xabar_matni}</b> »\n\n"
        f"━━━━━━━━━━━━━━━━━━"
    )

    # Tugma (faqat guruh xabarlari uchun)
    kb = None
    if msg_link:
        kb = InlineKeyboardMarkup(inline_keyboard=[[
            InlineKeyboardButton(text="Xabarga o'tish ↗️", url=msg_link)
        ]])

    try:
        await bot.send_message(chat_id=ADMIN_ID, text=dizaynli_xabar, reply_markup=kb, parse_mode="HTML")
    except Exception as e:
        logging.error(f"Xatolik: {e}")

async def main():
    # Eski conflictlarni tozalash
    await bot.delete_webhook(drop_pending_updates=True)
    
    # Render uchun portni sozlash
    app = web.Application()
    app.router.add_get("/", handle_render)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.getenv("PORT", 10000))
    site = web.TCPSite(runner, '0.0.0.0', port)
    asyncio.create_task(site.start())

    print(f"Bot ishga tushdi! Port: {port}")
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
