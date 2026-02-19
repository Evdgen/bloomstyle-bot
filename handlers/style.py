from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from keyboards import style_menu, makeup_scene_menu
from style_engine import get_look
from colortype_test import (
    start_colortype_test, 
    process_colortype_answer, 
    get_colortype_description,
    COLORTYPE_RESULTS
)
from face_shape_test import (
    start_face_shape_test,
    process_face_shape_answer,
    get_face_shape_description
)
from skin_type_test import (
    start_skin_type_test,
    process_skin_type_answer,
    get_skin_type_description,
    SKIN_TYPE_RESULTS
)
from database import (
    set_user_colortype, 
    set_user_face_shape, 
    set_user_skin_type,
    get_user_colortype, 
    get_user_face_shape,
    get_user_skin_type
)

router = Router()

# ==================== СОСТОЯНИЯ ДЛЯ ТЕСТОВ ====================

class ColortypeTest(StatesGroup):
    """Состояния для теста цветотипа"""
    waiting_answer = State()

class FaceShapeTest(StatesGroup):
    """Состояния для теста формы лица"""
    waiting_answer = State()

class SkinTypeTest(StatesGroup):
    """Состояния для теста типа кожи"""
    waiting_answer = State()

# ==================== ГЛАВНОЕ МЕНЮ STYLE ====================

@router.message(F.text == "💄 STYLE — Макияж и стиль")
async def style_main(message: Message):
    """Меню раздела STYLE"""
    await message.answer(
        "💄 *STYLE: Макияж и стиль*\n\n"
        "Выберите раздел:",
        reply_markup=style_menu(),
        parse_mode="Markdown"
    )

# ==================== ТЕСТ НА ТИП КОЖИ ====================

@router.message(F.text == "🧬 Определить тип кожи")
async def start_skin_test(message: Message, state: FSMContext):
    """Начать тест на определение типа кожи"""
    user_id = message.from_user.id
    
    question, options = start_skin_type_test(user_id)
    
    from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
    
    rows = []
    current_row = []
    for i, opt in enumerate(options):
        current_row.append(KeyboardButton(text=opt))
        if len(current_row) == 2 or i == len(options) - 1:
            rows.append(current_row)
            current_row = []
    
    kb = ReplyKeyboardMarkup(
        keyboard=rows + [[KeyboardButton(text="❌ Отменить тест")]],
        resize_keyboard=True
    )
    
    await state.set_state(SkinTypeTest.waiting_answer)
    await message.answer(
        f"🧬 *ТЕСТ НА ТИП КОЖИ*\n\n{question}",
        reply_markup=kb,
        parse_mode="Markdown"
    )

@router.message(SkinTypeTest.waiting_answer)
async def process_skin_test(message: Message, state: FSMContext):
    """Обработка ответов на тест типа кожи"""
    user_id = message.from_user.id
    answer = message.text
    
    if answer == "❌ Отменить тест":
        await state.clear()
        await message.answer(
            "❌ Тест отменен. Вы можете начать заново в любое время.",
            reply_markup=style_menu()
        )
        return
    
    result, next_options = process_skin_type_answer(user_id, answer)
    
    if result and not next_options:
        await state.clear()
        
        skin_key = result["key"]
        set_user_skin_type(user_id, skin_key)
        
        await message.answer(
            f"✅ *ТЕСТ ЗАВЕРШЕН!*\n\n{get_skin_type_description(skin_key)}",
            reply_markup=style_menu(),
            parse_mode="Markdown"
        )
    else:
        from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
        
        rows = []
        current_row = []
        for i, opt in enumerate(next_options):
            current_row.append(KeyboardButton(text=opt))
            if len(current_row) == 2 or i == len(next_options) - 1:
                rows.append(current_row)
                current_row = []
        
        kb = ReplyKeyboardMarkup(
            keyboard=rows + [[KeyboardButton(text="❌ Отменить тест")]],
            resize_keyboard=True
        )
        
        await message.answer(result, reply_markup=kb, parse_mode="Markdown")

# ==================== ТЕСТ НА ЦВЕТОТИП ====================

