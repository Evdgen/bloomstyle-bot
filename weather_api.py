import requests
import random

# Конфигурация
WEATHER_API_KEY = "2029abc0c8a7a49cc7c1be46405edfb4"
GEO_URL = "http://api.openweathermap.org/geo/1.0/reverse"
WEATHER_URL = "http://api.openweathermap.org/data/2.5/weather"

# ==================== ОПРЕДЕЛЕНИЕ ГОРОДА ====================

def get_city_by_coords(lat, lon):
    """Определяем город по координатам"""
    try:
        url = f"{GEO_URL}?lat={lat}&lon={lon}&limit=1&appid={WEATHER_API_KEY}"
        response = requests.get(url, timeout=5).json()
        
        if response and len(response) > 0:
            city_ru = response[0].get('local_names', {}).get('ru')
            if city_ru:
                return city_ru
            return response[0].get('name', 'Москва')
    except:
        pass
    
    # Примерное определение по координатам
    if 55.5 < lat < 60.0 and 29.5 < lon < 31.5:
        return "Санкт-Петербург"
    elif 55.5 < lat < 56.0 and 37.0 < lon < 38.0:
        return "Москва"
    elif 43.0 < lat < 44.0 and 39.0 < lon < 40.0:
        return "Сочи"
    
    return "Санкт-Петербург"

# ==================== ПОЛУЧЕНИЕ ПОГОДЫ ====================

def get_weather(city_name):
    """Получить погоду для города"""
    try:
        url = f"{WEATHER_URL}?q={city_name}&appid={WEATHER_API_KEY}&units=metric&lang=ru"
        response = requests.get(url, timeout=5).json()
        
        if response.get("cod") == 200:
            return {
                "city": response["name"],
                "temp": round(response["main"]["temp"]),
                "humidity": response["main"]["humidity"],
                "wind_speed": round(response["wind"]["speed"]),
                "description": response["weather"][0]["description"]
            }
        else:
            return get_test_weather(city_name)
    except:
        return get_test_weather(city_name)

# ==================== ТЕСТОВЫЕ ДАННЫЕ ====================

def get_test_weather(city_name):
    """Тестовые данные для любого города"""
    test_data = {
        "москва": {"temp": 12, "humidity": 30, "wind": 5, "desc": "облачно"},
        "санкт-петербург": {"temp": 10, "humidity": 45, "wind": 4, "desc": "дождливо"},
        "сочи": {"temp": 18, "humidity": 70, "wind": 3, "desc": "солнечно"},
        "казань": {"temp": 11, "humidity": 35, "wind": 4, "desc": "облачно"},
        "новосибирск": {"temp": 8, "humidity": 40, "wind": 6, "desc": "ветрено"},
        "екатеринбург": {"temp": 9, "humidity": 38, "wind": 5, "desc": "пасмурно"},
    }
    
    city_lower = city_name.lower().strip()
    if city_lower in test_data:
        data = test_data[city_lower]
        return {
            "city": city_name.capitalize(),
            "temp": data["temp"],
            "humidity": data["humidity"],
            "wind_speed": data["wind"],
            "description": data["desc"]
        }
    else:
        return {
            "city": city_name.capitalize(),
            "temp": random.randint(-5, 25),
            "humidity": random.randint(30, 80),
            "wind_speed": random.randint(1, 8),
            "description": random.choice(["солнечно", "облачно", "пасмурно", "ветрено"])
        }

# ==================== АНАЛИЗ РИСКОВ ====================

def get_weather_risks(humidity, wind_speed, skin_type="combination", reactivity="sensitive"):
    """Анализ рисков для кожи"""
    risks = []
    
    if humidity < 40:
        risks.append("💧 **Обезвоживание** — влажность ниже 40%")
        risks.append("   → Наносите гиалуронку на ВЛАЖНУЮ кожу")
    elif humidity > 70:
        risks.append("💦 **Высокая влажность** — риск забитых пор")
        risks.append("   → Выбирайте лёгкие гели")
    
    if wind_speed > 5:
        risks.append("🌬️ **Сильный ветер** — возможны покраснения")
        risks.append("   → Используйте SPF для защиты")
    
    if not risks:
        risks.append("✅ Сегодня кожа в безопасности")
    
    return risks

# ==================== УТРЕННЯЯ РУТИНА ====================

