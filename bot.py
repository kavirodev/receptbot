import random
from dotenv import load_dotenv
import os
import json

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

# Снизу идет список советов.

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

# Теперь тут идут рецепты.

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

# Снизу находятся функции для создания клавиатуры и обработки команд кнопок.

def main_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("💡 Совет дня", callback_data="tip")],
        [InlineKeyboardButton("🍳 Рандомный рецепт", callback_data="recipe")],
        [InlineKeyboardButton("ℹ️ О боте", callback_data="about")],
        [InlineKeyboardButton("🎮 Угадай число", callback_data="game")],
    ])
# ==========================
# /start
# ==========================

USERS_FILE = "users.json"

def load_users():
    try:
        with open(USERS_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_users(users):
    with open(USERS_FILE, "w", encoding="utf-8") as file:
        json.dump(users, file, ensure_ascii=False, indent=4)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    users = load_users()

    user_id = str(update.effective_user.id)
    name = update.effective_user.first_name

    if user_id not in users:
        users[user_id] = {
            "name": name,
            "registered": True,
            "score": 0
        }

        save_users(users)

        await update.message.reply_text(
            f"👋 Привет, {name}!\n\n"
            "✅ Ты успешно зарегистрирован!\n\n"
            "Добро пожаловать в бота!",
            reply_markup=main_keyboard()
        )

    else:
        await update.message.reply_text(
            f"С возвращением, {name}!\n\n"
            "Выбери действие:",
            reply_markup=main_keyboard()
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

       # Тут идут факты о создателе бота, и функция которая их выводит пользователю в телеграм. 
    elif query.data == "about":
        await query.edit_message_text(
            "<b>О боте</b>\n\n"
            "Я бот, который может давать советы, рассказывать себе, включать мини-игру с угадыванием числа и показывать случайные рецепты.\n\n"
            "Автор бота: Костюнин Валерий, 14 лет.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Назад", callback_data="menu")]
            ]),
            parse_mode="HTML"
        )

    elif query.data == "game":
        await query.edit_message_text(
    "Угадай число\n\n"
    "Выбери уровень сложности:\n\n"
    "За легкий уровень ты получишь одно очко\n"
    "За средний ты получишь два очка\n"
    "За сложный ты получишь три очка",
    reply_markup=InlineKeyboardMarkup([
        [InlineKeyboardButton("Таблица лидеров", callback_data="leaderboard")],
        [InlineKeyboardButton("Легкий (1-10)", callback_data="start_easy_game")],
        [InlineKeyboardButton("Средний (1-100)", callback_data="start_medium_game")],
        [InlineKeyboardButton("Сложный (1-1000)", callback_data="start_hard_game")],
        [InlineKeyboardButton("Назад", callback_data="menu")]
    ]),
)

        # Таблица лидеров
    elif query.data == "leaderboard":
        users = load_users()

        sorted_users = sorted(
            users.values(),
            key=lambda user: user.get("score", 0),
            reverse=True
        )

        text = "<b>🏆 Таблица лидеров</b>\n\n"

        if not sorted_users:
            text += "Пока что нет победителей."
        else:
            for i, user in enumerate(sorted_users[:10], start=1):
                name = user.get("name", "Неизвестный")
                score = user.get("score", 0)

                text += f"{i}. {name}: {score} очков\n"

        await query.edit_message_text(
            text,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(" Назад", callback_data="menu")]
            ]),
            parse_mode="HTML"
        )

    elif query.data == "start_easy_game":
        user_id = update.effective_user.id
        games[user_id] = random.randint(1, 10)
        games_scores[user_id] = 1

        await query.edit_message_text("Я загадал число от 1 до 10. Попробуй угадать")

    elif query.data == "start_medium_game":
        user_id = update.effective_user.id
        games[user_id] = random.randint(1, 100)
        games_scores[user_id] = 2

        await query.edit_message_text("Я загадал число от 1 до 100. Попробуй угадать")

    elif query.data == "start_hard_game":
        user_id = update.effective_user.id
        games[user_id] = random.randint(1, 1000)
        games_scores[user_id] = 3

        await query.edit_message_text("Я загадал число от 1 до 1000. Попробуй угадать")

    # Главное меню
    elif query.data == "menu":
        await query.edit_message_text(
            "👋 <b>Главное меню</b>\n\n"
            "Выбери нужный раздел.",
            reply_markup=main_keyboard(),
            parse_mode="HTML"
        )
games = {}
games_scores = {}
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
        users = load_users()
        users[str(user_id)]["score"] += games_scores[user_id]
        save_users(users)
        await update.message.reply_text("Поздравляю, ты угадал число!\n\n"
                                        "Возращаю тебя в главное меню",
                                        reply_markup=main_keyboard()
                                        )
        del games[user_id]
        del games_scores[user_id]


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