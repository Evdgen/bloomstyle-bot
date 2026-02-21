from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from datetime import datetime

from database import get_user_city, get_user_skin_type, get_user_budget
from premium import (
    is_premium, activate_premium, activate_trial, has_used_trial,
    get_premium_expiry, PREMIUM_PRICES, PREMIUM_FEATURES
)
from .payments import PREMIUM_STARS
from .crypto_payments import CRYPTO_PRICES

router = Router()

@router.message(Command("premium"))
async def cmd_premium(message: Message):
    """Информация о Premium"""
    user_id = message.from_user.id
    premium_status = is_premium(user_id)
    
    if premium_status:
        expiry = get_premium_expiry(user_id)
        days_left = (expiry - datetime.now()).days if expiry else 0
        
        features_list = "\n".join([f"✅ {v}" for v in PREMIUM_FEATURES.values()])
        
        text = f"""
💎 BloomStyle Premium — АКТИВЕН

👑 Статус: ✅ Premium подписка
📅 Действует до: {expiry.strftime('%d.%m.%Y') if expiry else 'бессрочно'}
⏳ Осталось дней: {days_left}

✨ ДОСТУПНЫЕ ФУНКЦИИ:
{features_list}

💎 Спасибо, что вы с нами!
"""
        buttons = [
            [
                InlineKeyboardButton(text="📊 Климатический дневник", callback_data="premium_climate"),
                InlineKeyboardButton(text="🧪 Виртуальная косметичка", callback_data="premium_cosmetics")
            ],
            [
                InlineKeyboardButton(text="📈 Расширенная статистика", callback_data="premium_stats"),
                InlineKeyboardButton(text="🔬 Глубокий разбор", callback_data="premium_analyzer")
            ],
            [
                InlineKeyboardButton(text="🎨 Персональные образы", callback_data="premium_looks")
            ]
        ]
        keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    else:
        rub_month = int(CRYPTO_PRICES["month"] * 95)
        rub_year = int(CRYPTO_PRICES["year"] * 95)
        
        trial_text = "🎁 2 дня бесплатно" if not has_used_trial(user_id) else "❌ Пробный период использован"
        
        text = f"""
💎 BloomStyle Premium

🌟 ПРЕИМУЩЕСТВА:

📊 Климатический дневник — полная история реакций
🧪 Виртуальная косметичка — до 100 средств
📈 Расширенная статистика — экономия и прогресс
🔬 Глубокий разбор составов — детальный анализ
🎨 Персональные образы — стиль под вас

💰 СТОИМОСТЬ:

⭐ Telegram Stars:
• 1 месяц — {PREMIUM_STARS['month']} Stars
• 1 год — {PREMIUM_STARS['year']} Stars

💎 Криптовалюта (USDT):
• 1 месяц — {CRYPTO_PRICES['month']} USDT ≈ {rub_month}₽
• 1 год — {CRYPTO_PRICES['year']} USDT ≈ {rub_year}₽

{trial_text}
"""
        keyboard = get_premium_keyboard(user_id)
    
    await message.answer(text, reply_markup=keyboard)

def get_premium_keyboard(user_id):
    """Клавиатура для Premium с проверкой триала"""
    buttons = []
    
    # Кнопка триала (только если не использован)
    if not has_used_trial(user_id):
        buttons.append([InlineKeyboardButton(text="🎁 2 дня бесплатно", callback_data="activate_trial")])
    
    buttons.append([InlineKeyboardButton(text="💳 Купить Premium", callback_data="show_prices")])
    buttons.append([
        InlineKeyboardButton(text="📊 Климатический дневник", callback_data="premium_climate"),
        InlineKeyboardButton(text="🧪 Виртуальная косметичка", callback_data="premium_cosmetics")
    ])
    buttons.append([
        InlineKeyboardButton(text="📈 Расширенная статистика", callback_data="premium_stats"),
        InlineKeyboardButton(text="🔬 Глубокий разбор", callback_data="premium_analyzer")
    ])
    buttons.append([InlineKeyboardButton(text="🎨 Персональные образы", callback_data="premium_looks")])
    
    return InlineKeyboardMarkup(inline_keyboard=buttons)

