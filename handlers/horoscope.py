from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime

from database import set_user_zodiac, get_user_zodiac
from keyboards import style_menu

router = Router()

# Словарь с гороскопами красоты
BEAUTY_HOROSCOPE = {
    "овен": {
        "name": "♈ Овен",
        "today": "🔥 Сегодня вашей коже нужна энергия! Используйте витамин С утром для сияния.",
        "ingredient": "Витамин С",
        "ritual": "Массаж лица кубиком льда",
        "makeup": "Яркие губы"
    },
    "телец": {
        "name": "♉ Телец",
        "today": "🌿 Время плотных кремов! Ваша кожа жаждет питания.",
        "ingredient": "Масло ши",
        "ritual": "Питательная маска",
        "makeup": "Натуральные оттенки"
    },
    "близнецы": {
        "name": "♊ Близнецы",
        "today": "🦋 Экспериментируйте! Идеальный день для новых средств.",
        "ingredient": "Ниацинамид",
        "ritual": "Мультимаскинг",
        "makeup": "Цветная тушь"
    },
    "рак": {
        "name": "♋ Рак",
        "today": "🌙 Забота и нежность. Вашей коже нужно успокоение.",
        "ingredient": "Пантенол",
        "ritual": "Успокаивающая маска",
        "makeup": "Нежный розовый"
    },
    "лев": {
        "name": "♌ Лев",
        "today": "👑 Сияние и роскошь! Хайлайтер — ваш лучший друг.",
        "ingredient": "Коллаген",
        "ritual": "Патчи под глаза",
        "makeup": "Сияющая кожа"
    },
    "дева": {
        "name": "♍ Дева",
        "today": "✨ Чистота и порядок. Двойное очищение обязательно!",
        "ingredient": "Салициловая кислота",
        "ritual": "Глубокая очищающая маска",
        "makeup": "Идеально ровный тон"
    },
    "весы": {
        "name": "♎ Весы",
        "today": "⚖️ Баланс во всём. Ищите золотую середину.",
        "ingredient": "Гиалуроновая кислота",
        "ritual": "Тонизирование",
        "makeup": "Акцент на глаза"
    },
    "скорпион": {
        "name": "♏ Скорпион",
        "today": "🕷️ Глубокое воздействие. Ретинол и кислоты — ваш выбор.",
        "ingredient": "Ретинол",
        "ritual": "Обновление с кислотами",
        "makeup": "Дымчатые глаза"
    },
    "стрелец": {
        "name": "♐ Стрелец",
        "today": "🏹 Приключения! Экспериментируйте с текстурами.",
        "ingredient": "Энзимы",
        "ritual": "Двойное очищение",
        "makeup": "Яркие оттенки"
    },
    "козерог": {
        "name": "♑ Козерог",
        "today": "🏔️ Дисциплина. Многоступенчатый уход — ваш конёк.",
        "ingredient": "Пептиды",
        "ritual": "Полная 10-шаговая рутина",
        "makeup": "Чёткие линии"
    },
    "водолей": {
        "name": "♒ Водолей",
        "today": "💧 Инновации! Гидрогелевые патчи — то что нужно.",
        "ingredient": "Пробиотики",
        "ritual": "Гидрогелевые патчи",
        "makeup": "Необычные цвета"
    },
    "рыбы": {
        "name": "♓ Рыбы",
        "today": "🌊 Мечтательность. Термальная вода в течение дня.",
        "ingredient": "Морские водоросли",
        "ritual": "Термальная вода",
        "makeup": "Акварельные оттенки"
    }
}

@router.message(F.text == "🌟 Гороскоп красоты")
async def beauty_horoscope_menu(message: Message):
    """Меню гороскопа красоты"""
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✨ Гороскоп на сегодня", callback_data="horoscope_today"),
            InlineKeyboardButton(text="♈ Выбрать знак", callback_data="horoscope_choose")
        ],
        [
            InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_style")
        ]
    ])
    
    await message.answer(
        "🌟 *Гороскоп красоты*\n\n"
        "Узнайте, что звёзды говорят о вашей коже сегодня!\n\n"
        "✨ Астрологи рекомендуют уход по знаку зодиака",
        reply_markup=kb,
        parse_mode="Markdown"
    )

@router.callback_query(F.data == "horoscope_choose")
async def choose_zodiac(callback: CallbackQuery):
    """Выбор знака зодиака"""
    zodiacs = [
        ["♈ Овен", "♉ Телец", "♊ Близнецы"],
        ["♋ Рак", "♌ Лев", "♍ Дева"],
        ["♎ Весы", "♏ Скорпион", "♐ Стрелец"],
        ["♑ Козерог", "♒ Водолей", "♓ Рыбы"],
    ]
    
    keyboard = []
    for row in zodiacs:
        buttons = []
        for z in row:
            sign = z.split()[1].lower()
            buttons.append(InlineKeyboardButton(text=z, callback_data=f"zodiac_{sign}"))
        keyboard.append(buttons)
    
    keyboard.append([InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_horoscope")])
    
    kb = InlineKeyboardMarkup(inline_keyboard=keyboard)
    
    await callback.message.edit_text(
        "🌟 *Выберите ваш знак зодиака:*",
        reply_markup=kb,
        parse_mode="Markdown"
    )
    await callback.answer()

@router.callback_query(F.data.startswith("zodiac_"))
async def save_zodiac(callback: CallbackQuery):
    """Сохранение знака зодиака и показ гороскопа"""
    zodiac = callback.data.replace("zodiac_", "")
    user_id = callback.from_user.id
    
    # Сохраняем знак в базу
    set_user_zodiac(user_id, zodiac)
    
    # Показываем гороскоп
    await show_today_horoscope(callback.message, zodiac)
    await callback.answer()

async def show_today_horoscope(message, zodiac_key):
    """Показать гороскоп на сегодня"""
    zodiac = BEAUTY_HOROSCOPE.get(zodiac_key, BEAUTY_HOROSCOPE["овен"])
    
    text = f"""
🌟 *Гороскоп красоты на сегодня*

{zodiac['name']}

✨ *СОВЕТ ДНЯ:*
{zodiac['today']}

💎 *ЗВЕЗДНЫЙ ИНГРЕДИЕНТ:*
{zodiac['ingredient']}

🧖‍♀️ *РИТУАЛ КРАСОТЫ:*
{zodiac['ritual']}

💄 *МАКИЯЖ ДНЯ:*
{zodiac['makeup']}
"""
    
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_horoscope")]
    ])
    
    await message.edit_text(text, reply_markup=kb, parse_mode="Markdown")

@router.callback_query(F.data == "horoscope_today")
async def today_horoscope(callback: CallbackQuery):
    """Гороскоп для сохранённого знака"""
    user_id = callback.from_user.id
    zodiac = get_user_zodiac(user_id)
    
    if not zodiac:
        # Если знак не выбран
        await choose_zodiac(callback)
        return
    
    await show_today_horoscope(callback.message, zodiac)
    await callback.answer()

@router.callback_query(F.data == "back_to_horoscope")
async def back_to_horoscope(callback: CallbackQuery):
    """Назад в меню гороскопа"""
    await beauty_horoscope_menu(callback.message)
    await callback.answer()

@router.callback_query(F.data == "back_to_style")
async def back_to_style(callback: CallbackQuery):
    """Возврат в меню STYLE"""
    await callback.message.answer(
        "💄 *STYLE: Макияж и стиль*",
        reply_markup=style_menu(),
        parse_mode="Markdown"
    )
    await callback.answer()