# database.py — полное хранилище данных пользователей

from datetime import datetime

# Словарь для хранения данных пользователей
# { user_id: {
#     "city": "Санкт-Петербург",
#     "skin_type": "combination",
#     "budget": "medium",
#     "colortype": "summer",
#     "face_shape": "oval",
#     "zodiac": "овен",
#     "registered_date": "2024-01-01",
#     "routines_saved": 0,
#     "money_saved": 0
# } }
users_db = {}

# ==================== ГОРОД ====================

def set_user_city(user_id, city):
    """Сохранить город пользователя"""
    if user_id not in users_db:
        users_db[user_id] = {}
    users_db[user_id]["city"] = city
    print(f"✅ Город для пользователя {user_id}: {city}")
    return True

def get_user_city(user_id):
    """Получить город пользователя"""
    if user_id in users_db and "city" in users_db[user_id]:
        return users_db[user_id]["city"]
    return None

# ==================== ТИП КОЖИ ====================

def set_user_skin_type(user_id, skin_type):
    """Сохранить тип кожи"""
    if user_id not in users_db:
        users_db[user_id] = {}
    users_db[user_id]["skin_type"] = skin_type
    print(f"🧬 Тип кожи для пользователя {user_id}: {skin_type}")
    return True

def get_user_skin_type(user_id):
    """Получить тип кожи"""
    if user_id in users_db and "skin_type" in users_db[user_id]:
        return users_db[user_id]["skin_type"]
    return "combination"  # По умолчанию

# ==================== БЮДЖЕТ ====================

def set_user_budget(user_id, budget):
    """Сохранить бюджет пользователя"""
    if user_id not in users_db:
        users_db[user_id] = {}
    users_db[user_id]["budget"] = budget
    print(f"💰 Бюджет для пользователя {user_id}: {budget}")
    return True

def get_user_budget(user_id):
    """Получить бюджет пользователя"""
    if user_id in users_db and "budget" in users_db[user_id]:
        return users_db[user_id]["budget"]
    return "medium"  # По умолчанию

# ==================== ЦВЕТОТИП ====================

def set_user_colortype(user_id, colortype):
    """Сохранить цветотип пользователя"""
    if user_id not in users_db:
        users_db[user_id] = {}
    users_db[user_id]["colortype"] = colortype
    print(f"🎨 Цветотип для пользователя {user_id}: {colortype}")
    return True

def get_user_colortype(user_id):
    """Получить цветотип пользователя"""
    if user_id in users_db and "colortype" in users_db[user_id]:
        return users_db[user_id]["colortype"]
    return None

# ==================== ФОРМА ЛИЦА ====================

def set_user_face_shape(user_id, face_shape):
    """Сохранить форму лица пользователя"""
    if user_id not in users_db:
        users_db[user_id] = {}
    users_db[user_id]["face_shape"] = face_shape
    print(f"📐 Форма лица для пользователя {user_id}: {face_shape}")
    return True

def get_user_face_shape(user_id):
    """Получить форму лица пользователя"""
    if user_id in users_db and "face_shape" in users_db[user_id]:
        return users_db[user_id]["face_shape"]
    return None

# ==================== ЗНАК ЗОДИАКА ====================

def set_user_zodiac(user_id, zodiac):
    """Сохранить знак зодиака пользователя"""
    if user_id not in users_db:
        users_db[user_id] = {}
    users_db[user_id]["zodiac"] = zodiac
    print(f"🌟 Знак зодиака для пользователя {user_id}: {zodiac}")
    return True

def get_user_zodiac(user_id):
    """Получить знак зодиака пользователя"""
    if user_id in users_db and "zodiac" in users_db[user_id]:
        return users_db[user_id]["zodiac"]
    return None

# ==================== СТАТИСТИКА ====================

def init_user_stats(user_id):
    """Инициализировать статистику пользователя"""
    if user_id not in users_db:
        users_db[user_id] = {}
    
    if "registered_date" not in users_db[user_id]:
        users_db[user_id]["registered_date"] = datetime.now().strftime("%d.%m.%Y")
    
    if "routines_saved" not in users_db[user_id]:
        users_db[user_id]["routines_saved"] = 0
    
    if "money_saved" not in users_db[user_id]:
        users_db[user_id]["money_saved"] = 0
    
    return True

def increment_routines_saved(user_id, amount=1):
    """Увеличить счетчик сохраненных рутин"""
    if user_id not in users_db:
        users_db[user_id] = {}
    if "routines_saved" not in users_db[user_id]:
        users_db[user_id]["routines_saved"] = 0
    users_db[user_id]["routines_saved"] += amount

