import asyncio
import logging
from aiogram import Bot, Dispatcher

from config import BOT_TOKEN
from handlers import (
    start_router,
    bloom_router,
    style_router,
    knowledge_router,
    settings_router,
    premium_router,
    payments_router,
    crypto_router,
    horoscope_router,
    mystery_box_router,
    habit_tracker_router,
    prank_router
)

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Подключаем все роутеры
dp.include_router(start_router)
dp.include_router(bloom_router)
dp.include_router(style_router)
dp.include_router(knowledge_router)
dp.include_router(settings_router)
dp.include_router(premium_router)
dp.include_router(payments_router)
dp.include_router(crypto_router)
dp.include_router(horoscope_router)
dp.include_router(mystery_box_router)
dp.include_router(habit_tracker_router)
dp.include_router(prank_router)

async def main():
    """Запуск бота"""
    print("🚀 Бот BloomStyle запущен и готов к работе!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())