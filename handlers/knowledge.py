from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from keyboards import knowledge_menu

# СОЗДАЕМ РОУТЕР
router = Router()

# ==================== СОСТОЯНИЯ ДЛЯ РАЗБОРА СОСТАВОВ ====================

class IngredientAnalysis(StatesGroup):
    """Состояния для разбора состава"""
    waiting_product_name = State()

# ==================== ГЛАВНОЕ МЕНЮ ЗНАНИЙ ====================

@router.message(F.text == "📚 ЗНАНИЯ и новости")
async def knowledge_main(message: Message):
    """Главное меню раздела ЗНАНИЯ"""
    await message.answer(
        "📚 *Знания и новости*\n\nВыберите раздел:",
        reply_markup=knowledge_menu(),
        parse_mode="Markdown"
    )

# ==================== БАЗА КОМПОНЕНТОВ ====================

@router.message(F.text == "🧪 База компонентов")
async def knowledge_components(message: Message):
    """База компонентов с командами"""
    text = """
🧪 *БАЗА КОМПОНЕНТОВ*

*Нажмите на команду, чтобы узнать подробнее:*

🔹 **/ha** — Гиалуроновая кислота
🔹 **/niacinamide** — Ниацинамид (B3)
🔹 **/retinol** — Ретинол (A)
🔹 **/vitamin_c** — Витамин С
🔹 **/ceramides** — Церамиды
🔹 **/peptides** — Пептиды
🔹 **/aha_bha** — AHA/BHA кислоты
🔹 **/azelaic** — Азелаиновая кислота
🔹 **/squalane** — Сквалан
🔹 **/centella** — Центелла азиатская

💡 *Введите команду в чат*
"""
    await message.answer(text, parse_mode="Markdown")

# ==================== КОМАНДЫ ДЛЯ КОМПОНЕНТОВ ====================

@router.message(Command("ha"))
async def cmd_ha(message: Message):
    text = """
🔬 *ГИАЛУРОНОВАЯ КИСЛОТА*

📌 *Что это:* Увлажняющий компонент, притягивает и удерживает воду

💪 *Эффективность:* Доказана клинически

🎯 *Для чего:* Увлажнение, разглаживание мелких морщин

🌍 *КЛИМАТ:*
✅ Влажность >40% — работает идеально
⚠️ Влажность <40% — наносить ТОЛЬКО на влажную кожу

💡 *СОВЕТ:* Наносите на влажную кожу сразу после умывания

⭐ *Популярные средства:* The Ordinary HA, La Roche-Posay Hyalu B5, Hada Labo
"""
    await message.answer(text, parse_mode="Markdown")

@router.message(Command("niacinamide"))
async def cmd_niacinamide(message: Message):
    text = """
🔬 *НИАЦИНАМИД (ВИТАМИН B3)*

📌 *Что это:* Многофункциональный компонент

💪 *Эффективность:* Доказана

🎯 *Для чего:* 
• Укрепление защитного барьера
• Матирование, сужение пор
• Осветление пигментации

🌍 *КЛИМАТ:* Работает в любом климате

💡 *СОВЕТ:* Оптимальная концентрация 5-10%

⭐ *Популярные средства:* The Ordinary Niacinamide, La Roche-Posay Effaclar Duo+
"""
    await message.answer(text, parse_mode="Markdown")

@router.message(Command("retinol"))
async def cmd_retinol(message: Message):
    text = """
🔬 *РЕТИНОЛ (ВИТАМИН A)*

📌 *Что это:* Золотой стандарт антивозрастного ухода

💪 *Эффективность:* Максимально доказана

🎯 *Для чего:* 
• Ускорение обновления клеток
• Стимуляция коллагена
• Разглаживание морщин

🌍 *КЛИМАТ:*
⚠️ Не использовать в сухом климате без плотного крема
❌ Не использовать с кислотами в один день

💡 *СОВЕТ:* Начинайте с 0.25%, 1 раз в 3 дня. SPF обязателен!

⭐ *Популярные средства:* The Ordinary Retinol, La Roche-Posay Retinol B3
"""
    await message.answer(text, parse_mode="Markdown")

