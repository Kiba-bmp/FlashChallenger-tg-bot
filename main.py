import asyncio
import os

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from dotenv import load_dotenv

from db import init_db, random_challenge

async def start_timer(chat_id: int, message_id: int):
    await asyncio.sleep(60)
    sessions.pop((chat_id, message_id), None)
    try:
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
sessions = {}
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
        [InlineKeyboardButton(text="✅ Выполнил: 0", callback_data="done")]
    ])
    
    # Отправляем задание с кнопкой
    sent_msg = await message.answer(text=f"\n{task_text}\n\n⏳ У вас есть 60 секунд!", reply_markup=keyboard)
    sessions[(sent_msg.chat.id, sent_msg.message_id)] = set()
    # Запускаем таймер
    asyncio.create_task(start_timer(sent_msg.chat.id, sent_msg.message_id))

@dp.callback_query(F.data == "done")
async def completed(callback: CallbackQuery):
    if not isinstance(callback.message, Message):
        await callback.answer("Задание недоступно")
        return

    key = (callback.message.chat.id, callback.message.message_id)
    participants = sessions.get(key)

    if participants is None:
        await callback.answer("Время вышло")
    elif callback.from_user.id in participants:
        await callback.answer("Уже засчитано")
    else:
        participants.add(callback.from_user.id)
        count = len(participants)
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=f"✅ Выполнил: {count}", callback_data="done")]
        ])
        await callback.message.edit_reply_markup(reply_markup=keyboard)
        await callback.answer("Засчитано")

async def main():
    init_db()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())