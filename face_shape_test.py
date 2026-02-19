# face_shape_test.py — опросник для определения формы лица

# Вопросы для определения формы лица
FACE_SHAPE_QUESTIONS = [
    {
        "question": "1/4. Какая часть вашего лица самая широкая?",
        "options": {
            "👨 Лоб": "forehead",
            "😊 Скулы": "cheekbones",
            "🦷 Челюсть": "jaw",
            "⚖️ Все части примерно равны": "equal"
        }
    },
    {
        "question": "2/4. Какая форма вашей линии челюсти?",
        "options": {
            "🟣 Острая, заостренная": "sharp",
            "🟢 Закругленная, мягкая": "round",
            "🔵 Угловатая, квадратная": "angular",
            "⚪️ Не могу определить": "unknown"
        }
    },
    {
        "question": "3/4. Как бы вы описали ваш подбородок?",
        "options": {
            "🔻 Острый, выступающий": "pointed",
            "⚪️ Округлый": "rounded",
            "◼️ Квадратный, широкий": "square",
            "📏 Прямой, средней ширины": "straight"
        }
    },
    {
        "question": "4/4. Какое соотношение длины и ширины лица?",
        "options": {
            "📏 Длина примерно равна ширине": "equal",
            "📐 Длина больше ширины": "longer",
            "📏 Ширина больше длины": "wider",
            "❓ Не уверен(а)": "unsure"
        }
    }
]

# Результаты форм лица с ДЕТАЛЬНЫМ описанием
FACE_SHAPE_RESULTS = {
    "oval": {
        "name": "✨ Овальное лицо",
        "description": "Сбалансированные пропорции, длина примерно в 1.5 раза больше ширины. Скулы слегка выступают, линия челюсти закруглена.",
        "characteristics": [
            "✅ Лоб чуть шире подбородка",
            "✅ Скулы — самая широкая часть",
            "✅ Подбородок закругленный",
            "✅ Линия челюсти мягкая"
        ],
        "haircuts": "✅ Каскад, боб-каре, длинные прямые волосы, пикси\n❌ Избегайте: очень коротких стрижек, закрывающих лоб",
        "glasses": "✅ Прямоугольные, кошачий глаз, овальные, геометрические\n❌ Избегайте: слишком массивных оправ",
        "makeup": "✅ Можно экспериментировать. Румяна наносите на скулы и растушевывайте вверх к вискам.\n❌ Контуринг не обязателен",
        "eyebrows": "✅ Горизонтальные или слегка изогнутые брови",
        "celebrity": "Джордж Клуни, Джулия Робертс, Ким Кардашьян"
    },
    "round": {
        "name": "🟡 Круглое лицо",
        "description": "Ширина и длина примерно равны, мягкие округлые линии, полные щеки, закругленный подбородок.",
        "characteristics": [
            "✅ Ширина и длина почти равны",
            "✅ Мягкие, округлые линии",
            "✅ Полные щеки",
            "✅ Закругленный подбородок"
        ],
        "haircuts": "✅ Асимметричные стрижки, длинные волосы, объем на макушке, косая челка\n❌ Избегайте: круглых стрижек до подбородка, прямой густой челки",
        "glasses": "✅ Прямоугольные, угловатые, кошачий глаз\n❌ Избегайте: круглых оправ",
        "makeup": "✅ Вертикальный контуринг по бокам лба и скул, вытянутые стрелки, тени с растушевкой вверх\n❌ Избегайте: горизонтальных линий",
        "eyebrows": "✅ Брови с высоким подъемом",
        "celebrity": "Селена Гомес, Кирстен Данст, Мила Кунис"
    },
    "square": {
        "name": "🔲 Квадратное лицо",
        "description": "Широкий лоб, выраженные скулы, четкая квадратная линия челюсти. Длина и ширина примерно равны.",
        "characteristics": [
            "✅ Широкий лоб",
            "✅ Выраженные скулы",
            "✅ Квадратная линия челюсти",
            "✅ Угловатые черты"
        ],
        "haircuts": "✅ Мягкие волны, градуированные стрижки, косая челка, слоистые стрижки\n❌ Избегайте: геометрических стрижек, прямых линий, гладких пучков",
        "glasses": "✅ Овальные, круглые, авиаторы, без верхней линии\n❌ Избегайте: квадратных и прямоугольных оправ",
        "makeup": "✅ Смягчение углов, румяна на яблочки щек, акцент на глаза, мягкая растушевка\n❌ Избегайте: четких линий и графичных форм",
        "eyebrows": "✅ Мягкие, округлые брови",
        "celebrity": "Анджелина Джоли, Кира Найтли, Деми Мур"
    },
    "heart": {
        "name": "❤️ Сердцевидное лицо",
        "description": "Широкий лоб, высокие скулы, узкий заостренный подбородок.",
        "characteristics": [
            "✅ Широкий лоб",
            "✅ Высокие скулы",
            "✅ Узкий подбородок",
            "✅ Форма перевернутого треугольника"
        ],
        "haircuts": "✅ Боб, пикси, волнистые средней длины, боковая челка, объем внизу\n❌ Избегайте: объема на макушке, тяжелой прямой челки",
        "glasses": "✅ Овальные, круглые, без верхней линии, авиаторы\n❌ Избегайте: массивных оправ наверху",
        "makeup": "✅ Акцент на глаза, затемнение висков, светлый хайлайтер на подбородок\n❌ Избегайте: темных тонов на подбородке",
        "eyebrows": "✅ Мягкие, естественные брови",
        "celebrity": "Риз Уизерспун, Хлоя Грейс Морец, Кэти Холмс"
    },
    "rectangle": {
        "name": "📏 Прямоугольное лицо",
        "description": "Длина明显 больше ширины, прямой лоб, квадратная челюсть.",
        "characteristics": [
            "✅ Длина больше ширины",
            "✅ Прямой лоб",
            "✅ Квадратная челюсть",
            "✅ Удлиненная форма"
        ],
        "haircuts": "✅ Объем по бокам, мягкие волны, косая челка, градуированные стрижки\n❌ Избегайте: длинных прямых волос, зачесанных назад",
        "glasses": "✅ Овальные, круглые, большие оправы\n❌ Избегайте: узких прямоугольных оправ",
        "makeup": "✅ Визуально укорачивает лицо — темный тональный крем на подбородке и лбу, светлый на скулах",
        "eyebrows": "✅ Прямые, горизонтальные брови",
        "celebrity": "Сара Джессика Паркер, Лив Тайлер"
    }
}