@router.message(Command("vitamin_c"))
async def cmd_vitamin_c(message: Message):
    text = """
🔬 *ВИТАМИН C (АСКОРБИНОВАЯ КИСЛОТА)*

📌 *Что это:* Мощный антиоксидант

💪 *Эффективность:* Доказана

🎯 *Для чего:* 
• Антиоксидантная защита
• Осветление пигментации
• Стимуляция коллагена

🌍 *КЛИМАТ:*
✅ Защищает от УФ и загрязнений
⚠️ Нестабилен на свету

💡 *СОВЕТ:* Используйте утром под SPF

⭐ *Популярные средства:* The Ordinary Vitamin C, Geek & Gorgeous C-Glow
"""
    await message.answer(text, parse_mode="Markdown")

@router.message(Command("ceramides"))
async def cmd_ceramides(message: Message):
    text = """
🔬 *ЦЕРАМИДЫ*

📌 *Что это:* Липиды, восстанавливающие барьер кожи

💪 *Эффективность:* Доказана

🎯 *Для чего:* 
• Восстановление поврежденного барьера
• Удержание влаги
• Защита от агрессивных факторов

🌍 *КЛИМАТ:*
✅ Идеальны для сухого и ветреного климата
✅ Подходят для чувствительной кожи

💡 *СОВЕТ:* Ищите в составе "ceramide NP, AP, EOP"

⭐ *Популярные средства:* Cerave, Dr.Jart+ Ceramidin, The Ordinary NMF
"""
    await message.answer(text, parse_mode="Markdown")

@router.message(Command("peptides"))
async def cmd_peptides(message: Message):
    text = """
🔬 *ПЕПТИДЫ*

📌 *Что это:* Сигналы для клеток кожи

💪 *Эффективность:* Доказана

🎯 *Для чего:* 
• Стимуляция коллагена
• Разглаживание морщин
• Укрепление кожи

🌍 *КЛИМАТ:* Работают в любом климате

💡 *СОВЕТ:* Ищите матриксил, аргирелин, медный пептид

⭐ *Популярные средства:* The Ordinary Buffet, Geek & Gorgeous 101
"""
    await message.answer(text, parse_mode="Markdown")

@router.message(Command("aha_bha"))
async def cmd_aha_bha(message: Message):
    text = """
🔬 *AHA/BHA КИСЛОТЫ*

📌 *Что это:* Химические эксфолианты

💪 *Эффективность:* Доказана

🎯 *Для чего:* 
• AHA — отшелушивание поверхности, увлажнение
• BHA — очищение пор, противовоспалительное

🌍 *КЛИМАТ:*
⚠️ Не использовать при низкой влажности
⚠️ SPF обязателен!

💡 *СОВЕТ:* Начинайте с 1-2 раз в неделю

⭐ *Популярные средства:* The Ordinary AHA 30% + BHA 2%, COSRX BHA Power Liquid
"""
    await message.answer(text, parse_mode="Markdown")

@router.message(Command("azelaic"))
async def cmd_azelaic(message: Message):
    text = """
🔬 *АЗЕЛАИНОВАЯ КИСЛОТА*

📌 *Что это:* Мягкий компонент для проблемной кожи

💪 *Эффективность:* Доказана

🎯 *Для чего:* 
• Лечение акне и розацеа
• Осветление постакне
• Противовоспалительное

🌍 *КЛИМАТ:* Подходит для любого климата

💡 *СОВЕТ:* Можно использовать утром и вечером

⭐ *Популярные средства:* The Ordinary Azelaic Acid, Skinoren
"""
    await message.answer(text, parse_mode="Markdown")

@router.message(Command("squalane"))
async def cmd_squalane(message: Message):
    text = """
🔬 *СКВАЛАН*

📌 *Что это:* Легкий увлажнитель

💪 *Эффективность:* Доказана

🎯 *Для чего:* 
• Увлажнение без жирности
• Восстановление барьера
• Подходит для всех типов кожи

🌍 *КЛИМАТ:* Работает в любом климате

💡 *СОВЕТ:* Ищите растительный сквалан

⭐ *Популярные средства:* The Ordinary Squalane, Biossance
"""
    await message.answer(text, parse_mode="Markdown")

