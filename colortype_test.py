# colortype_test.py — тест на определение цветотипа

import random

# Вопросы для теста
COLORTYPE_QUESTIONS = [
    {
        "question": "1/8. Какой у вас натуральный цвет волос?",
        "options": {
            "❄️ Пепельный блонд, платиновый": "winter",
            "🌾 Пшеничный, золотистый блонд": "spring",
            "🍂 Рыжий, медовый, каштановый": "autumn",
            "🌑 Русый, пепельный шатен": "summer",
            "🖤 Черный, темный шатен": "winter"
        }
    },
    {
        "question": "2/8. Какой у вас цвет глаз?",
        "options": {
            "💙 Ярко-синие, серо-голубые": "winter",
            "💚 Изумрудные, темно-зеленые": "autumn",
            "🤎 Карие, ореховые": "autumn",
            "💜 Серо-зеленые, серо-голубые": "summer",
            "💛 Янтарные, золотисто-карие": "spring"
        }
    },
    {
        "question": "3/8. Как ваша кожа реагирует на солнце?",
        "options": {
            "🔥 Быстро обгораю, почти не загораю": "winter",
            "🌞 Сначала обгораю, потом загораю": "summer",
            "☀️ Загораю легко и быстро": "spring",
            "🌴 Загораю до оливкового оттенка": "autumn"
        }
    },
    {
        "question": "4/8. Какой оттенок кожи у вас?",
        "options": {
            "🌸 Фарфоровый, розоватый": "winter",
            "🍑 Персиковый, бежевый": "spring",
            "🌿 Оливковый, золотистый": "autumn",
            "🌫️ Светлый с сероватым подтоном": "summer"
        }
    },
    {
        "question": "5/8. Какие цвета вам чаще всего говорят, что вам идут?",
        "options": {
            "❄️ Холодные синие, розовые": "winter",
            "🌸 Пастельные, нежные": "summer",
            "🌞 Яркие, теплые, коралловые": "spring",
            "🍂 Землистые, оливковые, терракотовые": "autumn"
        }
    },
    {
        "question": "6/8. Как выглядит вена на вашем запястье?",
        "options": {
            "🔵 Синяя, фиолетовая": "winter",
            "🟢 Зеленая": "autumn",
            "🔷 Сине-зеленая": "summer",
            "💚 Оливковая": "spring"
        }
    },
    {
        "question": "7/8. Какое украшение вам больше идет?",
        "options": {
            "✨ Серебро, белое золото": "winter",
            "🌟 Золото": "autumn",
            "🌙 Розовое золото": "spring",
            "⚜️ Матовое серебро": "summer"
        }
    },
    {
        "question": "8/8. Какой оттенок помады вам идет больше?",
        "options": {
            "🍇 Ягодный, сливовый, фуксия": "winter",
            "🌸 Розовый, ягодный": "summer",
            "🍑 Коралловый, персиковый": "spring",
            "🧱 Терракотовый, кирпичный": "autumn"
        }
    }
]

