from aiogram import Router, F
from aiogram.types import Message
from datetime import datetime

from keyboards import bloom_menu, product_search_menu, travel_menu
from weather_api import get_weather, get_weather_risks, get_morning_routine, get_evening_routine
from product_engine import get_products_by_problem, format_products
from texts import get_travel_tropics, get_travel_mountains, get_travel_city
from database import get_user_city

router = Router()

@router.message(F.text == "🌱 BLOOM — Уход")
async def bloom_main(message: Message):
    await message.answer(
        "🌱 *BLOOM: Уход за кожей*\n\nВыберите раздел:",
        reply_markup=bloom_menu(),
        parse_mode="Markdown"
    )

@router.message(F.text == "📅 Уход на сегодня")
async def bloom_today(message: Message):
    user_id = message.from_user.id
    city = get_user_city(user_id)
    
    if not city:
        await message.answer(
            "📍 *Город не определён*\n\n"
            "Нажмите /start и отправьте геолокацию.",
            parse_mode="Markdown"
        )
        return
    
    weather = get_weather(city)
    
    if not weather:
        await message.answer("⏳ Не удалось получить погоду. Попробуйте позже.")
        return
    
    risks = get_weather_risks(weather["humidity"], weather["wind_speed"])
    risk_text = "⚠️ *КЛЮЧЕВЫЕ РИСКИ:*\n" + "\n".join(risks)
    
    await message.answer(
        f"📍 *{weather['city']}*\n"
        f"🌡️ {weather['temp']}°C | 💧 {weather['humidity']}% | 🌬️ {weather['wind_speed']} м/с\n"
        f"📝 {weather['description']}",
        parse_mode="Markdown"
    )
    
    await message.answer(risk_text, parse_mode="Markdown")
    await message.answer(get_morning_routine(weather), parse_mode="Markdown")
    await message.answer(get_evening_routine(weather), parse_mode="Markdown")

@router.message(F.text == "📊 Климат-отчёт")  # ИЗМЕНЕНО НАЗВАНИЕ!
async def climate_report(message: Message):
    """Детальный отчёт о климате (БЕЗ анализа кожи)"""
    
    user_id = message.from_user.id
    city = get_user_city(user_id)
    
    if not city:
        await message.answer(
            "📍 *Город не определён*\n\n"
            "Нажмите /start и отправьте геолокацию.",
            parse_mode="Markdown"
        )
        return
    
    weather = get_weather(city)
    
    if not weather:
        await message.answer("⏳ Не удалось получить данные о погоде.")
        return
    
    risks = get_weather_risks(weather["humidity"], weather["wind_speed"])
    
    text = f"🌍 *КЛИМАТ-ОТЧЁТ: {weather['city']}*\n\n"
    text += f"📅 *Дата:* {datetime.now().strftime('%d.%m.%Y')}\n\n"
    text += f"🌡️ *Температура:* {weather['temp']}°C\n"
    text += f"💧 *Влажность:* {weather['humidity']}%\n"
    text += f"🌬️ *Ветер:* {weather['wind_speed']} м/с\n"
    text += f"📝 *Описание:* {weather['description']}\n\n"
    text += "⚠️ *ПОГОДНЫЕ РИСКИ:*\n" + "\n".join(risks) + "\n\n"
    text += "💡 *РЕКОМЕНДАЦИЯ ДНЯ:*\n"
    
    if weather["humidity"] < 40:
        text += "• Утром: гиалуроновая кислота на влажную кожу\n"
        text += "• Днём: термальная вода в спрее\n"
        text += "• Вечером: восстанавливающий крем с церамедами\n"
    elif weather["humidity"] > 70:
        text += "• Утром: лёгкий гель для умывания\n"
        text += "• Днём: матирующие салфетки\n"
        text += "• Вечером: гель-крем без масел\n"
    elif weather["wind_speed"] > 5:
        text += "• Утром: SPF 30+ (защита от ветра)\n"
        text += "• Днём: избегайте длительного пребывания на ветру\n"
        text += "• Вечером: пантенол или цика-крем\n"
    else:
        text += "• Сегодня кожа в безопасности\n"
        text += "• Поддерживайте обычную рутину\n"
        text += "• Не забывайте про SPF\n"
    
    await message.answer(text, parse_mode="Markdown")

@router.message(F.text == "🔍 Подобрать средство")
async def bloom_search(message: Message):
    await message.answer(
        "🔍 *Подбор средства*\n\nВыберите вашу проблему:",
        reply_markup=product_search_menu(),
        parse_mode="Markdown"
    )

@router.message(F.text == "💧 Сухость/шелушение")
async def products_dry(message: Message):
    user_id = message.from_user.id
    products = get_products_by_problem("Сухость/шелушение", user_id=user_id)
    await message.answer(
        format_products("Сухость/шелушение", products),
        parse_mode="Markdown"
    )

@router.message(F.text == "🔥 Жирный блеск/поры")
async def products_oily(message: Message):
    user_id = message.from_user.id
    products = get_products_by_problem("Жирный блеск/поры", user_id=user_id)
    await message.answer(
        format_products("Жирный блеск/поры", products),
        parse_mode="Markdown"
    )

@router.message(F.text == "🌡️ Чувствительность/покраснения")
async def products_sensitive(message: Message):
    user_id = message.from_user.id
    products = get_products_by_problem("Чувствительность/покраснения", user_id=user_id)
    await message.answer(
        format_products("Чувствительность/покраснения", products),
        parse_mode="Markdown"
    )

@router.message(F.text == "🧴 Увлажнение")
async def products_moisture(message: Message):
    user_id = message.from_user.id
    products = get_products_by_problem("Увлажнение", user_id=user_id)
    await message.answer(
        format_products("Увлажнение", products),
        parse_mode="Markdown"
    )

@router.message(F.text == "🛡️ SPF-защита")
async def products_spf(message: Message):
    user_id = message.from_user.id
    products = get_products_by_problem("SPF-защита", user_id=user_id)
    await message.answer(
        format_products("SPF-защита", products),
        parse_mode="Markdown"
    )

@router.message(F.text == "✈️ Уход в путешествиях")
async def bloom_travel(message: Message):
    await message.answer(
        "✈️ *Уход в путешествиях*\n\nВыберите направление:",
        reply_markup=travel_menu(),
        parse_mode="Markdown"
    )

@router.message(F.text == "🏖️ Тропики/пляж")
async def travel_tropics(message: Message):
    await message.answer(get_travel_tropics(), parse_mode="Markdown")

@router.message(F.text == "🏔️ Горы/холод")
async def travel_mountains(message: Message):
    await message.answer(get_travel_mountains(), parse_mode="Markdown")

@router.message(F.text == "🏙️ Городской тур")
async def travel_city(message: Message):
    await message.answer(get_travel_city(), parse_mode="Markdown")

@router.message(F.text == "🔙 В меню BLOOM")
async def back_to_bloom(message: Message):
    await message.answer(
        "🌱 *BLOOM: Уход за кожей*",
        reply_markup=bloom_menu(),
        parse_mode="Markdown"
    )