@router.callback_query(F.data == "activate_trial")
async def process_activate_trial(callback: CallbackQuery):
    """Активация пробного периода (только 1 раз)"""
    user_id = callback.from_user.id
    
    success, message = activate_trial(user_id)
    
    if success:
        expiry = get_premium_expiry(user_id)
        await callback.message.edit_text(
            f"🎁 *{message}*\n\n"
            f"✅ Premium доступен до {expiry.strftime('%d.%m.%Y')}\n"
            f"⏳ Осталось: 2 дня\n\n"
            f"✨ Теперь вам доступны все Premium-функции!",
            parse_mode="Markdown"
        )
    else:
        await callback.message.edit_text(
            f"❌ *{message}*",
            parse_mode="Markdown"
        )
    await callback.answer()

# ==================== PREMIUM ФУНКЦИИ ====================

@router.callback_query(F.data == "premium_climate")
async def process_climate_diary(callback: CallbackQuery):
    """Климатический дневник (Premium)"""
    user_id = callback.from_user.id
    
    if not is_premium(user_id):
        await callback.message.edit_text(
            "💎 *Эта функция доступна только в Premium!*\n\n"
            "Оформите подписку — /premium",
            parse_mode="Markdown"
        )
        await callback.answer()
        return
    
    await callback.message.edit_text(
        f"📊 *Климатический дневник*\n\n"
        f"📅 *Статистика за 30 дней:*\n"
        f"• ☀️ УФ-индекс выше 5: 12 дней\n"
        f"• 💧 Влажность ниже 40%: 18 дней\n"
        f"• 🌬️ Ветер выше 5 м/с: 9 дней\n\n"
        f"📈 *Реакции вашей кожи:*\n"
        f"• Сухость/шелушение: 7 дней\n"
        f"• Жирный блеск: 5 дней\n"
        f"• Покраснения: 3 дня\n\n"
        f"🔍 *Закономерности:*\n"
        f"• Сухость появляется через 1 день после низкой влажности\n"
        f"• Покраснения связаны с ветром >6 м/с\n\n"
        f"💡 *Прогноз на неделю:*\n"
        f"• Завтра: риск обезвоживания (влажность 35%)\n"
        f"• Через 2 дня: возможны покраснения (ветер 7 м/с)",
        parse_mode="Markdown"
    )
    await callback.answer()

@router.callback_query(F.data == "premium_cosmetics")
async def process_virtual_cosmetics(callback: CallbackQuery):
    """Виртуальная косметичка (Premium)"""
    user_id = callback.from_user.id
    
    if not is_premium(user_id):
        await callback.message.edit_text(
            "💎 *Эта функция доступна только в Premium!*\n\n"
            "Оформите подписку — /premium",
            parse_mode="Markdown"
        )
        await callback.answer()
        return
    
    await callback.message.edit_text(
        f"🧪 *Виртуальная косметичка*\n\n"
        f"📦 *Ваши средства (3/100):*\n\n"
        f"1️⃣ *La Roche-Posay Cicaplast Baume B5*\n"
        f"   • Куплен: 01.02.2026\n"
        f"   • Годен до: 01.02.2027\n"
        f"   • Совместимость: ✅\n\n"
        f"2️⃣ *The Ordinary Niacinamide 10% + Zinc*\n"
        f"   • Куплен: 05.02.2026\n"
        f"   • Годен до: 05.02.2027\n"
        f"   • Совместимость: ⚠️ Не смешивать с витамином С\n\n"
        f"3️⃣ *Cerave Moisturizing Cream*\n"
        f"   • Куплен: 10.02.2026\n"
        f"   • Годен до: 10.02.2027\n"
        f"   • Совместимость: ✅\n\n"
        f"➕ *Добавить средство* — /add_product",
        parse_mode="Markdown"
    )
    await callback.answer()

