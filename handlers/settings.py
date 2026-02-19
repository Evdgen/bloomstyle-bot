from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ContentType
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from datetime import datetime

from keyboards import settings_menu, main_menu, budget_menu, skin_type_menu
from texts import DISCLAIMER, SAFETY_TIPS, HELP
from database import (
    get_full_profile, 
    set_user_budget, 
    set_user_skin_type, 
    set_user_city,
    get_user_city, 
    init_user_stats
)
from premium import is_premium, activate_premium, get_premium_expiry, PREMIUM_PRICES
from weather_api import get_city_by_coords
from .payments import PREMIUM_STARS

router = Router()

# ==================== СОСТОЯНИЯ ДЛЯ НАСТРОЙКИ ПРОФИЛЯ ====================

class ProfileSetup(StatesGroup):
    """Состояния для настройки профиля"""
    waiting_skin_type = State()
    waiting_budget = State()
    waiting_city = State()

# ==================== ГЛАВНОЕ МЕНЮ НАСТРОЕК ====================

@router.message(F.text == "⚙️ НАСТРОЙКИ и Premium")
async def settings_main(message: Message):
    """Меню настроек"""
    await message.answer(
        "⚙️ *Настройки и Premium*\n\nВыберите раздел:",
        reply_markup=settings_menu(),
        parse_mode="Markdown"
    )

# ==================== ПРОФИЛЬ ПОЛЬЗОВАТЕЛЯ ====================

@router.message(F.text == "👤 Мой профиль")
async def settings_profile(message: Message):
    """Полный профиль пользователя"""
    user_id = message.from_user.id
    init_user_stats(user_id)
    profile = get_full_profile(user_id)
    
    premium_status = is_premium(user_id)
    if premium_status:
        expiry = get_premium_expiry(user_id)
        days_left = (expiry - datetime.now()).days if expiry else 0
        premium_text = f"✅ Premium активен • осталось {days_left} дн."
    else:
        premium_text = "❌ Premium не активен"
    
    text = f"""
👤 *ВАШ ПРОФИЛЬ*

📍 **Город:** {profile['city']}
🧬 **Тип кожи:** {profile['skin_type']}
💰 **Бюджет:** {profile['budget']}
🎨 **Цветотип:** {profile['colortype']}
📐 **Форма лица:** {profile['face_shape']}
🌟 **Знак зодиака:** {profile['zodiac']}

💎 **Premium:** {premium_text}

📊 *СТАТИСТИКА:*
• Пользуется BloomStyle: {profile['days_active']} дн.
• Сохранённых рутин: {profile['routines_saved']}
• Экономия на мини-версиях: {profile['money_saved']}₽

🔄 *Команды для изменения:*
• /set_skin — изменить тип кожи
• /set_budget — изменить бюджет
• /set_city — изменить город
• /premium — информация о Premium
"""
    await message.answer(text, parse_mode="Markdown")

# ==================== ИЗМЕНЕНИЕ ТИПА КОЖИ ====================

@router.message(Command("set_skin"))
@router.message(F.text == "🧬 Изменить тип кожи")
async def change_skin_type(message: Message, state: FSMContext):
    """Начать изменение типа кожи"""
    await state.set_state(ProfileSetup.waiting_skin_type)
    await message.answer(
        "🧬 *Выберите ваш тип кожи:*",
        reply_markup=skin_type_menu(),
        parse_mode="Markdown"
    )

@router.message(ProfileSetup.waiting_skin_type)
async def process_skin_type(message: Message, state: FSMContext):
    """Обработка выбора типа кожи"""
    user_id = message.from_user.id
    skin_text = message.text
    
    skin_map = {
        "💧 Сухая": "dry",
        "🔥 Жирная": "oily",
        "🌓 Комбинированная": "combination",
        "⚖️ Нормальная": "normal",
        "🌡️ Чувствительная": "sensitive"
    }
    
    if skin_text in skin_map:
        skin_type = skin_map[skin_text]
        set_user_skin_type(user_id, skin_type)
        await state.clear()
        await message.answer(
            f"✅ *Тип кожи изменён на:* {skin_text}",
            reply_markup=settings_menu(),
            parse_mode="Markdown"
        )
    elif skin_text == "🔙 В главное меню":
        await state.clear()
        await message.answer(
            "🌸 *Главное меню*",
            reply_markup=main_menu(),
            parse_mode="Markdown"
        )
    else:
        await message.answer(
            "❌ Пожалуйста, выберите тип кожи из меню ниже:",
            reply_markup=skin_type_menu(),
            parse_mode="Markdown"
        )

# ==================== ИЗМЕНЕНИЕ БЮДЖЕТА ====================

@router.message(Command("set_budget"))
@router.message(F.text == "💰 Изменить бюджет")
async def change_budget(message: Message, state: FSMContext):
    """Начать изменение бюджета"""
    await state.set_state(ProfileSetup.waiting_budget)
    await message.answer(
        "💰 *Выберите ваш бюджет:*\n\n"
        "• 💸 Бюджетный — до 1000₽ за средство\n"
        "• 💳 Средний — 1000-2500₽ за средство\n"
        "• 💎 Премиум — от 2500₽ за средство",
        reply_markup=budget_menu(),
        parse_mode="Markdown"
    )

