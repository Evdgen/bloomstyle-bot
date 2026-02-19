from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
import requests
from datetime import datetime

from premium import activate_premium, get_premium_expiry

router = Router()

# 👇 ТВОЙ API КЛЮЧ (КОТОРЫЙ ТЫ ПОЛУЧИЛА)
CRYPTO_API_KEY = "533292:AATaQU5yY4LaGZnNm8m6Go8GgSsWHI4qs14"
CRYPTO_API_URL = "https://pay.crypt.bot/api"

# Цены в USDT (1 USDT ≈ 1$ ≈ 95₽)
CRYPTO_PRICES = {
    "month": 1.57,  # 1.57 USDT = 149₽
    "year": 10.42   # 10.42 USDT = 990₽
}

# Хранилище счетов
user_invoices = {}

def create_crypto_invoice(amount_usd, description, payload):
    """Создание счета в CryptoBot через API"""
    try:
        url = f"{CRYPTO_API_URL}/createInvoice"
        headers = {
            "Crypto-Pay-API-Token": CRYPTO_API_KEY,
            "Content-Type": "application/json"
        }
        data = {
            "asset": "USDT",
            "amount": str(amount_usd),
            "description": description,
            "payload": payload,
            "paid_btn_name": "openBot",
            "paid_btn_url": "https://t.me/BloomStyle_bot",
            "allow_comments": False,
            "allow_anonymous": False
        }
        
        response = requests.post(url, headers=headers, json=data)
        result = response.json()
        
        if result.get("ok"):
            return result["result"]
        else:
            print(f"Ошибка CryptoBot: {result}")
            return None
    except Exception as e:
        print(f"Ошибка при создании счета: {e}")
        return None

def check_invoice_status(invoice_id):
    """Проверка статуса счета"""
    try:
        url = f"{CRYPTO_API_URL}/getInvoices"
        headers = {"Crypto-Pay-API-Token": CRYPTO_API_KEY}
        params = {"invoice_ids": [invoice_id]}
        
        response = requests.get(url, headers=headers, params=params)
        result = response.json()
        
        if result.get("ok") and result.get("result") and len(result["result"]["items"]) > 0:
            return result["result"]["items"][0].get("status")
        return None
    except:
        return None

@router.callback_query(F.data == "buy_crypto_month")
async def buy_crypto_month(callback: CallbackQuery):
    """Покупка Premium на 1 месяц через крипту"""
    await callback.message.edit_text(
        "⏳ *Создаю счет для оплаты...*",
        parse_mode="Markdown"
    )
    
    invoice = create_crypto_invoice(
        CRYPTO_PRICES["month"],
        "💎 BloomStyle Premium — 1 месяц",
        "crypto_month"
    )
    
    if invoice and invoice.get("pay_url"):
        user_invoices[callback.from_user.id] = {
            "invoice_id": invoice["invoice_id"],
            "amount": CRYPTO_PRICES["month"],
            "period": 30
        }
        
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="💳 Оплатить USDT", url=invoice["pay_url"])],
            [InlineKeyboardButton(text="✅ Проверить оплату", callback_data="check_crypto_payment")],
            [InlineKeyboardButton(text="⭐ Оплатить Stars", callback_data="show_stars_prices")],
            [InlineKeyboardButton(text="🔙 Назад", callback_data="show_prices")]
        ])
        
        rub = int(CRYPTO_PRICES["month"] * 95)
        await callback.message.edit_text(
            f"💳 *Оплата через CryptoBot*\n\n"
            f"💰 Сумма: {CRYPTO_PRICES['month']} USDT ≈ {rub}₽\n"
            f"📅 Тариф: 1 месяц Premium\n\n"
            f"🔗 *Нажмите кнопку ниже для оплаты:*\n\n"
            f"✅ После оплаты нажмите «Проверить оплату»",
            reply_markup=kb,
            parse_mode="Markdown"
        )
    else:
        await callback.message.edit_text(
            "❌ *Ошибка при создании счета*\n\n"
            "Попробуйте позже или выберите другой способ оплаты.",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="⭐ Оплатить Stars", callback_data="show_stars_prices")],
                [InlineKeyboardButton(text="🔙 Назад", callback_data="show_prices")]
            ]),
            parse_mode="Markdown"
        )
    await callback.answer()

