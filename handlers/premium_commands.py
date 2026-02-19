from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from datetime import datetime

from database import get_user_city, get_user_skin_type, get_user_budget
from premium import is_premium, activate_premium, get_premium_expiry, PREMIUM_PRICES
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
        buttons = [
            [
                InlineKeyboardButton(text="📊 Климатический дневник", callback_data="premium_climate"),
                InlineKeyboardButton(text="🧪 Виртуальная косметичка", callback_data="premium_cosmetics")
            ],
            [
                InlineKeyboardButton(text="📸 AR-примерка", callback_data="premium_ar"),
                InlineKeyboardButton(text="📈 Расширенная статистика", callback_data="premium_stats")
            ]
        ]
        keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    else:
        rub_month = int(CRYPTO_PRICES["month"] * 95)
        rub_year = int(CRYPTO_PRICES["year"] * 95)
        
        text = f"""
💎 BloomStyle Premium

🌟 ПРЕИМУЩЕСТВА:

📊 Климатический дневник — полная история реакций
🧪 Виртуальная косметичка — до 100 средств
📸 AR-примерка макияжа — 50 примерок в день
📈 Расширенная статистика — экономия и прогресс

💰 СТОИМОСТЬ:

⭐ Telegram Stars:
• 1 месяц — {PREMIUM_STARS['month']} Stars
• 1 год — {PREMIUM_STARS['year']} Stars

💎 Криптовалюта (USDT):
• 1 месяц — {CRYPTO_PRICES['month']} USDT ≈ {rub_month}₽
• 1 год — {CRYPTO_PRICES['year']} USDT ≈ {rub_year}₽

🎁 Пробный период: 2 дня бесплатно!
"""
        keyboard = get_premium_keyboard()
    
    await message.answer(text, reply_markup=keyboard)