@router.message(F.text == "🎨 Определить цветотип")
async def start_colortype(message: Message, state: FSMContext):
    """Начать тест на определение цветотипа"""
    user_id = message.from_user.id
    
    question, options = start_colortype_test(user_id)
    
    from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
    
    rows = []
    current_row = []
    for i, opt in enumerate(options):
        current_row.append(KeyboardButton(text=opt))
        if len(current_row) == 2 or i == len(options) - 1:
            rows.append(current_row)
            current_row = []
    
    kb = ReplyKeyboardMarkup(
        keyboard=rows + [[KeyboardButton(text="❌ Отменить тест")]],
        resize_keyboard=True
    )
    
    await state.set_state(ColortypeTest.waiting_answer)
    await message.answer(
        f"🎨 *ТЕСТ НА ЦВЕТОТИП*\n\n{question}",
        reply_markup=kb,
        parse_mode="Markdown"
    )

@router.message(ColortypeTest.waiting_answer)
async def process_colortype(message: Message, state: FSMContext):
    """Обработка ответов на тест цветотипа"""
    user_id = message.from_user.id
    answer = message.text
    
    if answer == "❌ Отменить тест":
        await state.clear()
        await message.answer(
            "❌ Тест отменен. Вы можете начать заново в любое время.",
            reply_markup=style_menu()
        )
        return
    
    result, next_options = process_colortype_answer(user_id, answer)
    
    if result and not next_options:
        await state.clear()
        
        colortype_key = None
        for key, value in COLORTYPE_RESULTS.items():
            if value["name"] == result["name"]:
                colortype_key = key
                break
        
        if colortype_key:
            set_user_colortype(user_id, colortype_key)
        
        await message.answer(
            f"✅ *ТЕСТ ЗАВЕРШЕН!*\n\n{get_colortype_description(colortype_key)}",
            reply_markup=style_menu(),
            parse_mode="Markdown"
        )
    else:
        from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
        
        rows = []
        current_row = []
        for i, opt in enumerate(next_options):
            current_row.append(KeyboardButton(text=opt))
            if len(current_row) == 2 or i == len(next_options) - 1:
                rows.append(current_row)
                current_row = []
        
        kb = ReplyKeyboardMarkup(
            keyboard=rows + [[KeyboardButton(text="❌ Отменить тест")]],
            resize_keyboard=True
        )
        
        await message.answer(result, reply_markup=kb, parse_mode="Markdown")

# ==================== ТЕСТ НА ФОРМУ ЛИЦА ====================

@router.message(F.text == "📐 Определить форму лица")
async def start_face_shape(message: Message, state: FSMContext):
    """Начать тест на определение формы лица"""
    user_id = message.from_user.id
    
    question, options = start_face_shape_test(user_id)
    
    from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
    
    rows = []
    current_row = []
    for i, opt in enumerate(options):
        current_row.append(KeyboardButton(text=opt))
        if len(current_row) == 2 or i == len(options) - 1:
            rows.append(current_row)
            current_row = []
    
    kb = ReplyKeyboardMarkup(
        keyboard=rows + [[KeyboardButton(text="❌ Отменить тест")]],
        resize_keyboard=True
    )
    
    await state.set_state(FaceShapeTest.waiting_answer)
    await message.answer(
        f"📐 *ТЕСТ НА ФОРМУ ЛИЦА*\n\n{question}",
        reply_markup=kb,
        parse_mode="Markdown"
    )

@router.message(FaceShapeTest.waiting_answer)
async def process_face_shape(message: Message, state: FSMContext):
    """Обработка ответов на тест формы лица с ФИНАЛЬНЫМ ВЫВОДОМ"""
    user_id = message.from_user.id
    answer = message.text
    
    if answer == "❌ Отменить тест":
        await state.clear()
        await message.answer(
            "❌ Тест отменен. Вы можете начать заново в любое время.",
            reply_markup=style_menu()
        )
        return
    
    result, next_options = process_face_shape_answer(user_id, answer)
    
    if result and not next_options:
        await state.clear()
        
        shape_key = result["key"]
        set_user_face_shape(user_id, shape_key)
        
        # ПОЛНЫЙ ФИНАЛЬНЫЙ ВЫВОД
        await message.answer(
            f"✅ *ТЕСТ ЗАВЕРШЕН!*\n\n{get_face_shape_description(shape_key)}",
            reply_markup=style_menu(),
            parse_mode="Markdown"
        )
    else:
        from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
        
        rows = []
        current_row = []
        for i, opt in enumerate(next_options):
            current_row.append(KeyboardButton(text=opt))
            if len(current_row) == 2 or i == len(next_options) - 1:
                rows.append(current_row)
                current_row = []
        
        kb = ReplyKeyboardMarkup(
            keyboard=rows + [[KeyboardButton(text="❌ Отменить тест")]],
            resize_keyboard=True
        )
        
        await message.answer(result, reply_markup=kb, parse_mode="Markdown")