@router.callback_query(F.data == "premium_stats")
async def process_premium_stats(callback: CallbackQuery):
    """Расширенная статистика (Premium)"""
    user_id = callback.from_user.id
    
    if not is_premium(user_id):
        await callback.message.edit_text(
            "💎 *Эта функция доступна только в Premium!*\n\n"
            "Оформите подписку — /premium",
            parse_mode="Markdown"
        )
        await callback.answer()
        return
    
    city = get_user_city(user_id) or "Москва"
    skin_type = get_user_skin_type(user_id)
    
    skin_names = {
        "dry": "Сухая", 
        "oily": "Жирная",
        "combination": "Комбинированная", 
        "normal": "Нормальная", 
        "sensitive": "Чувствительная"
    }
    skin_display = skin_names.get(skin_type, "Комбинированная")
    
    await callback.message.edit_text(
        f"📈 *Расширенная статистика*\n\n"
        f"👤 *Ваш профиль:*\n"
        f"• Город: {city}\n"
        f"• Тип кожи: {skin_display}\n\n"
        f"💰 *Экономия:*\n"
        f"• На мини-версиях: 1 240₽\n"
        f"• На неподходящих средствах: 3 500₽\n"
        f"• Всего сэкономлено: 4 740₽\n\n"
        f"📊 *Активность:*\n"
        f"• Сохранённых рутин: 12\n"
        f"• Пройденных тестов: 3\n"
        f"• Дней в BloomStyle: 14\n\n"
        f"🏆 *Прогресс:*\n"
        f"• Текущий челлендж: 45%\n"
        f"• Заработано баллов: 230\n"
        f"• Место в рейтинге: 127",
        parse_mode="Markdown"
    )
    await callback.answer()

@router.callback_query(F.data == "premium_analyzer")
async def process_premium_analyzer(callback: CallbackQuery):
    """Глубокий разбор составов (Premium)"""
    user_id = callback.from_user.id
    
    if not is_premium(user_id):
        await callback.message.edit_text(
            "💎 *Эта функция доступна только в Premium!*\n\n"
            "Оформите подписку — /premium",
            parse_mode="Markdown"
        )
        await callback.answer()
        return
    
    await callback.message.edit_text(
        f"🔬 *Глубокий разбор составов*\n\n"
        f"✨ *Детальный анализ ингредиентов:*\n"
        f"• Совместимость компонентов\n"
        f"• Эффективные концентрации\n"
        f"• Исследования и доказательства\n"
        f"• Альтернативы и аналоги\n\n"
        f"📝 *Введите название средства или его состав:*\n\n"
        f"Пример: Cicaplast, Effaclar, The Ordinary",
        parse_mode="Markdown"
    )
    await callback.answer()

@router.callback_query(F.data == "premium_looks")
async def process_premium_looks(callback: CallbackQuery):
    """Персональные образы (Premium)"""
    user_id = callback.from_user.id
    
    if not is_premium(user_id):
        await callback.message.edit_text(
            "💎 *Эта функция доступна только в Premium!*\n\n"
            "Оформите подписку — /premium",
            parse_mode="Markdown"
        )
        await callback.answer()
        return
    
    await callback.message.edit_text(
        f"🎨 *Персональные образы*\n\n"
        f"✨ *На основе вашего цветотипа и формы лица:*\n\n"
        f"1️⃣ 👔 **«Деловой стиль»**\n"
        f"   • Макияж: матовая кожа + nude помада\n"
        f"   • Одежда: классический костюм\n\n"
        f"2️⃣ 💕 **«Романтичный вечер»**\n"
        f"   • Макияж: сияющая кожа + красные губы\n"
        f"   • Одежда: коктейльное платье\n\n"
        f"3️⃣ 🌿 **«Повседневный образ»**\n"
        f"   • Макияж: BB-крем + тинт\n"
        f"   • Одежда: джинсы + свитер\n\n"
        f"➕ *Сохранить свой образ* — скоро",
        parse_mode="Markdown"
    )
    await callback.answer()