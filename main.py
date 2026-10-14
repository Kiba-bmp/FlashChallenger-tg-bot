import asyncio
import os

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from dotenv import load_dotenv

from db import init_db, random_challenge
load_dotenv()
bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher()
used = {}

@dp.message(Command("start"))
async def start(message: Message):
    await message.answer("Привет! Отправь /challenge, и я дам задание.")

@dp.message(Command("challenge"))
async def challenge(message: Message):
    seen = used.setdefault(message.chat.id, set())
    row = random_challenge(seen)
    if row is None:  # все задания выданы - начинаем круг заново
        seen.clear()
        row = random_challenge()
    if row is None:
        await message.answer("В базе пока нет заданий.")
        return
    seen.add(row[0])
    await message.answer(row[1])

async def main():
    init_db()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())