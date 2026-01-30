import asyncio
import logging
import os
import pytz
import re
from datetime import datetime
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command, ChatMemberUpdatedFilter
from aiogram.types import ChatMemberUpdated
from aiohttp import web

# --- KONFIGURATSIYA ---
API_TOKEN = '8361596312:AAEno_t8e5eN__bTkKCDcE7GseSrhYWh9cQ'
ADMINS = [8319486490, 6554563734] 

KEYWORDS = [
    "nasheed", "nashida", "нашида", "maruza", "ma'ruza", "маруза",
    "namoz", "намоз", "diniy muamo", "диний муаммо",
    "mahalla", "маҳалла", "gaz", "газ", "svet", "свет", "elektr", "электр",
    "xokimyat", "хокимят", "hokimiyat", "ҳокимият", 
    "murojat", "мурожат", "murojaat", "мурожаат",
    "suv", "сув", "suz"
]

# Guruhlar ro'yxati (ID lar to'plami)
all_joined_groups = set()

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Render serveri
async def handle_render(request):
    return web.Response(text="Bot To'liq Monitoring Rejimida!")

async def start_server():
    app = web.Application()
    app.router.add_get("/", handle_render)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.environ.get("PORT", 8080))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()

# --- GURUHLARNI ANIQLASH (Yangi qo'shilganda yoki chiqarilganda) ---
@dp.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=True))
async def on_my_chat_member_update(event: ChatMemberUpdated):
    chat_id = event.chat.id
    # Agar bot guruhga qo'shilsa (admin yoki a'zo sifatida)
    if event.new_chat_member.status in ["member", "administrator"]:
        all_joined_groups.add(chat_id)
        for admin_id in ADMINS:
            await bot.send_message(admin_id, f"➕ <b>Yangi ulanish:</b> {event.chat.title}\nID: <code>{chat_id}</code>", parse_mode="HTML")
    
    # Agar bot guruhdan chiqarilsa
    elif event.new_chat_member.status in ["left", "kicked"]:
        if chat_id in all_joined_groups:
            all_joined_groups.remove(chat_id)
            for admin_id in ADMINS:
                await bot.send_message(admin_id, f"➖ <b>Guruhdan chiqish:</b> {event.chat.title}", parse_mode="HTML")

# --- ADMIN STATISTIKA ---
@dp.message(Command("stats"))
async def get_stats(message: types.Message):
    if message.from_user.id in ADMINS:
        await message.answer(
            f"📊 <b>BOTNING TO'LIQ STATISTIKASI</b>\n"
            f"⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n"
            f"📢 Jami ulangan guruhlar: <b>{len(all_joined_groups)} ta</b>\n"
            f"👤 Mas'ul adminlar: <b>{len(ADMINS)} ta</b>\n"
            f"⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯", 
            parse_mode="HTML"
        )

# --- XABARLARNI FILTRLASH ---
@dp.message(F.text)
async def handle_messages(message: types.Message):
    # Har qanday kelgan xabardan guruh ID sini ro'yxatga qo'shib qo'yamiz (aniqlik uchun)
    if message.chat.type in ['group', 'supergroup']:
        all_joined_groups.add(message.chat.id)

    text_lower = message.text.lower()
    is_found = any(re.search(rf'\b{re.escape(word)}\b', text_lower) for word in KEYWORDS)

    if is_found:
        uzb_tz = pytz.timezone('Asia/Tashkent')
        now = datetime.now(uzb_tz)
        report = (
            f"🔔 <b>YANGI MUROJAAT</b>\n"
            f"⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n"
            f"👤 <b>Kimdan:</b> {message.from_user.full_name}\n"
            f"📍 <b>Guruh:</b> <code>{message.chat.title}</code>\n"
            f"📝 <b>Xabar:</b> <blockquote>{message.text}</blockquote>\n"
            f"⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n"
            f"📅 {now.strftime('%d.%m.%Y')} | ⏰ {now.strftime('%H:%M')}\n"
            f"🔢 Jami ulanishlar: <b>{len(all_joined_groups)} ta</b>"
        )

        kb = []
        if message.chat.type in ['group', 'supergroup']:
            short_id = str(message.chat.id).replace("-100", "")
            kb.append([types.InlineKeyboardButton(text="🔍 Xabarni ko'rish", url=f"https://t.me/c/{short_id}/{message.message_id}")])

        for admin_id in ADMINS:
            try:
                await bot.send_message(admin_id, report, parse_mode="HTML", reply_markup=types.InlineKeyboardMarkup(inline_keyboard=kb))
            except: pass

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await asyncio.gather(start_server(), dp.start_polling(bot))

if __name__ == "__main__":
    asyncio.run(main())