@router.message(Command("centella"))
async def cmd_centella(message: Message):
    text = """
🔬 *ЦЕНТЕЛЛА АЗИАТСКАЯ*

📌 *Что это:* Лекарственное растение

💪 *Эффективность:* Доказана

🎯 *Для чего:* 
• Успокаивает раздражения
• Заживляет повреждения
• Подходит для чувствительной кожи

🌍 *КЛИМАТ:* Идеальна для ветреной погоды

💡 *СОВЕТ:* Ищите "madecassoside", "centella asiatica"

⭐ *Популярные средства:* Skin1004, COSRX Centella, La Roche-Posay Cicaplast
"""
    await message.answer(text, parse_mode="Markdown")

# ==================== РАЗБОР СОСТАВОВ ====================

@router.message(F.text == "🔬 Разбор составов")
async def analysis_start(message: Message, state: FSMContext):
    """Начать разбор состава"""
    await state.set_state(IngredientAnalysis.waiting_product_name)
    await message.answer(
        "🔬 *РАЗБОР СОСТАВОВ*\n\n"
        "📝 *Введите название средства:*\n\n"
        "Примеры: Cicaplast, Effaclar, Cerave, The Ordinary\n\n"
        "Или введите состав для разбора",
        parse_mode="Markdown"
    )

@router.message(IngredientAnalysis.waiting_product_name)
async def analysis_process(message: Message, state: FSMContext):
    """Обработка запроса на разбор состава"""
    query = message.text.lower()
    
    if "cicaplast" in query:
        text = """
🔬 *La Roche-Posay Cicaplast Baume B5*

📋 *СОСТАВ:*
• Пантенол 5% — восстановление
• Мадекассосид — заживление
• Масло ши — питание
• Цинк — противовоспалительное

✅ *ПЛЮСЫ:*
• Быстро заживляет
• Успокаивает раздражение
• Без отдушек

⚠️ *МИНУСЫ:*
• Плотная текстура
• Может забивать поры

🎯 *ДЛЯ КОГО:* Сухая, поврежденная, чувствительная кожа
⭐ *РЕЙТИНГ:* 4.9/5
"""
    elif "effaclar" in query:
        text = """
🔬 *La Roche-Posay Effaclar Duo+*

📋 *СОСТАВ:*
• Ниацинамид — восстановление барьера
• Салициловая кислота — очищение пор
• Цинк — матирование

✅ *ПЛЮСЫ:*
• Уменьшает жирный блеск
• Сужает поры
• Легкая текстура

⚠️ *МИНУСЫ:*
• Может сушить
• Есть отдушка

🎯 *ДЛЯ КОГО:* Жирная, комбинированная, проблемная кожа
⭐ *РЕЙТИНГ:* 4.7/5
"""
    elif "cerave" in query:
        text = """
🔬 *Cerave Moisturizing Cream*

📋 *СОСТАВ:*
• Церамиды — восстановление барьера
• Гиалуроновая кислота — увлажнение
• Глицерин — смягчение

✅ *ПЛЮСЫ:*
• Восстанавливает барьер
• Без отдушек
• Экономичный

⚠️ *МИНУСЫ:*
• Плотная текстура
• Не подходит для жирной кожи

🎯 *ДЛЯ КОГО:* Сухая, нормальная кожа
⭐ *РЕЙТИНГ:* 4.8/5
"""
    elif "hyaluronic" in query or "ordinary ha" in query:
        text = """
🔬 *The Ordinary Hyaluronic Acid 2% + B5*

📋 *СОСТАВ:*
• Гиалуроновая кислота — увлажнение
• Пантенол — восстановление

✅ *ПЛЮСЫ:*
• Хорошо увлажняет
• Низкая цена
• Легкая текстура

⚠️ *МИНУСЫ:*
• Может липнуть
• Требует влажную кожу

🎯 *ДЛЯ КОГО:* Все типы кожи
⭐ *РЕЙТИНГ:* 4.8/5
"""
    elif "niacinamide" in query:
        text = """
🔬 *The Ordinary Niacinamide 10% + Zinc 1%*

📋 *СОСТАВ:*
• Ниацинамид — матирование, барьер
• Цинк — противовоспалительное

✅ *ПЛЮСЫ:*
• Контролирует жирный блеск
• Сужает поры
• Низкая цена

⚠️ *МИНУСЫ:*
• Может скатываться
• Высокая концентрация

🎯 *ДЛЯ КОГО:* Жирная, комбинированная кожа
⭐ *РЕЙТИНГ:* 4.9/5
"""
    else:
        text = f"""
🔬 *Разбор состава: {message.text}*

❌ *Средство не найдено в базе*

📝 *Попробуйте:*
• Cicaplast
• Effaclar
• Cerave
• The Ordinary

💡 *Или используйте команды компонентов:*
/ha, /niacinamide, /retinol, /vitamin_c, /ceramides
"""
    
    await message.answer(text, parse_mode="Markdown")
    await state.clear()