# Состояния пользователей для теста
user_face_test_states = {}

def start_face_shape_test(user_id):
    """Начать тест на определение формы лица"""
    user_face_test_states[user_id] = {
        "answers": [],
        "current_q": 0
    }
    return FACE_SHAPE_QUESTIONS[0]["question"], list(FACE_SHAPE_QUESTIONS[0]["options"].keys())

def process_face_shape_answer(user_id, answer):
    """Обработать ответ и вернуть следующий вопрос или результат"""
    if user_id not in user_face_test_states:
        return None, None
    
    state = user_face_test_states[user_id]
    q_index = state["current_q"]
    
    # Сохраняем ответ
    current_q = FACE_SHAPE_QUESTIONS[q_index]
    shape_value = None
    for option, value in current_q["options"].items():
        if option == answer:
            shape_value = value
            break
    
    if shape_value:
        state["answers"].append(shape_value)
    
    # Переходим к следующему вопросу
    state["current_q"] += 1
    
    if state["current_q"] >= len(FACE_SHAPE_QUESTIONS):
        # Тест завершен - подсчитываем результат
        result = calculate_face_shape(state["answers"])
        # Очищаем состояние ПОСЛЕ получения результата
        del user_face_test_states[user_id]
        return result, None
    else:
        # Следующий вопрос
        next_q = FACE_SHAPE_QUESTIONS[state["current_q"]]
        return next_q["question"], list(next_q["options"].keys())

def calculate_face_shape(answers):
    """Подсчет результатов теста формы лица с ФИНАЛЬНЫМ ВЫВОДОМ"""
    
    if len(answers) < 4:
        return FACE_SHAPE_RESULTS["oval"]
    
    widest = answers[0] if len(answers) > 0 else "cheekbones"
    jaw = answers[1] if len(answers) > 1 else "round"
    chin = answers[2] if len(answers) > 2 else "rounded"
    ratio = answers[3] if len(answers) > 3 else "longer"
    
    # Логика определения
    if widest == "forehead" and jaw == "sharp" and chin == "pointed":
        result_key = "heart"
    elif widest == "jaw" and jaw == "angular" and chin == "square":
        result_key = "square"
    elif ratio == "equal" and jaw == "round":
        result_key = "round"
    elif ratio == "longer" and jaw in ["angular", "square"]:
        result_key = "rectangle"
    else:
        result_key = "oval"
    
    return {
        "key": result_key,
        "result": FACE_SHAPE_RESULTS[result_key]
    }

def get_face_shape_description(shape_key):
    """Получить полное описание формы лица"""
    fs = FACE_SHAPE_RESULTS.get(shape_key, FACE_SHAPE_RESULTS["oval"])
    
    text = f"📐 *{fs['name']}*\n\n"
    text += f"📝 *ОПИСАНИЕ:* {fs['description']}\n\n"
    text += f"🔍 *ХАРАКТЕРИСТИКИ:*\n"
    for char in fs['characteristics']:
        text += f"{char}\n"
    text += f"\n✂️ *СТРИЖКИ:*\n{fs['haircuts']}\n\n"
    text += f"👓 *ОЧКИ:*\n{fs['glasses']}\n\n"
    text += f"💄 *МАКИЯЖ:*\n{fs['makeup']}\n\n"
    text += f"✍️ *БРОВИ:* {fs['eyebrows']}\n\n"
    text += f"🌟 *ЗНАМЕНИТОСТИ С ТАКОЙ ЖЕ ФОРМОЙ:*\n{fs.get('celebrity', '')}"
    
    return text