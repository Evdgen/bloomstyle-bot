from datetime import datetime, timedelta

# Список Premium-функций (БЕЗ AR-примерки)
PREMIUM_FEATURES = {
    "climate_diary": "📊 Климатический дневник",
    "virtual_cosmetics": "🧪 Виртуальная косметичка",
    "extended_stats": "📈 Расширенная статистика",
    "personal_looks": "🎨 Персональные образы",
    "product_analyzer": "🔬 Глубокий разбор составов"  # НОВАЯ ФУНКЦИЯ!
}

# Цены (для информации)
PREMIUM_PRICES = {
    "month": 149,
    "year": 990,
    "currency": "⭐"
}

# Хранилище Premium-пользователей
premium_users = {}

# Хранилище использовавших триал
trial_used = set()

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

def activate_trial(user_id):
    """Активация пробного периода (только 1 раз)"""
    if user_id in trial_used:
        return False, "Вы уже использовали пробный период!"
    
    trial_used.add(user_id)
    activate_premium(user_id, 2)
    return True, "Пробный период активирован на 2 дня!"

def has_used_trial(user_id):
    """Проверка, использовал ли пользователь триал"""
    return user_id in trial_used

def get_premium_features(user_id):
    """Получить список доступных функций"""
    if is_premium(user_id):
        return PREMIUM_FEATURES
    else:
        return {}  # Пустой словарь для обычных пользователей

def get_premium_expiry(user_id):
    """Получить дату истечения Premium"""
    if user_id in premium_users:
        return premium_users[user_id]
    return None