# Результаты цветотипов
COLORTYPE_RESULTS = {
    "winter": {
        "name": "❄️ Холодная Зима",
        "description": "Контрастная, яркая, холодная",
        "colors": "Холодный синий, фуксия, изумрудный, черный, белый",
        "lipstick": "Фуксия, винный, холодный красный, сливовый",
        "foundation": "Холодный розовый подтон",
        "eyes": "Графит, слива, серебро, холодные коричневые",
        "blush": "Холодный розовый, фуксия",
        "avoid": "Теплые коричневые, оранжевые, персиковые, золото"
    },
    "summer": {
        "name": "🌸 Холодное Лето",
        "description": "Мягкая, нежная, приглушенная",
        "colors": "Пыльная роза, серый, лаванда, холодный синий, изумрудный",
        "lipstick": "Холодный розовый, ягодный, сливовый, нюд с розовым подтоном",
        "foundation": "Розовато-бежевый подтон",
        "eyes": "Серые, сиреневые, холодные коричневые, графит",
        "blush": "Холодный розовый, пыльная роза",
        "avoid": "Персиковый, оранжевый, яркий красный, золотой"
    },
    "spring": {
        "name": "🌼 Теплая Весна",
        "description": "Свежая, яркая, золотистая",
        "colors": "Коралловый, персиковый, бирюзовый, золотой, слоновая кость",
        "lipstick": "Коралловый, персиковый, золотистый, теплый розовый",
        "foundation": "Золотисто-бежевый подтон",
        "eyes": "Золотистые, медные, бирюзовые, теплые коричневые",
        "blush": "Персиковый, коралловый",
        "avoid": "Холодные темные тона, черный, серый"
    },
    "autumn": {
        "name": "🍂 Теплая Осень",
        "description": "Глубокая, насыщенная, землистая",
        "colors": "Оливковый, терракот, горчичный, коричневый, ржавый",
        "lipstick": "Терракотовый, кирпичный, теплый красный, шоколадный",
        "foundation": "Золотистый, оливковый подтон",
        "eyes": "Золотисто-коричневые, оливковые, медные, слива",
        "blush": "Терракотовый, бронзовый",
        "avoid": "Холодные розовые, голубые, серебро, пастель"
    }
}

# Состояния пользователей для теста (временное хранилище)
user_test_states = {}

def start_colortype_test(user_id):
    """Начать тест на цветотип"""
    user_test_states[user_id] = {
        "answers": [],
        "current_q": 0
    }
    return COLORTYPE_QUESTIONS[0]["question"], list(COLORTYPE_QUESTIONS[0]["options"].keys())

def process_colortype_answer(user_id, answer):
    """Обработать ответ и вернуть следующий вопрос или результат"""
    if user_id not in user_test_states:
        return None, None
    
    state = user_test_states[user_id]
    q_index = state["current_q"]
    
    # Сохраняем ответ
    current_q = COLORTYPE_QUESTIONS[q_index]
    color_score = None
    for option, score in current_q["options"].items():
        if option == answer:
            color_score = score
            break
    
    if color_score:
        state["answers"].append(color_score)
    
    # Переходим к следующему вопросу
    state["current_q"] += 1
    
    if state["current_q"] >= len(COLORTYPE_QUESTIONS):
        # Тест завершен - подсчитываем результат
        result = calculate_colortype(state["answers"])
        del user_test_states[user_id]  # Очищаем состояние
        return result, None
    else:
        # Следующий вопрос
        next_q = COLORTYPE_QUESTIONS[state["current_q"]]
        return next_q["question"], list(next_q["options"].keys())

def calculate_colortype(answers):
    """Подсчет результатов теста"""
    scores = {"winter": 0, "summer": 0, "spring": 0, "autumn": 0}
    
    for answer in answers:
        if answer in scores:
            scores[answer] += 1
    
    # Определяем победителя
    winner = max(scores, key=scores.get)
    return COLORTYPE_RESULTS[winner]

def get_colortype_description(colortype_key):
    """Получить описание цветотипа"""
    ct = COLORTYPE_RESULTS.get(colortype_key, COLORTYPE_RESULTS["summer"])
    
    text = f"{ct['name']}\n"
    text += f"✨ *{ct['description']}*\n\n"
    text += f"🎨 *ВАША ПАЛИТРА:*\n{ct['colors']}\n\n"
    text += f"💄 *ПОМАДА:* {ct['lipstick']}\n"
    text += f"💎 *ТОНАЛЬНАЯ ОСНОВА:* {ct['foundation']}\n"
    text += f"👁️ *ТЕНИ:* {ct['eyes']}\n"
    text += f"🌸 *РУМЯНА:* {ct['blush']}\n\n"
    text += f"❌ *ИЗБЕГАТЬ:* {ct['avoid']}"
    
    return text