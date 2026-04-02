import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

# Токен тестового бота
TOKEN = "8039333293:AAHUT_YoELjQL4BOJRLOtehEidJD49fhizw"

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("✅ Тестовый бот работает! Поздравляю!")

@dp.message()
async def echo(message: types.Message):
    await message.answer(f"Ты написал: {message.text}")

async def main():
    print("🚀 Тестовый бот запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
