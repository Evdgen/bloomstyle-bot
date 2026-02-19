import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

# Типы кожи
SKIN_TYPES = {
    "dry": "Сухая",
    "oily": "Жирная",
    "combination": "Комбинированная",
    "normal": "Нормальная",
    "sensitive": "Чувствительная"
}

# Бюджетные сегменты
BUDGETS = {
    "budget": "До 500₽",
    "medium": "500-1500₽",
    "premium": "1500-3000₽",
    "luxury": "От 3000₽"
}

# Реактивность кожи
REACTIVITY = {
    "stable": "Устойчивая",
    "sensitive": "Чувствительная",
    "allergic": "Аллергичная"
}