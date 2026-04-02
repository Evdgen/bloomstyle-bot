import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, F
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from dotenv import load_dotenv

# Загружаем переменные окружения (BOT_TOKEN из Bothost)
load_dotenv()

# Включаем логи (полезно для отладки на хостинге)
logging.basicConfig(level=logging.INFO)

# Берём токен из переменных окружения
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Проверка: если токена нет — бот не запустится
if not BOT_TOKEN:
    raise ValueError("❌ BOT_TOKEN не найден в переменных окружения!")

# Создаём бота и диспетчера
bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()

# --- Клавиатура главного меню ---
def get_main_keyboard():
    buttons = [
        [KeyboardButton(text="🌸 Подобрать образ")],
        [KeyboardButton(text="👗 Мои сохранения")],
        [KeyboardButton(text="📞 Связаться со стилистом")],
        [KeyboardButton(text="❓ Помощь")]
    ]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

# --- Команда /start ---
@dp.message(CommandStart())
async def start_command(message: Message):
    await message.answer(
        "🌸 *BloomStyle* — твой персональный стилист в Telegram!\n\n"
        "Я помогу тебе:\n"
        "✨ Подобрать образ под твой тип внешности\n"
        "👗 Найти одежду, которая тебе идёт\n"
        "🎨 Определить цветотип и форму лица\n\n"
        "👇 Выбери действие в меню ниже",
        reply_markup=get_main_keyboard(),
        parse_mode="Markdown"
    )

# --- Команда /help ---
@dp.message(Command("help"))
async def help_command(message: Message):
    await message.answer(
        "❓ *Помощь по командам*\n\n"
        "/start — начать работу\n"
        "/help — это сообщение\n"
        "/survey — начать подбор стиля\n\n"
        "Также ты можешь пользоваться кнопками меню.",
        parse_mode="Markdown"
    )

# --- Команда /survey (заглушка) ---
@dp.message(Command("survey"))
async def survey_command(message: Message):
    await message.answer(
        "🎨 *Скоро здесь будет опросник!*\n\n"
        "Я буду задавать вопросы о:\n"
        "• Твоём цветотипе\n"
        "• Форме лица\n"
        "• Любимых стилях одежды\n\n"
        "А пока — пользуйся кнопками меню!",
        parse_mode="Markdown"
    )

# --- Кнопка "Подобрать образ" ---
@dp.message(F.text == "🌸 Подобрать образ")
async def choose_style(message: Message):
    await message.answer(
        "🎨 *Давай подберем твой идеальный образ!*\n\n"
        "Скоро здесь появится опросник по:\n"
        "• Цветотипу\n"
        "• Форме лица\n"
        "• Предпочтениям в одежде\n\n"
        "А пока — можешь написать /survey",
        parse_mode="Markdown"
    )

# --- Кнопка "Мои сохранения" ---
@dp.message(F.text == "👗 Мои сохранения")
async def my_saves(message: Message):
    await message.answer(
        "📦 *Мои сохранения*\n\n"
        "Здесь будут храниться твои любимые образы.\n"
        "Пока что тут пусто — сохрани первый образ!",
        parse_mode="Markdown"
    )

# --- Кнопка "Связаться со стилистом" ---
@dp.message(F.text == "📞 Связаться со стилистом")
async def contact_stylist(message: Message):
    await message.answer(
        "📞 *Связь со стилистом*\n\n"
        "Напиши нам: @evd_gen\n"
        "Или отправь сообщение прямо сюда — я передам!",
        parse_mode="Markdown"
    )

# --- Кнопка "Помощь" ---
@dp.message(F.text == "❓ Помощь")
async def help_button(message: Message):
    await help_command(message)

# --- Заглушка на любое другое сообщение ---
@dp.message()
async def echo(message: Message):
    await message.answer(
        "Я тебя не совсем понял 😅\n"
        "Используй кнопки меню или команду /help"
    )

# --- Запуск бота ---
async def main():
    print("🚀 Бот BloomStyle запускается...")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