@router.callback_query(F.data == "buy_crypto_year")
async def buy_crypto_year(callback: CallbackQuery):
    """Покупка Premium на 1 год через крипту"""
    await callback.message.edit_text(
        "⏳ *Создаю счет для оплаты...*",
        parse_mode="Markdown"
    )
    
    invoice = create_crypto_invoice(
        CRYPTO_PRICES["year"],
        "💎 BloomStyle Premium — 1 год",
        "crypto_year"
    )
    
    if invoice and invoice.get("pay_url"):
        user_invoices[callback.from_user.id] = {
            "invoice_id": invoice["invoice_id"],
            "amount": CRYPTO_PRICES["year"],
            "period": 365
        }
        
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="💳 Оплатить USDT", url=invoice["pay_url"])],
            [InlineKeyboardButton(text="✅ Проверить оплату", callback_data="check_crypto_payment")],
            [InlineKeyboardButton(text="⭐ Оплатить Stars", callback_data="show_stars_prices")],
            [InlineKeyboardButton(text="🔙 Назад", callback_data="show_prices")]
        ])
        
        rub = int(CRYPTO_PRICES["year"] * 95)
        savings = CRYPTO_PRICES["month"] * 12 - CRYPTO_PRICES["year"]
        await callback.message.edit_text(
            f"💳 *Оплата через CryptoBot*\n\n"
            f"💰 Сумма: {CRYPTO_PRICES['year']} USDT ≈ {rub}₽\n"
            f"📅 Тариф: 1 год Premium\n"
            f"✨ *Экономия: {savings:.2f} USDT*\n\n"
            f"🔗 *Нажмите кнопку ниже для оплаты:*\n\n"
            f"✅ После оплаты нажмите «Проверить оплату»",
            reply_markup=kb,
            parse_mode="Markdown"
        )
    else:
        await callback.message.edit_text(
            "❌ *Ошибка при создании счета*\n\n"
            "Попробуйте позже или выберите другой способ оплаты.",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="⭐ Оплатить Stars", callback_data="show_stars_prices")],
                [InlineKeyboardButton(text="🔙 Назад", callback_data="show_prices")]
            ]),
            parse_mode="Markdown"
        )
    await callback.answer()

@router.callback_query(F.data == "check_crypto_payment")
async def check_crypto_payment(callback: CallbackQuery):
    """Проверка статуса оплаты"""
    user_id = callback.from_user.id
    
    if user_id not in user_invoices:
        await callback.answer("❌ Счет не найден", show_alert=True)
        return
    
    invoice_data = user_invoices[user_id]
    status = check_invoice_status(invoice_data["invoice_id"])
    
    if status == "paid":
        # Активируем Premium
        activate_premium(user_id, invoice_data["period"])
        expiry = get_premium_expiry(user_id)
        
        # Удаляем данные счета
        del user_invoices[user_id]
        
        await callback.message.edit_text(
            f"🎉 *Оплата прошла успешно!*\n\n"
            f"💎 *BloomStyle Premium активирован*\n"
            f"📅 Действует до: {expiry.strftime('%d.%m.%Y')}\n\n"
            f"✨ Все Premium-функции уже доступны!",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="📊 Климатический дневник", callback_data="premium_climate")],
                [InlineKeyboardButton(text="🔙 В Premium", callback_data="back_to_premium")]
            ]),
            parse_mode="Markdown"
        )
        await callback.answer("✅ Premium активирован!")
    else:
        await callback.answer("⏳ Оплата ещё не получена. Попробуйте позже.", show_alert=True)