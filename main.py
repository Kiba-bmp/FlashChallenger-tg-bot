import asyncio
import os

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from dotenv import load_dotenv

from db import init_db, random_challenge
#source .venv/bin/activate
load_dotenv()
bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher()
last_task = {}

@dp.message(Command("start"))
async def start(message: Message):
    await message.answer("Привет! Отправь /challenge, и я дам задание.")

@dp.message(Command("challenge"))
async def challenge(message: Message):
    row = random_challenge(last_task.get(message.chat.id, 0))
    if row is None:
        await message.answer("В базе пока нет заданий.")
        return
    last_task[message.chat.id] = row[0]
    await message.answer(row[1])

async def main():
    init_db()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())