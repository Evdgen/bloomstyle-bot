import random

# ==================== БАЗА ПРОДУКТОВ ПО РЕГИОНАМ И БЮДЖЕТАМ ====================

PRODUCTS_DB = {
    # 🇷🇺 РОССИЯ (₽)
    "ru": {
        "budget": {  # до 1000₽
            "Сухость/шелушение": [
                {"name": "Cerave Moisturizing Cream", "price": 890, "mini_price": 390, "brand": "США", "link": "https://ozon.ru", "rating": 4.7},
                {"name": "The Ordinary Hyaluronic Acid 2%", "price": 750, "mini_price": None, "brand": "Канада", "link": "https://ozon.ru", "rating": 4.8},
                {"name": "Clean&Clear Увлажняющий", "price": 450, "mini_price": None, "brand": "Россия", "link": "https://wildberries.ru", "rating": 4.2},
                {"name": "Librederm Гиалурон", "price": 890, "mini_price": 350, "brand": "Россия", "link": "https://wildberries.ru", "rating": 4.5}
            ],
            "Жирный блеск/поры": [
                {"name": "The Ordinary Niacinamide 10%", "price": 750, "mini_price": None, "brand": "Канада", "link": "https://ozon.ru", "rating": 4.9},
                {"name": "Garnier Чистая Кожа", "price": 550, "mini_price": None, "brand": "Франция", "link": "https://wildberries.ru", "rating": 4.3},
                {"name": "Librederm Матирующий", "price": 890, "mini_price": 350, "brand": "Россия", "link": "https://wildberries.ru", "rating": 4.4},
                {"name": "La Roche-Posay Effaclar Micro", "price": 990, "mini_price": 390, "brand": "Франция", "link": "https://ozon.ru", "rating": 4.6}
            ],
            "Чувствительность/покраснения": [
                {"name": "La Roche-Posay Cicaplast B5", "price": 890, "mini_price": 350, "brand": "Франция", "link": "https://ozon.ru", "rating": 4.9},
                {"name": "Bioderma Sensibio", "price": 950, "mini_price": 390, "brand": "Франция", "link": "https://wildberries.ru", "rating": 4.7},
                {"name": "Avene Tolerance Control", "price": 990, "mini_price": 390, "brand": "Франция", "link": "https://ozon.ru", "rating": 4.6}
            ],
            "Увлажнение": [
                {"name": "Cerave Moisturizing Cream", "price": 890, "mini_price": 390, "brand": "США", "link": "https://ozon.ru", "rating": 4.7},
                {"name": "The Ordinary NMF", "price": 890, "mini_price": 390, "brand": "Канада", "link": "https://ozon.ru", "rating": 4.5},
                {"name": "Nivea Soft", "price": 350, "mini_price": None, "brand": "Германия", "link": "https://wildberries.ru", "rating": 4.3}
            ],
            "SPF-защита": [
                {"name": "Bioderma Photoderm SPF 30", "price": 990, "mini_price": 490, "brand": "Франция", "link": "https://ozon.ru", "rating": 4.7},
                {"name": "Garnier SPF 30", "price": 650, "mini_price": None, "brand": "Франция", "link": "https://wildberries.ru", "rating": 4.4},
                {"name": "Librederm SPF 30", "price": 890, "mini_price": 350, "brand": "Россия", "link": "https://wildberries.ru", "rating": 4.5}
            ]
        },
        "medium": {  # 1000-2500₽
            "Сухость/шелушение": [
                {"name": "La Roche-Posay Cicaplast B5", "price": 1850, "mini_price": 590, "brand": "Франция", "link": "https://ozon.ru", "rating": 4.9},
                {"name": "Avene Tolerance Control", "price": 2100, "mini_price": 690, "brand": "Франция", "link": "https://wildberries.ru", "rating": 4.8},
                {"name": "COSRX Snail Mucin", "price": 1650, "mini_price": None, "brand": "Корея", "link": "https://ozon.ru", "rating": 4.9},
                {"name": "Skin1004 Centella", "price": 1450, "mini_price": None, "brand": "Корея", "link": "https://ozon.ru", "rating": 4.8}
            ],
            "Жирный блеск/поры": [
                {"name": "La Roche-Posay Effaclar Duo+", "price": 1500, "mini_price": 590, "brand": "Франция", "link": "https://ozon.ru", "rating": 4.8},
                {"name": "COSRX BHA Power Liquid", "price": 1900, "mini_price": None, "brand": "Корея", "link": "https://ozon.ru", "rating": 4.7},
                {"name": "Isntree Green Tea", "price": 1700, "mini_price": None, "brand": "Корея", "link": "https://ozon.ru", "rating": 4.6}
            ],
            "SPF-защита": [
                {"name": "La Roche-Posay Anthelios SPF 50", "price": 1850, "mini_price": 590, "brand": "Франция", "link": "https://ozon.ru", "rating": 4.9},
                {"name": "Beauty of Joseon SPF 50", "price": 1600, "mini_price": None, "brand": "Корея", "link": "https://ozon.ru", "rating": 4.9},
                {"name": "COSRX Aloe SPF 50", "price": 1400, "mini_price": None, "brand": "Корея", "link": "https://ozon.ru", "rating": 4.7}
            ]
        },
        "premium": {  # 2500+₽
            "Сухость/шелушение": [
                {"name": "Skinceuticals HA Intensifier", "price": 8900, "mini_price": 2900, "brand": "США", "link": "https://ozon.ru", "rating": 4.9},
                {"name": "Estée Lauder Advanced Night Repair", "price": 7500, "mini_price": 2500, "brand": "США", "link": "https://ozon.ru", "rating": 4.9},
                {"name": "Clarins Hydra-Essentiel", "price": 3800, "mini_price": 1200, "brand": "Франция", "link": "https://wildberries.ru", "rating": 4.7}
            ],
            "SPF-защита": [
                {"name": "Shiseido Expert Sun Protector", "price": 3800, "mini_price": 1200, "brand": "Япония", "link": "https://ozon.ru", "rating": 4.8},
                {"name": "Supergoop! Play SPF 50", "price": 3200, "mini_price": None, "brand": "США", "link": "https://ozon.ru", "rating": 4.7}
            ]
        }
    },
    
    # 🇰🇷 КОРЕЯ (₩)
    "kr": {
        "budget": {
            "Сухость/шелушение": [
                {"name": "COSRX Snail Mucin", "price": 22000, "mini_price": 8000, "brand": "Корея", "link": "https://yesstyle.com", "rating": 4.9},
                {"name": "Isntree Hyaluronic Acid", "price": 18000, "mini_price": None, "brand": "Корея", "link": "https://yesstyle.com", "rating": 4.8}
            ]
        },
        "medium": {
            "SPF-защита": [
                {"name": "Beauty of Joseon SPF 50", "price": 16000, "mini_price": None, "brand": "Корея", "link": "https://yesstyle.com", "rating": 4.9},
                {"name": "COSRX Aloe SPF 50", "price": 14000, "mini_price": None, "brand": "Корея", "link": "https://yesstyle.com", "rating": 4.7}
            ]
        }
    },
    
    # 🇺🇸 США ($)
    "us": {
        "budget": {
            "Сухость/шелушение": [
                {"name": "CeraVe Moisturizing Cream", "price": 18, "mini_price": 6, "brand": "США", "link": "https://amazon.com", "rating": 4.8},
                {"name": "The Ordinary Hyaluronic Acid", "price": 9, "mini_price": None, "brand": "Канада", "link": "https://amazon.com", "rating": 4.7}
            ]
        }
    },
    
    # 🇪🇺 ЕВРОПА (€)
    "eu": {
        "budget": {
            "Сухость/шелушение": [
                {"name": "CeraVe Moisturizing Cream", "price": 16, "mini_price": 5, "brand": "США", "link": "https://lookfantastic.com", "rating": 4.8},
                {"name": "La Roche-Posay Cicaplast", "price": 15, "mini_price": 5, "brand": "Франция", "link": "https://lookfantastic.com", "rating": 4.9}
            ]
        }
    },
    
    # 🇯🇵 ЯПОНИЯ (¥)
    "jp": {
        "budget": {
            "Сухость/шелушение": [
                {"name": "Hada Labo Gokujyun", "price": 1500, "mini_price": None, "brand": "Япония", "link": "https://amazon.co.jp", "rating": 4.8},
                {"name": "Skin Aqua SPF", "price": 1200, "mini_price": None, "brand": "Япония", "link": "https://amazon.co.jp", "rating": 4.7}
            ]
        }
    }
}