def get_morning_routine(weather, skin_type="combination"):
    """Утренняя рутина с учётом погоды"""
    humidity = weather["humidity"]
    wind = weather["wind_speed"]
    
    text = f"🌅 *УТРЕННЯЯ РУТИНА*\n\n"
    text += f"📍 {weather['city']} | 🌡️ {weather['temp']}°C | 💧 {humidity}% | 🌬️ {wind} м/с\n\n"
    
    # Очищение
    if humidity < 40 or skin_type in ["dry", "sensitive"]:
        text += "1. **Очищение:** *Cerave Hydrating Cleanser*\n"
        text += "   ✅ Без SLS, не сушит\n"
        text += "   🧪 Мини 50 мл: 450₽ | [КУПИТЬ](https://ozon.ru)\n\n"
    else:
        text += "1. **Очищение:** *La Roche-Posay Effaclar Gel*\n"
        text += "   ✅ Матирует, не пересушивает\n"
        text += "   🧪 Мини 50 мл: 590₽ | [КУПИТЬ](https://ozon.ru)\n\n"
    
    # Сыворотка
    if humidity < 40:
        text += "2. **Сыворотка:** *The Ordinary Hyaluronic Acid 2% + B5*\n"
        text += "   ⚠️ Наносить на ВЛАЖНУЮ кожу!\n"
        text += "   💰 750₽ | [КУПИТЬ](https://ozon.ru)\n\n"
    else:
        text += "2. **Сыворотка:** *The Ordinary Niacinamide 10% + Zinc*\n"
        text += "   ✅ Матирует, сужает поры\n"
        text += "   💰 750₽ | [КУПИТЬ](https://ozon.ru)\n\n"
    
    # Защита/увлажнение
    if wind > 5:
        text += "3. **Защита:** *La Roche-Posay Anthelios SPF 30*\n"
        text += "   🛡️ Защищает от ветра и UVA/UVB\n"
        text += "   🧪 Мини 15 мл: 590₽ | [КУПИТЬ](https://ozon.ru)\n"
    else:
        text += "3. **Увлажнение:** *Cerave Moisturizing Cream*\n"
        text += "   💧 Базовый уход с церамедами\n"
        text += "   🧪 Мини 15 мл: 390₽ | [КУПИТЬ](https://ozon.ru)\n"
    
    return text

# ==================== ВЕЧЕРНЯЯ РУТИНА ====================

def get_evening_routine(weather, skin_type="combination"):
    """Вечерняя рутина, которая МЕНЯЕТСЯ под погоду"""
    humidity = weather["humidity"]
    wind = weather["wind_speed"]
    
    text = f"🌃 *ВЕЧЕРНЯЯ РУТИНА*\n\n"
    text += f"📍 {weather['city']} | 🌡️ {weather['temp']}°C | 💧 {humidity}% | 🌬️ {wind} м/с\n\n"
    
    # Двойное очищение — всегда
    text += "1. **Двойное очищение:**\n"
    text += "   • *Bioderma Sensibio H2O* — мицеллярная вода\n"
    text += "   • *Cerave Hydrating Cleanser* — мягкий гель\n"
    text += "   🧪 Набор мини: 890₽ | [КУПИТЬ](https://ozon.ru)\n\n"
    
    # Восстановление — ЗАВИСИТ ОТ ПОГОДЫ!
    if wind > 5:
        text += "2. **Интенсивное восстановление:**\n"
        text += "   • *La Roche-Posay Cicaplast Baume B5*\n"
        text += "   ✅ Пантенол + мадекассосид — заживляет микроповреждения от ветра\n"
        text += "   🧪 Мини 15 мл: 350₽ | [КУПИТЬ](https://ozon.ru)\n\n"
    elif humidity < 40:
        text += "2. **Глубокое увлажнение:**\n"
        text += "   • *Cerave Moisturizing Cream*\n"
        text += "   ✅ Церамиды + гиалуроновая кислота — восстанавливает барьер\n"
        text += "   🧪 Мини 15 мл: 390₽ | [КУПИТЬ](https://ozon.ru)\n\n"
    elif humidity > 70:
        text += "2. **Лёгкое восстановление:**\n"
        text += "   • *COSRX Snail Mucin 96*\n"
        text += "   ✅ Эссенция с муцином улитки — увлажняет без утяжеления\n"
        text += "   💰 1650₽ | [КУПИТЬ](https://ozon.ru)\n\n"
    else:
        # Рандомный выбор из нескольких вариантов
        options = [
            ("*The Ordinary Natural Moisturizing Factors*", "Ежедневный увлажняющий крем", "890₽"),
            ("*COSRX Oil-Free Ultra-Moisturizing Lotion*", "Лёгкая эмульсия с березовым соком", "1950₽"),
            ("*Avene Tolerance Control Soothing Skin Recovery Cream*", "Успокаивающий крем", "2100₽")
        ]
        choice = random.choice(options)
        text += f"2. **Восстановление:** {choice[0]}\n"
        text += f"   ✅ {choice[1]}\n"
        text += f"   💰 {choice[2]} | [КУПИТЬ](https://ozon.ru)\n\n"
    
    # Активные компоненты (чередуются)
    actives = [
        "• *The Ordinary Granactive Retinoid 2% Emulsion* — обновление клеток (2-3 раза/неделю)",
        "• *The Ordinary AHA 30% + BHA 2% Peeling Solution* — пилинг-маска (1 раз/неделю)",
        "• *The Ordinary Vitamin C Suspension 23% + HA Spheres 2%* — осветление (утром)",
        "• *Paula's Choice 2% BHA Liquid Exfoliant* — салициловая кислота для пор (вечер)"
    ]
    text += "3. *Активные компоненты (по необходимости):*\n"
    text += f"   {random.choice(actives)}\n"
    
    return text