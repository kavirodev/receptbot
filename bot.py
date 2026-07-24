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
    MessageHandler,
    filters,
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

my_name = "Костюнин Валерий"
my_age = 14
my_hobby = "играть в видео игры"
fact1 = "Я умею играть на гитаре"
fact2 = "Моя любимая видеоигра это Dota 2."
final_fact = "Я увлекаюсь техникой"
async def about(update, context):
    text = (
        f"Меня зовут {my_name}\n"
        f"Мне {my_age} лет\n"
        f"Мое хобби {my_hobby}\n"
        f"Первый факт обо мне {fact1}\n"
        f"Второй факт обо мне {fact2}\n"
        f"Последний факт обо мне {final_fact}\n"
        f"Этот бот работает 24/7 на pythonanywhere\n"
    )
    await update.message.reply_text(text)

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



    # Главное меню
    elif query.data == "menu":
        await query.edit_message_text(
            "👋 <b>Главное меню</b>\n\n"
            "Выбери нужный раздел.",
            reply_markup=main_keyboard(),
            parse_mode="HTML"
        )
games = {}
async def start_easy_game(update,context):
    user_id = update.effective_user.id
    secret_number = random.randint(1,10)
    games[user_id] = secret_number

    await update.message.reply_text("Я загадал число от 1 до 10. Попробуй угадать :)")

async def handle_guess(update, context):
    user_id = update.effective_user.id

    if user_id not in games:
        return
    text = update.message.text

    if not text.isdigit():
        await update.message.reply_text("Это не число, иди попробуй сново.")
        return

    guess = int(text)
    secret_number = games[user_id]
    if guess < secret_number:
        await update.message.reply_text("Больше!")
    elif guess > secret_number:
        await update.message.reply_text("Меньше!")
    else:
        await update.message.reply_text("Поздравляю, ты угадал число!")


async def start_medium_game(update,context):
    user_id = update.effective_user.id
    secret_number = random.randint(1,100)
    games[user_id] = secret_number

    await update.message.reply_text("Я загадал число от 1 до 100. Попробуй угадать :)")

async def start_hard_game(update,context):
    user_id = update.effective_user.id
    secret_number = random.randint(1,1000)
    games[user_id] = secret_number

    await update.message.reply_text("Я загадал число от 1 до 1000. Попробуй угадать :)")


# ==========================
# ЗАПУСК БОТА
# ==========================

def main():
    app = Application.builder().token(TOKEN).build()

    # Команды
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("about",about))
    app.add_handler(CommandHandler("start_easy_game",start_easy_game))
    app.add_handler(CommandHandler("start_medium_game",start_medium_game))
    app.add_handler(CommandHandler("start_hard_game",start_hard_game))
    # Обработка Inline-кнопок
    app.add_handler(CallbackQueryHandler(buttons))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_guess))
    print("✅ Бот успешно запущен!")

    app.run_polling()


if __name__ == "__main__":
    main()