# ==================== КОНВЕРТАЦИЯ ВАЛЮТ ====================

CURRENCIES = {
    "ru": "₽",
    "kr": "₩", 
    "eu": "€",
    "us": "$",
    "jp": "¥"
}

BUDGET_LEVELS = {
    "budget": "До 1000₽ / 30$ / 25€",
    "medium": "1000-2500₽ / 30-50$ / 25-45€",
    "premium": "2500₽+ / 50$+ / 45€+"
}

# ==================== ПРОФИЛЬ ПОЛЬЗОВАТЕЛЯ (ВРЕМЕННО) ====================

# В реальном проекте замени на БД
user_settings = {}

def set_user_region(user_id, region):
    """Установить регион пользователя"""
    if user_id not in user_settings:
        user_settings[user_id] = {}
    user_settings[user_id]['region'] = region

def set_user_budget(user_id, budget_level):
    """Установить бюджет пользователя"""
    if user_id not in user_settings:
        user_settings[user_id] = {}
    user_settings[user_id]['budget'] = budget_level

def get_user_region(user_id):
    """Получить регион пользователя"""
    return user_settings.get(user_id, {}).get('region', 'ru')

def get_user_budget(user_id):
    """Получить бюджет пользователя"""
    return user_settings.get(user_id, {}).get('budget', 'medium')

