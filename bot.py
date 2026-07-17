import random
from dotenv import load_dotenv
import os

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

from dotenv import load_dotenv
import os

# ==========================
# ВСТАВЬ СЮДА СВОЙ ТОКЕН
# ==========================

load_dotenv()

TOKEN = os.getenv("TOKEN")

# ==========================
# СОВЕТЫ
# ==========================

tips = [
    "💧 Пей больше воды.",
    "😴 Спи не менее 7–8 часов.",
    "🚶 Прогуляйся хотя бы 15 минут.",
    "📚 Каждый день узнавай что-нибудь новое.",
    "😊 Чаще улыбайся.",
    "🍎 Ешь больше овощей и фруктов.",
    "📱 Делай перерывы от телефона.",
    "💪 Даже 10 минут спорта лучше, чем ничего.",
    "🎯 Ставь себе маленькие цели.",
    "❤️ Заботься о себе.",
    "🌞 Начинай день с хорошего настроения.",
    "🎵 Иногда любимая музыка творит чудеса.",
    "📖 Почитай хотя бы 10 страниц книги.",
    "🧘 Не забывай отдыхать.",
    "✨ Верь в себя!"
]

# ==========================
# РЕЦЕПТЫ
# ==========================

recipes = [
    {
        "name": "🍝 Спагетти Карбонара",
        "ingredients": "Спагетти, бекон, яйца, сыр, перец.",
        "recipe": "Отвари спагетти. Обжарь бекон. Смешай яйца с сыром и добавь к горячим спагетти."
    },
    {
        "name": "🥞 Блины",
        "ingredients": "Молоко, яйца, мука, сахар.",
        "recipe": "Смешай ингредиенты до однородности и обжарь на сковороде."
    },
    {
        "name": "🍳 Омлет",
        "ingredients": "Яйца, молоко, соль.",
        "recipe": "Взбей яйца с молоком и приготовь на слабом огне."
    },
    {
        "name": "🥗 Овощной салат",
        "ingredients": "Помидоры, огурцы, зелень, масло.",
        "recipe": "Нарежь овощи, добавь зелень и заправь маслом."
    },
    {
        "name": "🥪 Горячий бутерброд",
        "ingredients": "Хлеб, сыр, ветчина.",
        "recipe": "Положи сыр и ветчину на хлеб и запеки 5–7 минут."
    },
    {
        "name": "🍕 Мини-пицца",
        "ingredients": "Лаваш, сыр, кетчуп, колбаса.",
        "recipe": "Смажь лаваш кетчупом, добавь начинку и запеки 10 минут."
    },
]

# ==========================
# КЛАВИАТУРА
# ==========================

def main_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("💡 Совет дня", callback_data="tip")],
        [InlineKeyboardButton("🍳 Рандомный рецепт", callback_data="recipe")],
        [InlineKeyboardButton("ℹ️ О боте", callback_data="about")]
    ])
# ==========================
# /start
# ==========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "👋 <b>Добро пожаловать!</b>\n\n"
        "Я умею:\n"
        "💡 Давать совет дня\n"
        "🍳 Показывать случайный рецепт\n"
        "ℹ️ Рассказывать о себе\n\n"
        "Выбери действие ниже ⬇️"
    )

    await update.message.reply_text(
        text,
        reply_markup=main_keyboard(),
        parse_mode="HTML"
    )


# ==========================
# ОБРАБОТКА КНОПОК
# ==========================

async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    # Совет дня
    if query.data == "tip":
        tip = random.choice(tips)

        await query.edit_message_text(
            f"💡 <b>Совет дня</b>\n\n{tip}",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔄 Еще совет", callback_data="tip")],
                [InlineKeyboardButton("🏠 Назад", callback_data="menu")]
            ]),
            parse_mode="HTML"
        )

    # Рецепт
    elif query.data == "recipe":
        recipe = random.choice(recipes)

        text = (
            f"<b>{recipe['name']}</b>\n\n"
            f"🛒 <b>Ингредиенты:</b>\n"
            f"{recipe['ingredients']}\n\n"
            f"👨‍🍳 <b>Приготовление:</b>\n"
            f"{recipe['recipe']}"
        )

        await query.edit_message_text(
            text,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🎲 Другой рецепт", callback_data="recipe")],
                [InlineKeyboardButton("🏠 Назад", callback_data="menu")]
            ]),
            parse_mode="HTML"
        )

    # О боте
    elif query.data == "about":
        await query.edit_message_text(
            "ℹ️ <b>О боте</b>\n\n"
            "Этот бот написан на Python ❤️\n\n"
            "Возможности:\n"
            "• 💡 Совет дня\n"
            "• 🍳 Случайный рецепт\n\n"
            "Автор: Valera",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🏠 Назад", callback_data="menu")]
            ]),
            parse_mode="HTML"
        )

    # Главное меню
    elif query.data == "menu":
        await query.edit_message_text(
            "👋 <b>Главное меню</b>\n\n"
            "Выбери нужный раздел.",
            reply_markup=main_keyboard(),
            parse_mode="HTML"
        )
# ==========================
# ЗАПУСК БОТА
# ==========================

def main():
    app = Application.builder().token(TOKEN).build()

    # Команды
    app.add_handler(CommandHandler("start", start))

    # Обработка Inline-кнопок
    app.add_handler(CallbackQueryHandler(buttons))

    print("✅ Бот успешно запущен!")

    app.run_polling()


if __name__ == "__main__":
    main()