import asyncio
import os
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message
from dotenv import load_dotenv
from database import init_db, get_balance, add_balance, deduct_balance
from gemini_analysis import analyze_chart

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start_handler(message: Message):
    balance = await get_balance(message.from_user.id)
    await message.answer(
        f"👋 Xush kelibsiz!\n\n"
        f"📊 Shamlar (candlestick) skrinshotini yuboring — ICT strategiya asosida tahlil qilib beraman.\n\n"
        f"💰 Balansingiz: {balance} ta tahlil\n"
        f"💳 Balans to'ldirish uchun admin bilan bog'laning."
    )

@dp.message(Command("balance"))
async def balance_handler(message: Message):
    balance = await get_balance(message.from_user.id)
    await message.answer(f"💰 Sizning balansingiz: {balance} ta tahlil qoldi")

@dp.message(Command("addcredit"))
async def addcredit_handler(message: Message):
    if message.from_user.id != ADMIN_ID:
        return
    try:
        parts = message.text.split()
        user_id = int(parts[1])
        amount = int(parts[2])
        await add_balance(user_id, amount)
        await message.answer(f"✅ {user_id} ga {amount} ta tahlil qo'shildi")
        await bot.send_message(user_id, f"💰 Balansingizga {amount} ta tahlil qo'shildi!")
    except (IndexError, ValueError):
        await message.answer("Format: /addcredit <user_id> <miqdor>")

@dp.message(F.photo)
async def photo_handler(message: Message):
    user_id = message.from_user.id
    balance = await get_balance(user_id)

    if balance <= 0:
        await message.answer(
            "❌ Balansingiz yetarli emas.\n\n"
            "💵 Narx: 5 ta tahlil — 5000 so'm\n"
            "To'lov qilish uchun admin bilan bog'laning."
        )
        return

    processing_msg = await message.answer("🔍 Tahlil qilinmoqda...")

    photo = message.photo[-1]
    file = await bot.get_file(photo.file_id)
    file_bytes = await bot.download_file(file.file_path)

    try:
        result = analyze_chart(file_bytes.read())
        await deduct_balance(user_id)
        new_balance = await get_balance(user_id)
        await processing_msg.delete()
        await message.answer(f"{result}\n\n💰 Qolgan balans: {new_balance} ta")
    except Exception as e:
        await processing_msg.delete()
        await message.answer(f"⚠️ Xatolik yuz berdi, qayta urinib ko'ring.\n{str(e)}")

async def main():
    await init_db()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
