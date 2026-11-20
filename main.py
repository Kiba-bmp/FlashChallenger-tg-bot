import asyncio
import os

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from dotenv import load_dotenv

from db import init_db, random_challenge

async def start_timer(chat_id: int):
    """Запускает таймер на 60 секунд"""
    await asyncio.sleep(60)
    try:
        # Отправляем сообщение об окончании времени
        await bot.send_message(chat_id, "Время вышло! Кто успел выполнить задание?")
    except Exception as e:
        print(f"Ошибка при отправке сообщения о конце таймера: {e}")
load_dotenv()
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN: raise ValueError("Нет токена в .env")
bot = Bot(token=TOKEN)
dp = Dispatcher()
used = {}

@dp.message(Command("start"))
async def start(message: Message):
    await message.answer("Привет! Отправь /challenge, и я дам задание.")

@dp.message(Command("challenge"))
async def challenge(message: Message):
    seen = used.setdefault(message.chat.id, set())
    row = random_challenge(seen)
    
    if row is None:
        seen.clear()
        row = random_challenge()
        
    if row is None:
        await message.answer("В базе пока нет заданий.")
        return
        
    task_id, task_text = row
    seen.add(task_id)
    
    # Создаем кнопку 
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Выполнил", callback_data="done")]
    ])
    
    # Отправляем задание с кнопкой
    sent_msg = await message.answer(text=f"\n{task_text}\n\n⏳ У вас есть 60 секунд!", reply_markup=keyboard)
    
    # Запускаем таймер
    asyncio.create_task(start_timer(message.chat.id))
async def main():
    init_db()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())