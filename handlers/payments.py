from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, PreCheckoutQuery, LabeledPrice, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from datetime import datetime

from premium import activate_premium, get_premium_expiry

router = Router()

# Цены в Telegram Stars
PREMIUM_STARS = {
    "month": 149,  # 149 звёзд
    "year": 990    # 990 звёзд
}

@router.callback_query(F.data == "buy_premium_month")
async def buy_premium_month(callback: CallbackQuery):
    """Покупка Premium на 1 месяц за Stars"""
    await callback.message.answer_invoice(
        title="💎 BloomStyle Premium — 1 месяц",
        description="✨ Полный доступ ко всем Premium-функциям на 30 дней",
        payload="premium_month",
        currency="XTR",
        prices=[LabeledPrice(label="Premium 1 месяц", amount=PREMIUM_STARS["month"])],
        provider_token=""
    )
    await callback.answer()

@router.callback_query(F.data == "buy_premium_year")
async def buy_premium_year(callback: CallbackQuery):
    """Покупка Premium на 1 год за Stars"""
    savings = PREMIUM_STARS["month"] * 12 - PREMIUM_STARS["year"]
    await callback.message.answer_invoice(
        title="💎 BloomStyle Premium — 1 год",
        description=f"✨ Полный доступ на 365 дней (экономия {savings}⭐!)",
        payload="premium_year",
        currency="XTR",
        prices=[LabeledPrice(label="Premium 1 год", amount=PREMIUM_STARS["year"])],
        provider_token=""
    )
    await callback.answer()

@router.pre_checkout_query()
async def pre_checkout_handler(pre_checkout: PreCheckoutQuery):
    """Обязательная проверка перед оплатой"""
    await pre_checkout.answer(ok=True)

@router.message(F.successful_payment)
async def successful_payment_handler(message: Message):
    """Обработка успешной оплаты"""
    user_id = message.from_user.id
    payload = message.successful_payment.invoice_payload
    
    if payload == "premium_month":
        activate_premium(user_id, 30)
        stars = PREMIUM_STARS["month"]
        period = "1 месяц"
    elif payload == "premium_year":
        activate_premium(user_id, 365)
        stars = PREMIUM_STARS["year"]
        period = "1 год"
    else:
        return
    
    expiry = get_premium_expiry(user_id)
    
    await message.answer(
        f"🎉 *Спасибо за покупку!*\n\n"
        f"💎 *BloomStyle Premium — {period}*\n"
        f"⭐ Потрачено: {stars} Stars\n"
        f"📅 Активен до: {expiry.strftime('%d.%m.%Y') if expiry else 'бессрочно'}\n\n"
        f"✨ Все Premium-функции уже доступны!",
        parse_mode="Markdown"
    )