def get_premium_keyboard():
    """Клавиатура для Premium"""
    buttons = [
        [
            InlineKeyboardButton(text="🎁 2 дня бесплатно", callback_data="activate_trial"),
            InlineKeyboardButton(text="💳 Купить Premium", callback_data="show_prices")
        ],
        [
            InlineKeyboardButton(text="📊 Климатический дневник", callback_data="premium_climate"),
            InlineKeyboardButton(text="🧪 Виртуальная косметичка", callback_data="premium_cosmetics")
        ],
        [
            InlineKeyboardButton(text="📸 AR-примерка", callback_data="premium_ar"),
            InlineKeyboardButton(text="📈 Расширенная статистика", callback_data="premium_stats")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

@router.callback_query(F.data == "show_prices")
async def show_prices(callback: CallbackQuery):
    """Показать варианты оплаты"""
    buttons = [
        [
            InlineKeyboardButton(text="⭐ Telegram Stars", callback_data="show_stars_prices"),
            InlineKeyboardButton(text="💎 Криптовалюта (USDT)", callback_data="show_crypto_prices")
        ],
        [
            InlineKeyboardButton(text="🎁 2 дня бесплатно", callback_data="activate_trial")
        ],
        [
            InlineKeyboardButton(text="🔙 Назад к Premium", callback_data="back_to_premium")
        ]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    
    await callback.message.edit_text(
        "💳 *Выберите способ оплаты Premium*\n\n"
        "⭐ *Telegram Stars* — оплата через Telegram\n"
        "• Мгновенно, без комиссии\n"
        "• Нужно купить Stars в Telegram\n\n"
        "💎 *Криптовалюта (USDT)* — оплата через CryptoBot\n"
        "• Стабильная монета, привязана к доллару\n"
        "• Автоматическая проверка оплаты\n\n"
        "👇 *Выберите удобный способ:*",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )
    await callback.answer()

@router.callback_query(F.data == "show_stars_prices")
async def show_stars_prices(callback: CallbackQuery):
    """Показать цены в звёздах"""
    savings = PREMIUM_STARS["month"] * 12 - PREMIUM_STARS["year"]
    
    buttons = [
        [
            InlineKeyboardButton(text=f"⭐ 1 месяц — {PREMIUM_STARS['month']} Stars", callback_data="buy_premium_month"),
            InlineKeyboardButton(text=f"⭐ 1 год — {PREMIUM_STARS['year']} Stars", callback_data="buy_premium_year")
        ],
        [
            InlineKeyboardButton(text="💎 Криптовалюта", callback_data="show_crypto_prices"),
            InlineKeyboardButton(text="🎁 2 дня бесплатно", callback_data="activate_trial")
        ],
        [
            InlineKeyboardButton(text="🔙 К выбору способа", callback_data="show_prices")
        ]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    
    await callback.message.edit_text(
        f"⭐ *Оплата Telegram Stars*\n\n"
        f"⭐ *1 месяц* — {PREMIUM_STARS['month']} Stars\n"
        f"⭐ *1 год* — {PREMIUM_STARS['year']} Stars\n"
        f"✨ *Экономия при годовой подписке: {savings} Stars!*\n\n"
        f"✅ Климатический дневник\n"
        f"✅ Виртуальная косметичка\n"
        f"✅ AR-примерка макияжа\n"
        f"✅ Расширенная статистика\n\n"
        f"👇 *Выберите тариф:*",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )
    await callback.answer()

@router.callback_query(F.data == "show_crypto_prices")
async def show_crypto_prices(callback: CallbackQuery):
    """Показать цены в крипте"""
    savings = CRYPTO_PRICES["month"] * 12 - CRYPTO_PRICES["year"]
    rub_month = int(CRYPTO_PRICES["month"] * 95)
    rub_year = int(CRYPTO_PRICES["year"] * 95)
    
    buttons = [
        [
            InlineKeyboardButton(text=f"💎 1 месяц — {CRYPTO_PRICES['month']} USDT", callback_data="buy_crypto_month"),
            InlineKeyboardButton(text=f"💎 1 год — {CRYPTO_PRICES['year']} USDT", callback_data="buy_crypto_year")
        ],
        [
            InlineKeyboardButton(text="⭐ Telegram Stars", callback_data="show_stars_prices"),
            InlineKeyboardButton(text="🎁 2 дня бесплатно", callback_data="activate_trial")
        ],
        [
            InlineKeyboardButton(text="🔙 К выбору способа", callback_data="show_prices")
        ]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    
    await callback.message.edit_text(
        f"💎 *Оплата криптовалютой (USDT)*\n\n"
        f"💎 *1 месяц* — {CRYPTO_PRICES['month']} USDT ≈ {rub_month}₽\n"
        f"💎 *1 год* — {CRYPTO_PRICES['year']} USDT ≈ {rub_year}₽\n"
        f"✨ *Экономия: {savings:.2f} USDT*\n\n"
        f"✅ Стабильная монета USDT (привязана к доллару)\n"
        f"✅ Автоматическая проверка оплаты\n"
        f"✅ Мгновенная активация Premium\n\n"
        f"👇 *Выберите тариф:*",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )
    await callback.answer()

@router.callback_query(F.data == "activate_trial")
async def process_activate_trial(callback: CallbackQuery):
    """Активация пробного периода на 2 дня"""
    user_id = callback.from_user.id
    
    if is_premium(user_id):
        await callback.message.edit_text(
            "❌ *У вас уже активна Premium-подписка!*",
            parse_mode="Markdown"
        )
        await callback.answer()
        return
    
    activate_premium(user_id, 2)
    expiry = get_premium_expiry(user_id)
    
    await callback.message.edit_text(
        f"🎁 *Пробный период активирован!*\n\n"
        f"✅ Premium доступен до {expiry.strftime('%d.%m.%Y')}\n"
        f"⏳ Осталось: 2 дня\n\n"
        f"💎 Используйте /premium чтобы увидеть все функции",
        parse_mode="Markdown"
    )
    await callback.answer("✅ Триал активирован!")

@router.callback_query(F.data == "back_to_premium")
async def process_back_to_premium(callback: CallbackQuery):
    """Возврат к меню Premium"""
    await cmd_premium(callback.message)
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
        f"• 💧 Влажность ниже 40%: 18 дней\n\n"
        f"📈 *Реакции вашей кожи:*\n"
        f"• Сухость/шелушение: 7 дней\n"
        f"• Жирный блеск: 5 дней\n\n"
        f"💡 *Прогноз:* Завтра риск обезвоживания",
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
        f"1️⃣ La Roche-Posay Cicaplast\n"
        f"2️⃣ The Ordinary Niacinamide\n"
        f"3️⃣ Cerave Moisturizing Cream\n\n"
        f"➕ *Добавить средство* — скоро",
        parse_mode="Markdown"
    )
    await callback.answer()

@router.callback_query(F.data == "premium_ar")
async def process_ar_makeup(callback: CallbackQuery):
    """AR-примерка макияжа (Premium)"""
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
        f"📸 *AR-примерка макияжа*\n\n"
        f"🎨 *Доступно сегодня:* 50/50 примерок\n\n"
        f"💄 Помада — 24 оттенка\n"
        f"👁️ Тени — 15 палитр\n\n"
        f"🔗 *Ссылка:* https://bloomstyle.ar/makeup",
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
        f"👤 Город: {city}\n"
        f"🧬 Тип кожи: {skin_display}\n\n"
        f"💰 Экономия: 1 240₽\n"
        f"📊 Дней в BloomStyle: 14",
        parse_mode="Markdown"
    )
    await callback.answer()