# ==================== МАКИЯЖ НА СЛУЧАЙ ====================

@router.message(F.text == "🎭 Макияж на случай")
async def style_makeup(message: Message):
    """Меню сценариев макияжа"""
    await message.answer(
        "🎭 *Макияж на случай*\n\nВыберите сценарий:",
        reply_markup=makeup_scene_menu(),
        parse_mode="Markdown"
    )

@router.message(F.text == "🏢 Офисный день")
async def makeup_office(message: Message):
    import random
    
    user_id = message.from_user.id
    colortype = get_user_colortype(user_id)
    
    if colortype:
        ct = COLORTYPE_RESULTS.get(colortype, COLORTYPE_RESULTS["summer"])
        lipstick = ct["lipstick"].split(",")[0].strip()
        foundation = ct["foundation"]
        eyes = ct["eyes"].split(",")[0].strip()
    else:
        lipsticks = ["нюд", "пыльная роза", "розово-бежевый"]
        foundations = ["розовато-бежевый подтон", "золотисто-бежевый подтон"]
        eyes_colors = ["серые тени", "коричневые тени", "бежевые тени"]
        
        lipstick = random.choice(lipsticks)
        foundation = random.choice(foundations)
        eyes = random.choice(eyes_colors)
    
    finishes = ["натуральный", "сатиновый", "матовый"]
    finish = random.choice(finishes)
    
    text = f"""
🏢 *ОФИСНЫЙ МАКИЯЖ*

⏱️ *Время:* 10-12 минут

💄 *ОБРАЗ:*
• Тональная основа: {foundation}, {finish} финиш
• Брови: естественная форма, прозрачный гель
• Тени: {eyes}, легкая растушевка
• Тушь: черная или коричневая, 1 слой
• Помада: {lipstick}, тинт или бальзам
• Румяна: персиковые или розовые, легкое сияние

🛒 *НЕОБХОДИМЫЙ МИНИМУМ:*
• BB-крем SPF 25 — 890₽
• Тушь Maybelline Lash Sensational — 650₽
• Тинт Rom&nd — 490₽

💡 *СОВЕТ:* Для стойкости используйте праймер для век
"""
    await message.answer(text, parse_mode="Markdown")

@router.message(F.text == "💕 Свидание/вечеринка")
async def makeup_date(message: Message):
    import random
    
    user_id = message.from_user.id
    colortype = get_user_colortype(user_id)
    
    accents = ["губы", "глаза", "сияние кожи", "стрелки"]
    accent = random.choice(accents)
    
    if colortype == "winter":
        lipstick = "фуксия или холодный красный"
    elif colortype == "summer":
        lipstick = "ягодный или сливовый"
    elif colortype == "spring":
        lipstick = "коралловый или персиковый"
    elif colortype == "autumn":
        lipstick = "терракотовый или кирпичный"
    else:
        lipstick = random.choice(["красный", "винный", "сливовый", "коралловый"])
    
    text = f"""
💕 *МАКИЯЖ ДЛЯ СВИДАНИЯ*

⏱️ *Время:* 15-20 минут

🎯 *АКЦЕНТ НА:* {accent.upper()}

💄 *ОБРАЗ:*
• База: праймер + сияющая тональная основа
• Акцент: {lipstick} помада
• Глаза: легкая дымка, коричневая подводка
• Сияние: хайлайтер на скулы

🛒 *НЕОБХОДИМЫЙ МИНИМУМ:*
• Сияющая тональная основа — 790₽ (мини)
• Помада MAC — 990₽ (мини)
• Хайлайтер — 590₽ (мини)

💡 *СОВЕТ:* Нанесите помаду в 2 слоя для стойкости
"""
    await message.answer(text, parse_mode="Markdown")

