from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime, timedelta

router = Router()

# Хранилище привычек
habits_db = {}

# Список привычек
HABITS = [
    {"id": "water", "name": "💧 Выпил(а) 2л воды", "emoji": "💧", "points": 10},
    {"id": "spf", "name": "🧴 Нанес(ла) SPF", "emoji": "☀️", "points": 15},
    {"id": "clean", "name": "🧖 Умылся(ась) утром", "emoji": "🌅", "points": 5},
    {"id": "double_clean", "name": "🔄 Двойное очищение", "emoji": "🌙", "points": 15},
    {"id": "moisturize", "name": "💆‍♀️ Нанес(ла) крем", "emoji": "✨", "points": 5},
    {"id": "mask", "name": "🎭 Сделал(а) маску", "emoji": "🧖", "points": 20},
]

@router.message(F.text == "📋 Трекер привычек")
async def habit_tracker(message: Message):
    """Главное меню трекера привычек"""
    user_id = message.from_user.id
    
    init_user_habits(user_id)
    stats = get_habit_stats(user_id)
    
    text = f"""
📋 *Трекер привычек*

📅 *Сегодня:* {datetime.now().strftime('%d.%m.%Y')}

📊 *Прогресс:* {stats['completed']}/{stats['total']} привычек
🏆 *Очков сегодня:* {stats['today_points']}
⭐ *Всего очков:* {stats['total_points']}
🔥 *Серия:* {stats['streak']} дней

👇 *Отмечайте выполненные привычки:*
"""
    
    kb = create_habits_keyboard(user_id)
    
    await message.answer(text, reply_markup=kb, parse_mode="Markdown")

def init_user_habits(user_id):
    """Инициализация привычек"""
    if user_id not in habits_db:
        habits_db[user_id] = {
            "habits": {h["id"]: {"completed": False} for h in HABITS},
            "total_points": 0,
            "streak": 0,
            "last_active": None,
            "last_reset": None,
            "today_points": 0,
            "history": []
        }

def create_habits_keyboard(user_id):
    """Создание клавиатуры"""
    user_data = habits_db.get(user_id, {})
    user_habits = user_data.get("habits", {})
    
    check_and_reset_daily(user_id)
    
    buttons = []
    for habit in HABITS:
        completed = user_habits.get(habit["id"], {}).get("completed", False)
        status = "✅" if completed else habit["emoji"]
        button = InlineKeyboardButton(
            text=f"{status} {habit['name']} (+{habit['points']})",
            callback_data=f"habit_{habit['id']}"
        )
        buttons.append([button])
    
    buttons.append([
        InlineKeyboardButton(text="📊 Статистика", callback_data="habit_stats"),
        InlineKeyboardButton(text="🔥 Серия", callback_data="habit_streak")
    ])
    buttons.append([
        InlineKeyboardButton(text="🔙 В STYLE", callback_data="back_to_style")
    ])
    
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def check_and_reset_daily(user_id):
    """Проверка и сброс ежедневных привычек"""
    today = datetime.now().date()
    user_data = habits_db[user_id]
    
    if "last_reset" not in user_data or user_data["last_reset"] != today:
        # Сбрасываем привычки
        for habit_id in user_data["habits"]:
            user_data["habits"][habit_id]["completed"] = False
        
        # Обновляем серию
        if "last_active" in user_data and user_data["last_active"] == today - timedelta(days=1):
            user_data["streak"] += 1
        else:
            user_data["streak"] = 1
        
        user_data["last_reset"] = today
        user_data["today_points"] = 0

@router.callback_query(F.data.startswith("habit_"))
async def toggle_habit(callback: CallbackQuery):
    """Отметить привычку"""
    user_id = callback.from_user.id
    habit_id = callback.data.replace("habit_", "")
    
    init_user_habits(user_id)
    check_and_reset_daily(user_id)
    
    user_data = habits_db[user_id]
    current = user_data["habits"][habit_id]["completed"]
    
    if not current:
        for habit in HABITS:
            if habit["id"] == habit_id:
                user_data["total_points"] += habit["points"]
                user_data["today_points"] += habit["points"]
                break
    
    user_data["habits"][habit_id]["completed"] = not current
    user_data["last_active"] = datetime.now().date()
    
    await update_habit_message(callback)
    await callback.answer()