# ==================== ОСНОВНЫЕ ФУНКЦИИ ПОДБОРА ====================

def get_products_by_problem(problem, user_id=None, region=None, budget_level=None):
    """
    Получить продукты по проблеме с учётом региона и бюджета
    """
    # Определяем регион и бюджет
    if user_id:
        region = region or get_user_region(user_id)
        budget_level = budget_level or get_user_budget(user_id)
    else:
        region = region or 'ru'
        budget_level = budget_level or 'medium'
    
    # Получаем продукты для региона
    region_data = PRODUCTS_DB.get(region, PRODUCTS_DB['ru'])
    budget_data = region_data.get(budget_level, region_data['medium'])
    products = budget_data.get(problem, [])
    
    # Если в выбранном бюджете нет продуктов, берём из среднего
    if not products and budget_level != 'medium':
        budget_data = region_data.get('medium', {})
        products = budget_data.get(problem, [])
    
    # Если всё ещё нет, берём из любого доступного
    if not products:
        for level in ['budget', 'medium', 'premium']:
            if level in region_data:
                products = region_data[level].get(problem, [])
                if products:
                    break
    
    # Перемешиваем для разнообразия
    if products:
        random.shuffle(products)
        # Возвращаем максимум 3 продукта
        return products[:3]
    
    return []

def get_products_by_budget(problem, budget_level, region='ru'):
    """Получить продукты по конкретному бюджету"""
    region_data = PRODUCTS_DB.get(region, PRODUCTS_DB['ru'])
    budget_data = region_data.get(budget_level, {})
    return budget_data.get(problem, [])

# ==================== ФОРМАТИРОВАНИЕ ОТВЕТА ====================

