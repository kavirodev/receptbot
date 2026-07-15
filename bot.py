

import json
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
    MessageHandler,
    ContextTypes,
    filters,
)

from dotenv import load_dotenv
load_dotenv()

TOKEN = os.environ.get('TOKEN')

JSON_FILE = "users.json"


def load_data():
    try:
        with open(JSON_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def save_data(data):
    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


waiting_users = {}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📝 Начать анкету", callback_data="start_form")],
        [InlineKeyboardButton("📄 Показать информацию", callback_data="show_info")]
    ]

    await update.message.reply_text(
        "Добро пожаловать!",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = str(query.from_user.id)

    if query.data == "start_form":
        waiting_users[user_id] = {
            "step": 1
        }

        await query.message.reply_text(
            "❓ Вопрос 1:\n\nКак тебя зовут?"
        )

    elif query.data == "show_info":
        data = load_data()

        if user_id not in data:
            await query.message.reply_text(
                "Вы ещё не заполняли анкету."
            )
            return

        user = data[user_id]

        text = (
            f"📄 Ваша информация\n\n"
            f"🆔 ID: {user_id}\n"
            f"👤 Имя: {user['name']}\n"
            f" Любимая игра: {user['game']}"
        )

        await query.message.reply_text(text)


async def messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)

    if user_id not in waiting_users:
        return

    state = waiting_users[user_id]

    if state["step"] == 1:
        state["name"] = update.message.text
        state["step"] = 2

        await update.message.reply_text(
            " Вопрос 2:\n\nКакая твоя любимая игра?"
        )

    elif state["step"] == 2:
        state["game"] = update.message.text

        data = load_data()

        data[user_id] = {
            "user_id": int(user_id),
            "name": state["name"],
            "game": state["game"]
        }

        save_data(data)

        del waiting_users[user_id]

        keyboard = [
            [InlineKeyboardButton("📝 Начать анкету", callback_data="start_form")],
            [InlineKeyboardButton("📄 Показать информацию", callback_data="show_info")]
        ]

        await update.message.reply_text(
            "✅ Анкета успешно сохранена!",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )


def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(buttons))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, messages))

    print("Бот запущен!")

    app.run_polling()


if __name__ == "__main__":
    main()