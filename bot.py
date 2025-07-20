import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.enums import ParseMode
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from config import API_TOKEN, CHANNEL_USERNAME

bot = Bot(token=API_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()

@dp.message(F.text)
async def post_preview(message: types.Message):
    btn = InlineKeyboardButton(text="📖 Давомини кўриш", callback_data="check_sub")
    markup = InlineKeyboardMarkup(inline_keyboard=[[btn]])
    await message.answer("Пост (қисқача):\n\nБу ерда қисқача маълумот бор...", reply_markup=markup)

@dp.callback_query(F.data == "check_sub")
async def check_subscription(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    chat_member = await bot.get_chat_member(chat_id=CHANNEL_USERNAME, user_id=user_id)

    if chat_member.status in ("member", "administrator", "creator"):
        await callback.message.answer("✅ Обуна тасдиқланди.\n\n👉 Пост давоми: Бу ерда тўлиқ маълумот...")
    else:
        markup = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="📲 Каналга обуна бўлиш", url=f"https://t.me/{CHANNEL_USERNAME[1:]}")],
            [InlineKeyboardButton(text="✅ Текшириш", callback_data="check_sub")]
        ])
        await callback.message.answer("❗ Давомини кўриш учун каналга обуна бўлинг:", reply_markup=markup)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    import asyncio
    asyncio.run(dp.start_polling(bot))