def format_products(problem, products, region='ru'):
    """
    Отформатировать список продуктов в красивый ответ
    """
    if not products:
        return f"❌ По запросу «{problem}» ничего не найдено.\n\nПопробуйте изменить бюджет или регион."
    
    currency = CURRENCIES.get(region, '₽')
    
    text = f"🎯 *{problem}:*\n\n"
    
    for i, p in enumerate(products, 1):
        text += f"{i}. **{p['name']}**\n"
        text += f"   ✨ {p['brand']} | ⭐ {p.get('rating', '4.5')}\n"
        text += f"   📝 {p.get('description', 'Увлажнение и восстановление')}\n"
        text += f"   💰 {p['price']}{currency}"
        
        if p.get('mini_price'):
            text += f" | 🧪 Мини {p['mini_price']}{currency}"
        
        text += f"\n   [🛒 КУПИТЬ]({p['link']})\n\n"
    
    text += "❗ *Перед использованием нового средства сделайте патч-тест*"
    
    return text

def format_budget_info(region='ru'):
    """Информация о бюджетах для региона"""
    currency = CURRENCIES.get(region, '₽')
    
    text = f"💰 *Доступные бюджеты для региона {region.upper()}:*\n\n"
    
    if region == 'ru':
        text += "• 💸 Бюджет: до 1000₽\n"
        text += "• 💳 Средний: 1000-2500₽\n"
        text += "• 💎 Премиум: 2500₽+\n"
    elif region == 'us':
        text += "• 💸 Бюджет: до 30$\n"
        text += "• 💳 Средний: 30-50$\n"
        text += "• 💎 Премиум: 50$+\n"
    elif region == 'eu':
        text += "• 💸 Бюджет: до 25€\n"
        text += "• 💳 Средний: 25-45€\n"
        text += "• 💎 Премиум: 45€+\n"
    elif region == 'kr':
        text += "• 💸 Бюджет: до 30000₩\n"
        text += "• 💳 Средний: 30000-50000₩\n"
        text += "• 💎 Премиум: 50000₩+\n"
    elif region == 'jp':
        text += "• 💸 Бюджет: до 3000¥\n"
        text += "• 💳 Средний: 3000-5000¥\n"
        text += "• 💎 Премиум: 5000¥+\n"
    
    return text

# ==================== РЕКОМЕНДАЦИИ ПОД КЛИМАТ ====================

def get_climate_recommendation(humidity, wind_speed, skin_type='combination'):
    """Рекомендация на основе климата"""
    if humidity < 40:
        return {
            "advice": "💧 Низкая влажность — используйте гиалуроновую кислоту на влажную кожу",
            "products": ["Гиалуроновая сыворотка", "Крем с церамедами", "SPF защита"]
        }
    elif humidity > 70:
        return {
            "advice": "💦 Высокая влажность — выбирайте лёгкие гели и эмульсии",
            "products": ["Гель для умывания", "Лёгкий увлажняющий крем", "Матирующий SPF"]
        }
    elif wind_speed > 5:
        return {
            "advice": "🌬️ Сильный ветер — защищайте кожу плотным кремом и SPF",
            "products": ["Восстанавливающий крем", "SPF 30+", "Термальная вода"]
        }
    else:
        return {
            "advice": "✅ Сегодня кожа в безопасности — поддерживайте обычный уход",
            "products": ["Мягкое очищение", "Увлажняющий крем", "SPF"]
        }

# ==================== ТОП-ПРОДУКТЫ ====================

def get_top_products(category, region='ru'):
    """Топ-3 продукта в категории"""
    all_products = []
    region_data = PRODUCTS_DB.get(region, PRODUCTS_DB['ru'])
    
    for budget_level in ['budget', 'medium', 'premium']:
        if budget_level in region_data:
            products = region_data[budget_level].get(category, [])
            all_products.extend(products)
    
    # Сортируем по рейтингу
    all_products.sort(key=lambda x: x.get('rating', 0), reverse=True)
    
    return all_products[:3]