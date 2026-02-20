import asyncio
import logging
import os
from aiogram import Bot, Dispatcher
from aiohttp import web

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

# ==================== ЗАГЛУШКА ДЛЯ RENDER ====================
async def handle_health(request):
    """Простой эндпоинт для проверки здоровья"""
    return web.Response(text="Бот работает!")

async def run_web_server():
    """Запуск простого веб-сервера для Render"""
    app = web.Application()
    app.router.add_get('/', handle_health)
    app.router.add_get('/health', handle_health)
    
    port = int(os.environ.get('PORT', 10000))
    print(f"🌐 Заглушка веб-сервера запущена на порту {port}")
    
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    print(f"✅ Заглушка порта {port} активна (бот работает в фоне)")

async def main():
    """Запуск бота и веб-сервера"""
    print("🚀 Бот BloomStyle запускается...")
    
    # Запускаем веб-сервер (заглушку) параллельно с ботом
    asyncio.create_task(run_web_server())
    
    # Запускаем бота
    print("🤖 Бот начинает polling...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())