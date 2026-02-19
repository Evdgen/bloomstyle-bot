from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime, timedelta
import random

router = Router()

# Хранилище последних открытий
last_opened = {}
user_rewards = {}

# Список наград
REWARDS = {
    "common": [
        {"name": "💧 Мини-версия крема", "value": "Скидка 15% на Cerave", "type": "discount", "amount": 15},
        {"name": "✨ +10 баллов", "value": "баллы", "type": "points", "amount": 10},
        {"name": "🎯 Рекомендация дня", "value": "VIP-рекомендация", "type": "feature", "feature": "vip"},
    ],
    "rare": [
        {"name": "🔥 +50 баллов", "value": "баллы", "type": "points", "amount": 50},
        {"name": "🧪 Мини-версия сыворотки", "value": "The Ordinary", "type": "product", "product": "ha"},
        {"name": "💰 Секретный промокод", "value": "300₽", "type": "promo", "amount": 300},
    ],
    "epic": [
        {"name": "💎 3 дня Premium", "value": "бесплатно", "type": "premium", "days": 3},
        {"name": "💯 +100 баллов", "value": "баллы", "type": "points", "amount": 100},
        {"name": "👑 VIP-статус на неделю", "value": "особые функции", "type": "feature", "feature": "vip"},
    ]
}

@router.message(F.text == "🎁 Сюрприз дня")
async def mystery_box(message: Message):
    """Главное меню коробки сюрпризов"""
    user_id = message.from_user.id
    
    # Проверяем, можно ли открыть
    can_open, time_left = can_open_box(user_id)
    
    if user_id not in user_rewards:
        user_rewards[user_id] = []
    
    stats = get_box_stats(user_id)
    
    status = "✅ *Доступно!*" if can_open else f"⏳ *Доступно через:* {time_left}"
    
    text = f"""
🎁 *Коробка сюрпризов*

Каждый день можно открыть одну коробку и получить:
• 💧 Скидки на косметику
• ✨ Бонусные баллы
• 🧪 Бесплатные мини-версии
• 💎 Пробный Premium

{status}

📊 *Статистика:*
• Открыто коробок: {stats['total']}
• Редких находок: {stats['rare']}
• Эпических: {stats['epic']}
"""
    
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎁 Открыть коробку!", callback_data="open_box")],
        [InlineKeyboardButton(text="📦 Мои награды", callback_data="my_rewards")],
        [InlineKeyboardButton(text="🔙 В STYLE", callback_data="back_to_style")]
    ])
    
    await message.answer(text, reply_markup=kb, parse_mode="Markdown")

def can_open_box(user_id):
    """Проверка, можно ли открыть коробку"""
    if user_id not in last_opened:
        return True, None
    
    last = last_opened[user_id]
    now = datetime.now()
    diff = now - last
    
    if diff.total_seconds() < 86400:  # 24 часа
        hours_left = 23 - diff.seconds // 3600
        minutes_left = 59 - (diff.seconds % 3600) // 60
        return False, f"{hours_left}ч {minutes_left}м"
    
    return True, None

def get_box_stats(user_id):
    """Статистика коробок"""
    rewards = user_rewards.get(user_id, [])
    
    stats = {
        'total': len(rewards),
        'common': sum(1 for r in rewards if r['category'] == 'common'),
        'rare': sum(1 for r in rewards if r['category'] == 'rare'),
        'epic': sum(1 for r in rewards if r['category'] == 'epic')
    }
    return stats

@router.callback_query(F.data == "open_box")
async def open_box(callback: CallbackQuery):
    """Открытие коробки"""
    user_id = callback.from_user.id
    
    # Проверяем, можно ли открыть
    can_open, time_left = can_open_box(user_id)
    if not can_open:
        await callback.answer(f"⏳ Подождите {time_left}", show_alert=True)
        return
    
    # Обновляем время последнего открытия
    last_opened[user_id] = datetime.now()
    
    # Выбираем награду
    reward = get_random_reward()
    
    # Сохраняем награду
    if user_id not in user_rewards:
        user_rewards[user_id] = []
    user_rewards[user_id].append(reward)
    
    # Показываем результат
    await show_reward(callback.message, reward)
    await callback.answer()

def get_random_reward():
    """Получение случайной награды"""
    roll = random.random()
    
    if roll < 0.7:
        category = "common"
    elif roll < 0.95:
        category = "rare"
    else:
        category = "epic"
    
    reward = random.choice(REWARDS[category])
    reward["category"] = category
    return reward

async def show_reward(message, reward):
    """Показать полученную награду"""
    
    colors = {"common": "📦", "rare": "✨", "epic": "💎"}
    emoji = colors.get(reward["category"], "🎁")
    
    text = f"""
{emoji} *ВЫ ПОЛУЧИЛИ!*

🎉 *{reward['name']}*

✨ *Описание:* {reward['value']}

📅 *Следующая коробка будет доступна через 24 часа*
"""
    
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📦 Забрать награду", callback_data="claim_reward")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_box")]
    ])
    
    await message.edit_text(text, reply_markup=kb, parse_mode="Markdown")

@router.callback_query(F.data == "claim_reward")
async def claim_reward(callback: CallbackQuery):
    """Забрать награду"""
    await callback.answer("✅ Награда активирована! Подробнее в /profile", show_alert=True)
    await back_to_box(callback)

@router.callback_query(F.data == "back_to_box")
async def back_to_box(callback: CallbackQuery):
    """Назад к коробке"""
    await mystery_box(callback.message)
    await callback.answer()

@router.callback_query(F.data == "my_rewards")
async def my_rewards(callback: CallbackQuery):
    """Мои награды"""
    user_id = callback.from_user.id
    rewards = user_rewards.get(user_id, [])
    stats = get_box_stats(user_id)
    
    if not rewards:
        text = "📦 *У вас пока нет наград*\n\nОткройте коробку!"
    else:
        text = f"📦 *Мои награды* (всего: {stats['total']})\n\n"
        for i, r in enumerate(rewards[-5:], 1):
            emoji = "💎" if r['category'] == 'epic' else "✨" if r['category'] == 'rare' else "📦"
            text += f"{emoji} {r['name']} — {r['value']}\n"
    
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_box")]
    ])
    
    await callback.message.edit_text(text, reply_markup=kb, parse_mode="Markdown")
    await callback.answer()