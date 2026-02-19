from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ContentType
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from keyboards import main_menu, skin_type_menu, budget_menu
from texts import DISCLAIMER, WELCOME
from database import set_user_city, get_user_city, set_user_skin_type, set_user_budget, init_user_stats
from weather_api import get_city_by_coords

router = Router()

# ==================== СОСТОЯНИЯ ДЛЯ ОНБОРДИНГА ====================

class Onboarding(StatesGroup):
    """Состояния для настройки профиля"""
    waiting_skin_type = State()
    waiting_budget = State()

# ==================== СТАРТ И ГЕОЛОКАЦИЯ ====================

@router.message(CommandStart())
async def cmd_start(message: Message):
    """Первый запуск — запрос геолокации"""
    
    # Проверяем, есть ли уже город у пользователя
    user_id = message.from_user.id
    existing_city = get_user_city(user_id)
    
    if existing_city:
        # Если город уже есть — показываем меню
        await message.answer(
            f"🌸 *С возвращением в BloomStyle!*\n\n"
            f"📍 Ваш город: {existing_city}\n"
            f"👇 Выберите раздел:",
            reply_markup=main_menu(),
            parse_mode="Markdown"
        )
        return
    
    # Если города нет — просим геолокацию
    location_kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📍 Отправить геолокацию", request_location=True)]
        ],
        resize_keyboard=True,
        input_field_placeholder="Нажмите кнопку ниже 👇"
    )
    
    await message.answer(
        "🌸 *Добро пожаловать в BloomStyle!*\n\n"
        "Я ваш персональный бьюти-гид с климатическим интеллектом.\n\n"
        "🌍 *Для начала мне нужно узнать ваш город.*\n"
        "Это нужно, чтобы подбирать уход под погоду в вашем регионе.\n\n"
        "👇 *Нажмите кнопку ниже и отправьте геолокацию*",
        reply_markup=location_kb,
        parse_mode="Markdown"
    )

@router.message(F.location)
async def handle_location(message: Message, state: FSMContext):
    """Обработка полученной геолокации"""
    
    lat = message.location.latitude
    lon = message.location.longitude
    user_id = message.from_user.id
    
    # Получаем город по координатам
    city = get_city_by_coords(lat, lon)
    
    # Сохраняем город в базу
    set_user_city(user_id, city)
    
    # Инициализируем статистику
    init_user_stats(user_id)
    
    await message.answer(
        f"✅ *Отлично! Ваш город: {city}*\n\n"
        f"📝 *Теперь давайте настроим ваш профиль.*\n\n"
        f"👇 *Выберите ваш тип кожи:*",
        reply_markup=skin_type_menu(),
        parse_mode="Markdown"
    )
    
    # Переходим к следующему шагу
    await state.set_state(Onboarding.waiting_skin_type)

# ==================== ШАГ 1: ТИП КОЖИ ====================

@router.message(Onboarding.waiting_skin_type)
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
        
        await message.answer(
            f"✅ *Тип кожи сохранён:* {skin_text}\n\n"
            f"💰 *Теперь выберите ваш бюджет:*\n\n"
            f"• 💸 Бюджетный — до 1000₽ за средство\n"
            f"• 💳 Средний — 1000-2500₽ за средство\n"
            f"• 💎 Премиум — от 2500₽ за средство",
            reply_markup=budget_menu(),
            parse_mode="Markdown"
        )
        
        # Переходим к выбору бюджета
        await state.set_state(Onboarding.waiting_budget)
    else:
        await message.answer(
            "❌ Пожалуйста, выберите тип кожи из меню ниже:",
            reply_markup=skin_type_menu(),
            parse_mode="Markdown"
        )

# ==================== ШАГ 2: БЮДЖЕТ ====================

@router.message(Onboarding.waiting_budget)
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
        
        # Завершаем онбординг
        await state.clear()
        
        await message.answer(
            f"✅ *Профиль успешно настроен!*\n\n"
            f"📍 Город: {get_user_city(user_id)}\n"
            f"🧬 Тип кожи: {skin_text_from_code(get_user_skin_type(user_id))}\n"
            f"💰 Бюджет: {budget_text}\n\n"
            f"👇 *Теперь вы можете пользоваться ботом!*",
            reply_markup=main_menu(),
            parse_mode="Markdown"
        )
        
        # Отправляем дисклеймер
        await message.answer(
            DISCLAIMER,
            parse_mode="Markdown"
        )
    else:
        await message.answer(
            "❌ Пожалуйста, выберите бюджет из меню ниже:",
            reply_markup=budget_menu(),
            parse_mode="Markdown"
        )

# ==================== ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ====================

def get_user_skin_type(user_id):
    """Получить тип кожи пользователя (заглушка)"""
    from database import get_user_skin_type
    return get_user_skin_type(user_id)

def skin_text_from_code(skin_code):
    """Преобразовать код типа кожи в текст"""
    skin_map = {
        "dry": "Сухая",
        "oily": "Жирная",
        "combination": "Комбинированная",
        "normal": "Нормальная",
        "sensitive": "Чувствительная"
    }
    return skin_map.get(skin_code, "Комбинированная")

# ==================== ДРУГИЕ КОМАНДЫ ====================

@router.message(Command('menu'))
async def cmd_menu(message: Message):
    """Команда меню"""
    await message.answer(
        "🌸 *Главное меню*",
        reply_markup=main_menu(),
        parse_mode="Markdown"
    )

@router.message(Command('help'))
async def cmd_help(message: Message):
    """Помощь"""
    from texts import HELP
    await message.answer(HELP, parse_mode="Markdown")

@router.message(F.text == "🔙 В главное меню")
async def back_to_main(message: Message):
    """Возврат в главное меню"""
    await message.answer(
        "🌸 *Главное меню*",
        reply_markup=main_menu(),
        parse_mode="Markdown"
    )