# ==================== КАНАЛЫ BLOOMSTYLE ====================

@router.message(F.text == "📰 Каналы BloomStyle")
async def knowledge_channels(message: Message):
    """Список Telegram-каналов"""
    text = f"""
📰 *КАНАЛЫ BLOOMSTYLE*

🔬 **Научный подход** – @bloomstyle_science
   • Глубокие разборы компонентов
   • Новости доказательной косметологии
   • Исследования и мифы

🇪🇺 **Европейские новинки** – @bloomstyle_europe
   • Франция, Италия, Германия
   • Люкс и аптечная косметика

🇰🇷 **Азиатские новинки** – @bloomstyle_asia
   • Корея, Япония, Китай
   • K-Beauty и J-Beauty тренды

🇷🇺 **Российские бренды** – @bloomstyle_russia
   • Новинки локальных марок
   • Импортозамещение в косметике

🔗 *Нажмите на название канала, чтобы подписаться*
"""
    await message.answer(text, parse_mode="Markdown")

# ==================== ЧЕЛЛЕНДЖИ ====================

@router.message(F.text == "🏆 Челленджи")
async def knowledge_challenges(message: Message):
    """Месячный челлендж"""
    text = """
🏆 *МЕСЯЧНЫЙ ЧЕЛЛЕНДЖ: ЗДОРОВЫЙ БАРЬЕР*

📅 *Февраль 2026 (28 дней)*

🗓 *НЕДЕЛЯ 1: Очищение (1-7 фев)*
   ✅ Двойное очищение каждый вечер
   🎁 +10 баллов/день

🗓 *НЕДЕЛЯ 2: Увлажнение (8-14 фев)*
   ✅ Гиалуроновая кислота на влажную кожу
   🎁 +15 баллов/день

🗓 *НЕДЕЛЯ 3: Восстановление (15-21 фев)*
   ✅ Крем с церамедами ежедневно
   🎁 +20 баллов/день

🗓 *НЕДЕЛЯ 4: Защита (22-28 фев)*
   ✅ SPF 30+ каждый день
   🎁 +15 баллов/день

🏅 *КАК УЧАСТВОВАТЬ:*
• /join — присоединиться к челленджу
• /done — отметить выполнение
• /stats — моя статистика

🎁 *ПРИЗЫ:*
🥇 1 место: 3 месяца Premium
🥈 2-3 место: 1 месяц Premium
🥉 4-10 место: промокод 1000₽
"""
    await message.answer(text, parse_mode="Markdown")

@router.message(Command("join"))
async def join_challenge(message: Message):
    await message.answer(
        "✅ *Вы присоединились к челленджу!*\n\n"
        "📅 Сегодня: День 1 — Двойное очищение\n"
        "👉 Отправьте /done после выполнения",
        parse_mode="Markdown"
    )

@router.message(Command("done"))
async def done_challenge(message: Message):
    await message.answer(
        "✅ *Отмечено! +10 баллов*\n\n"
        "📊 Всего баллов: 10\n"
        "🔥 Прогресс: 3%",
        parse_mode="Markdown"
    )

# ==================== ВОЗВРАТ В МЕНЮ ====================

@router.message(F.text == "🔙 В меню ЗНАНИЯ")
async def back_to_knowledge(message: Message):
    """Возврат в меню ЗНАНИЯ"""
    await message.answer(
        "📚 *Знания и новости*",
        reply_markup=knowledge_menu(),
        parse_mode="Markdown"
    )