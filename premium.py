from datetime import datetime, timedelta

# Список Premium-функций
PREMIUM_FEATURES = {
    "climate_diary": "📊 Климатический дневник",
    "virtual_cosmetics": "🧪 Виртуальная косметичка",
    "ar_makeup": "📸 AR-примерка макияжа",
    "extended_stats": "📈 Расширенная статистика",
    "personal_looks": "🎨 Персональные образы"
}

# Цены (для информации)
PREMIUM_PRICES = {
    "month": 149,
    "year": 990,
    "currency": "⭐"
}

# Хранилище Premium-пользователей
premium_users = {}

def is_premium(user_id):
    """Проверка, есть ли у пользователя Premium"""
    if user_id not in premium_users:
        return False
    expiry = premium_users.get(user_id)
    return expiry and datetime.now() < expiry

def activate_premium(user_id, days=30):
    """Активация Premium на N дней"""
    expiry = datetime.now() + timedelta(days=days)
    premium_users[user_id] = expiry
    print(f"💎 Premium активирован для {user_id} до {expiry.strftime('%d.%m.%Y')}")
    return expiry

def get_premium_features(user_id):
    """Получить список доступных функций"""
    if is_premium(user_id):
        return PREMIUM_FEATURES
    else:
        return {
            "climate_diary": "📊 Климатический дневник (базовая версия)",
            "personal_looks": "🎨 Базовые образы"
        }

def get_premium_expiry(user_id):
    """Получить дату истечения Premium"""
    if user_id in premium_users:
        return premium_users[user_id]
    return None