@router.message(ProfileSetup.waiting_budget)
async def process_budget(message: Message, state: FSMContext):
    """Обработка выбора бюджета"""
    user_id = message.from_user.id
    budget_text = message.text
    
    budget_map = {
        "💸 Бюджетный (до 1000₽)": "budget",
        "💳 Средний (1000-2500₽)": "medium",
        "💎 Премиум (2500₽+)": "premium"
    }
    
    if budget_text in budget_map:
        budget = budget_map[budget_text]
        set_user_budget(user_id, budget)
        await state.clear()
        await message.answer(
            f"✅ *Бюджет изменён на:* {budget_text}",
            reply_markup=settings_menu(),
            parse_mode="Markdown"
        )
    elif budget_text == "🔙 В главное меню":
        await state.clear()
        await message.answer(
            "🌸 *Главное меню*",
            reply_markup=main_menu(),
            parse_mode="Markdown"
        )
    else:
        await message.answer(
            "❌ Пожалуйста, выберите бюджет из меню ниже:",
            reply_markup=budget_menu(),
            parse_mode="Markdown"
        )

# ==================== ИЗМЕНЕНИЕ ГОРОДА ====================

@router.message(Command("set_city"))
@router.message(F.text == "📍 Изменить город")
async def change_city(message: Message, state: FSMContext):
    """Начать изменение города"""
    location_kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📍 Отправить геолокацию", request_location=True)],
            [KeyboardButton(text="🔙 В настройки")]
        ],
        resize_keyboard=True,
        input_field_placeholder="Отправьте геолокацию 👇"
    )
    
    await state.set_state(ProfileSetup.waiting_city)
    await message.answer(
        "📍 *Изменить город*\n\n"
        "Отправьте вашу геолокацию, чтобы я определил город.\n"
        "Или нажмите кнопку ниже 👇",
        reply_markup=location_kb,
        parse_mode="Markdown"
    )

@router.message(ProfileSetup.waiting_city, F.location)
async def process_city_location(message: Message, state: FSMContext):
    """Обработка новой геолокации"""
    user_id = message.from_user.id
    lat = message.location.latitude
    lon = message.location.longitude
    
    city = get_city_by_coords(lat, lon)
    set_user_city(user_id, city)
    
    await state.clear()
    await message.answer(
        f"✅ *Город успешно изменён!*\n\n📍 Теперь ваш город: {city}",
        reply_markup=settings_menu(),
        parse_mode="Markdown"
    )

@router.message(ProfileSetup.waiting_city, F.text == "🔙 В настройки")
async def cancel_city_change(message: Message, state: FSMContext):
    """Отмена изменения города"""
    await state.clear()
    await message.answer(
        "⚙️ *Настройки*",
        reply_markup=settings_menu(),
        parse_mode="Markdown"
    )

# ==================== PREMIUM (ИСПРАВЛЕННАЯ ВЕРСИЯ) ====================

@router.message(F.text == "💎 BloomStyle Premium")
async def settings_premium(message: Message):
    """Информация о Premium (без Markdown форматирования)"""
    user_id = message.from_user.id
    premium_status = is_premium(user_id)
    
    if premium_status:
        expiry = get_premium_expiry(user_id)
        days_left = (expiry - datetime.now()).days if expiry else 0
        
        text = f"""
💎 BloomStyle Premium — АКТИВЕН

👑 Статус: ✅ Premium подписка
📅 Действует до: {expiry.strftime('%d.%m.%Y') if expiry else 'бессрочно'}
⏳ Осталось дней: {days_left}

✨ ДОСТУПНЫЕ ФУНКЦИИ:
✅ 📊 Климатический дневник
✅ 🧪 Виртуальная косметичка
✅ 📸 AR-примерка макияжа
✅ 📈 Расширенная статистика
✅ 🎨 Персональные образы

💎 Спасибо, что вы с нами!
"""
    else:
        savings = PREMIUM_STARS["month"] * 12 - PREMIUM_STARS["year"]
        text = f"""
💎 BloomStyle Premium

🌟 ПРЕИМУЩЕСТВА:

📊 Климатический дневник — полная история реакций
🧪 Виртуальная косметичка — до 100 средств
📸 AR-примерка макияжа — 50 примерок в день
📈 Расширенная статистика — экономия и прогресс

💰 СТОИМОСТЬ:
• ⭐ {PREMIUM_STARS['month']} Stars/месяц
• ⭐ {PREMIUM_STARS['year']} Stars/год (экономия {savings}⭐)

🎁 Пробный период: 2 дня бесплатно!

/activate_trial — активировать 2 дня бесплатно
/premium — подробнее
"""
    await message.answer(text)

# ==================== ПОМОЩЬ И БЕЗОПАСНОСТЬ ====================

@router.message(F.text == "❓ Помощь и безопасность")
async def settings_help(message: Message):
    """Помощь и дисклеймеры"""
    await message.answer(HELP, parse_mode="Markdown")
    await message.answer(DISCLAIMER, parse_mode="Markdown")
    await message.answer(SAFETY_TIPS, parse_mode="Markdown")

# ==================== ВОЗВРАТЫ ====================

@router.message(F.text == "🔙 В главное меню")
async def back_to_main(message: Message):
    """Возврат в главное меню"""
    await message.answer(
        "🌸 *Главное меню*",
        reply_markup=main_menu(),
        parse_mode="Markdown"
    )

@router.message(F.text == "🔙 В настройки")
async def back_to_settings(message: Message):
    """Возврат в меню настроек"""
    await message.answer(
        "⚙️ *Настройки и Premium*",
        reply_markup=settings_menu(),
        parse_mode="Markdown"
    )