from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def main_menu():
    """Главное меню с 4 разделами + специальная кнопка"""
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="🌱 BLOOM — Уход"),
                KeyboardButton(text="💄 STYLE — Макияж и стиль")
            ],
            [
                KeyboardButton(text="📚 ЗНАНИЯ и новости"),
                KeyboardButton(text="⚙️ НАСТРОЙКИ и Premium")
            ],
            [
                KeyboardButton(text="🎁 SPECIAL FOR КИРИЛЛ")  # НОВАЯ КНОПКА
            ]
        ],
        resize_keyboard=True,
        input_field_placeholder="Выберите раздел..."
    )
    return kb

def bloom_menu():
    """Меню раздела BLOOM"""
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="📅 Уход на сегодня"),
                KeyboardButton(text="🔍 Подобрать средство")
            ],
            [
                KeyboardButton(text="📊 Климат-отчёт"),
                KeyboardButton(text="✈️ Уход в путешествиях")
            ],
            [
                KeyboardButton(text="🔙 В главное меню")
            ]
        ],
        resize_keyboard=True,
        input_field_placeholder="Выберите действие..."
    )
    return kb

def style_menu():
    """Меню раздела STYLE"""
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="🎭 Макияж на случай"),
                KeyboardButton(text="🧬 Определить тип кожи")
            ],
            [
                KeyboardButton(text="🎨 Определить цветотип"),
                KeyboardButton(text="📐 Определить форму лица")
            ],
            [
                KeyboardButton(text="🌟 Гороскоп красоты"),
                KeyboardButton(text="🎁 Сюрприз дня")
            ],
            [
                KeyboardButton(text="📋 Трекер привычек"),
                KeyboardButton(text="👗 Мои образы")
            ],
            [
                KeyboardButton(text="🔙 В главное меню")
            ]
        ],
        resize_keyboard=True,
        input_field_placeholder="Выберите действие..."
    )
    return kb

def knowledge_menu():
    """Меню раздела ЗНАНИЯ"""
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="🧪 База компонентов"),
                KeyboardButton(text="🔬 Разбор составов")
            ],
            [
                KeyboardButton(text="📰 Каналы BloomStyle"),
                KeyboardButton(text="🏆 Челленджи")
            ],
            [
                KeyboardButton(text="🔙 В главное меню")
            ]
        ],
        resize_keyboard=True,
        input_field_placeholder="Выберите действие..."
    )
    return kb

def settings_menu():
    """Меню раздела НАСТРОЙКИ"""
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="👤 Мой профиль"),
                KeyboardButton(text="💎 BloomStyle Premium")
            ],
            [
                KeyboardButton(text="🧬 Изменить тип кожи"),
                KeyboardButton(text="💰 Изменить бюджет")
            ],
            [
                KeyboardButton(text="📍 Изменить город"),
                KeyboardButton(text="❓ Помощь и безопасность")
            ],
            [
                KeyboardButton(text="🔙 В главное меню")
            ]
        ],
        resize_keyboard=True,
        input_field_placeholder="Выберите действие..."
    )
    return kb

def product_search_menu():
    """Меню поиска средств"""
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="💧 Сухость/шелушение"),
                KeyboardButton(text="🔥 Жирный блеск/поры")
            ],
            [
                KeyboardButton(text="🌡️ Чувствительность/покраснения"),
                KeyboardButton(text="🧴 Увлажнение")
            ],
            [
                KeyboardButton(text="🛡️ SPF-защита"),
                KeyboardButton(text="🔙 В меню BLOOM")
            ]
        ],
        resize_keyboard=True,
        input_field_placeholder="Выберите проблему..."
    )
    return kb

def travel_menu():
    """Меню путешествий"""
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="🏖️ Тропики/пляж"),
                KeyboardButton(text="🏔️ Горы/холод")
            ],
            [
                KeyboardButton(text="🏙️ Городской тур"),
                KeyboardButton(text="🔙 В меню BLOOM")
            ]
        ],
        resize_keyboard=True,
        input_field_placeholder="Выберите направление..."
    )
    return kb

def makeup_scene_menu():
    """Меню сценариев макияжа"""
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="🏢 Офисный день"),
                KeyboardButton(text="💕 Свидание/вечеринка")
            ],
            [
                KeyboardButton(text="✈️ Путешествие/дорога"),
                KeyboardButton(text="🌧️ Плохая погода")
            ],
            [
                KeyboardButton(text="🔙 В меню STYLE")
            ]
        ],
        resize_keyboard=True,
        input_field_placeholder="Выберите сценарий..."
    )
    return kb

def budget_menu():
    """Меню выбора бюджета"""
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="💸 Бюджетный (до 1000₽)"),
                KeyboardButton(text="💳 Средний (1000-2500₽)")
            ],
            [
                KeyboardButton(text="💎 Премиум (2500₽+)"),
                KeyboardButton(text="🔙 В главное меню")
            ]
        ],
        resize_keyboard=True,
        input_field_placeholder="Выберите ваш бюджет..."
    )
    return kb

def skin_type_menu():
    """Меню выбора типа кожи"""
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="💧 Сухая"),
                KeyboardButton(text="🔥 Жирная")
            ],
            [
                KeyboardButton(text="🌓 Комбинированная"),
                KeyboardButton(text="⚖️ Нормальная")
            ],
            [
                KeyboardButton(text="🌡️ Чувствительная"),
                KeyboardButton(text="🔙 В главное меню")
            ]
        ],
        resize_keyboard=True,
        input_field_placeholder="Выберите тип кожи..."
    )
    return kb