def increment_money_saved(user_id, amount):
    """Увеличить счетчик сэкономленных денег"""
    if user_id not in users_db:
        users_db[user_id] = {}
    if "money_saved" not in users_db[user_id]:
        users_db[user_id]["money_saved"] = 0
    users_db[user_id]["money_saved"] += amount

def get_user_stats(user_id):
    """Получить статистику пользователя"""
    if user_id not in users_db:
        users_db[user_id] = {}
    
    days_active = 0
    if "registered_date" in users_db[user_id]:
        try:
            reg_date = datetime.strptime(users_db[user_id]["registered_date"], "%d.%m.%Y")
            days_active = (datetime.now() - reg_date).days
        except:
            days_active = 1
    else:
        users_db[user_id]["registered_date"] = datetime.now().strftime("%d.%m.%Y")
        days_active = 0
    
    return {
        "registered_date": users_db[user_id].get("registered_date", datetime.now().strftime("%d.%m.%Y")),
        "days_active": days_active,
        "routines_saved": users_db[user_id].get("routines_saved", 0),
        "money_saved": users_db[user_id].get("money_saved", 0)
    }

# ==================== ПОЛНЫЙ ПРОФИЛЬ ====================

def get_full_profile(user_id):
    """Получить полный профиль пользователя"""
    if user_id not in users_db:
        users_db[user_id] = {}
    
    profile = users_db[user_id]
    
    # Город
    city_text = profile.get("city", "❌ не определён")
    
    # Бюджет с человеко-читаемым названием
    budget_text = "Средний (1000-2500₽)"
    if profile.get("budget") == "budget":
        budget_text = "Бюджетный (до 1000₽)"
    elif profile.get("budget") == "premium":
        budget_text = "Премиум (2500₽+)"
    
    # Тип кожи с человеко-читаемым названием
    skin_text = "Комбинированная"
    if profile.get("skin_type") == "dry":
        skin_text = "Сухая"
    elif profile.get("skin_type") == "oily":
        skin_text = "Жирная"
    elif profile.get("skin_type") == "normal":
        skin_text = "Нормальная"
    elif profile.get("skin_type") == "sensitive":
        skin_text = "Чувствительная"
    
    # Цветотип с человеко-читаемым названием
    colortype_text = "❌ не определён"
    if profile.get("colortype") == "winter":
        colortype_text = "❄️ Холодная Зима"
    elif profile.get("colortype") == "summer":
        colortype_text = "🌸 Холодное Лето"
    elif profile.get("colortype") == "spring":
        colortype_text = "🌼 Теплая Весна"
    elif profile.get("colortype") == "autumn":
        colortype_text = "🍂 Теплая Осень"
    
    # Форма лица с человеко-читаемым названием
    face_text = "❌ не определена"
    if profile.get("face_shape") == "oval":
        face_text = "✨ Овальное лицо"
    elif profile.get("face_shape") == "round":
        face_text = "🟡 Круглое лицо"
    elif profile.get("face_shape") == "square":
        face_text = "🔲 Квадратное лицо"
    elif profile.get("face_shape") == "heart":
        face_text = "❤️ Сердцевидное лицо"
    elif profile.get("face_shape") == "rectangle":
        face_text = "📏 Прямоугольное лицо"
    
    # Знак зодиака
    zodiac_text = "❌ не определён"
    zodiac_map = {
        "овен": "♈ Овен", "телец": "♉ Телец", "близнецы": "♊ Близнецы",
        "рак": "♋ Рак", "лев": "♌ Лев", "дева": "♍ Дева",
        "весы": "♎ Весы", "скорпион": "♏ Скорпион", "стрелец": "♐ Стрелец",
        "козерог": "♑ Козерог", "водолей": "♒ Водолей", "рыбы": "♓ Рыбы"
    }
    if profile.get("zodiac") in zodiac_map:
        zodiac_text = zodiac_map[profile["zodiac"]]
    
    stats = get_user_stats(user_id)
    
    return {
        "city": city_text,
        "skin_type": skin_text,
        "budget": budget_text,
        "colortype": colortype_text,
        "face_shape": face_text,
        "zodiac": zodiac_text,
        "days_active": stats["days_active"],
        "routines_saved": stats["routines_saved"],
        "money_saved": stats["money_saved"]
    }

def get_all_users():
    """Получить всех пользователей (для отладки)"""
    return users_db