@router.message(F.text == "✈️ Путешествие/дорога")
async def makeup_travel(message: Message):
    text = """
✈️ *МАКИЯЖ ДЛЯ ПУТЕШЕСТВИЙ*

⏱️ *Время:* 5-7 минут

🧳 *ЧЕМОДАНЧИК:*
• BB-крем — тонирует + увлажняет
• Водостойкая тушь — не потечет
• Термальная вода — увлажнение в полете
• Тинт 2в1 — для губ и щек

🛒 *МИНИ-НАБОР:*
• BB-крем SPF 30 — 590₽ (30 мл)
• Тушь Maybelline Waterproof — 650₽
• Тинт Rom&nd — 490₽
• Термальная вода Avene — 290₽ (50 мл)

💡 *СОВЕТ:* Только мини-версии в ручную кладь!
"""
    await message.answer(text, parse_mode="Markdown")

@router.message(F.text == "🌧️ Плохая погода")
async def makeup_bad_weather(message: Message):
    text = """
🌧️ *МАКИЯЖ ДЛЯ ПЛОХОЙ ПОГОДЫ*

⚠️ *Ветер, влажность, осадки*

💄 *СТОЙКИЕ ФОРМУЛЫ:*
1. **Праймер** — база для стойкости
2. **Тон** — водостойкий или матирующий
3. **Тушь** — только waterproof!
4. **Помада** — тинт или жидкая матовая
5. **Фиксатор** — спрей для макияжа

🛒 *НАБОР:*
• Праймер Smashbox — 490₽ (мини)
• Тушь Maybelline Waterproof — 650₽
• Тинт Rom&nd — 490₽
• Фиксирующий спрей MAC — 590₽ (мини)

💡 *СОВЕТ:* Матирующие салфетки в сумку
"""
    await message.answer(text, parse_mode="Markdown")

# ==================== МОИ ОБРАЗЫ ====================

@router.message(F.text == "👗 Мои образы")
async def style_looks(message: Message):
    user_id = message.from_user.id
    colortype = get_user_colortype(user_id)
    face_shape = get_user_face_shape(user_id)
    skin_type = get_user_skin_type(user_id)
    
    skin_text = SKIN_TYPE_RESULTS.get(skin_type, {}).get("name", "Не определён")
    colortype_text = COLORTYPE_RESULTS.get(colortype, {}).get("name", "Не определён")
    face_text = get_face_shape_description(face_shape).split("\n")[0] if face_shape else "Не определена"
    
    text = f"""
👗 *МОИ СОХРАНЁННЫЕ ОБРАЗЫ*

1️⃣ 👔 **«ИДЕАЛЬНЫЙ ОФИС»**
   • Макияж: матовая кожа + тонкие стрелки
   • Одежда: белая блузка + чёрные брюки
   • Время: 12 минут

2️⃣ 💕 **«РОМАНТИЧЕСКИЙ ВЕЧЕР»**
   • Макияж: сияющая кожа + красные губы
   • Одежда: чёрное платье
   • Время: 18 минут

3️⃣ 🌿 **«ВЫХОДНОЙ CASUAL»**
   • Макияж: BB-крем + тушь
   • Одежда: джинсы + футболка
   • Время: 7 минут

📊 *ПЕРСОНАЛИЗАЦИЯ:*
✅ Тип кожи: {skin_text}
{'✅ Цветотип: ' + colortype_text if colortype else '❌ Цветотип не определён'}
{'✅ Форма лица: ' + face_text if face_shape else '❌ Форма лица не определена'}

✨ *Пройдите тесты для персональных рекомендаций!*
"""
    await message.answer(text, parse_mode="Markdown")

# ==================== ВОЗВРАТЫ ====================

@router.message(F.text == "🔙 В меню STYLE")
async def back_to_style(message: Message):
    await message.answer(
        "💄 *STYLE: Макияж и стиль*",
        reply_markup=style_menu(),
        parse_mode="Markdown"
    )