async def update_habit_message(callback: CallbackQuery):
    """Обновление сообщения"""
    user_id = callback.from_user.id
    stats = get_habit_stats(user_id)
    
    text = f"""
📋 *Трекер привычек*

📅 *Сегодня:* {datetime.now().strftime('%d.%m.%Y')}

📊 *Прогресс:* {stats['completed']}/{stats['total']} привычек
🏆 *Очков сегодня:* {stats['today_points']}
⭐ *Всего очков:* {stats['total_points']}
🔥 *Серия:* {stats['streak']} дней
"""
    
    kb = create_habits_keyboard(user_id)
    
    await callback.message.edit_text(text, reply_markup=kb, parse_mode="Markdown")

def get_habit_stats(user_id):
    """Получение статистики"""
    user_data = habits_db.get(user_id, {})
    habits = user_data.get("habits", {})
    
    completed = sum(1 for h in habits.values() if h.get("completed", False))
    total = len(HABITS)
    
    return {
        "completed": completed,
        "total": total,
        "today_points": user_data.get("today_points", 0),
        "total_points": user_data.get("total_points", 0),
        "streak": user_data.get("streak", 0)
    }

@router.callback_query(F.data == "habit_stats")
async def show_habit_stats(callback: CallbackQuery):
    """Показать статистику"""
    user_id = callback.from_user.id
    stats = get_habit_stats(user_id)
    
    if stats['streak'] >= 7:
        week_status = "✅"
    else:
        week_status = f"{stats['streak']}/7"
    
    if stats['streak'] >= 30:
        month_status = "✅"
    else:
        month_status = f"{stats['streak']}/30"
    
    if stats['streak'] >= 100:
        hundred_status = "✅"
    else:
        hundred_status = f"{stats['streak']}/100"
    
    text = f"""
📊 *Расширенная статистика*

🔥 *Серия:* {stats['streak']} дней
⭐ *Всего очков:* {stats['total_points']}

🏆 *Достижения:*
✅ Новичок (7 дней) — {week_status}
🔜 Зелёный (30 дней) — {month_status}
🔜 Мастер (100 дней) — {hundred_status}
"""
    
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_habits")]
    ])
    
    await callback.message.edit_text(text, reply_markup=kb, parse_mode="Markdown")
    await callback.answer()

@router.callback_query(F.data == "habit_streak")
async def show_streak(callback: CallbackQuery):
    """Показать серию"""
    user_id = callback.from_user.id
    stats = get_habit_stats(user_id)
    
    text = f"""
🔥 *Ваша серия: {stats['streak']} дней*

💪 *Продолжайте в том же духе!*

🎯 *Следующие цели:*
• 7 дней: {'✅' if stats['streak'] >= 7 else f'{stats["streak"]}/7'}
• 30 дней: {'✅' if stats['streak'] >= 30 else f'{stats["streak"]}/30'}
• 100 дней: {'✅' if stats['streak'] >= 100 else f'{stats["streak"]}/100'}
"""
    
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_habits")]
    ])
    
    await callback.message.edit_text(text, reply_markup=kb, parse_mode="Markdown")
    await callback.answer()

@router.callback_query(F.data == "back_to_habits")
async def back_to_habits(callback: CallbackQuery):
    """Назад к трекеру"""
    await habit_tracker(callback.message)
    await callback.answer()

@router.callback_query(F.data == "back_to_style")
async def back_to_style(callback: CallbackQuery):
    """Возврат в меню STYLE"""
    from keyboards import style_menu
    await callback.message.answer(
        "💄 *STYLE: Макияж и стиль*",
        reply_markup=style_menu(),
        parse_mode="Markdown"
    )
    await callback.answer()