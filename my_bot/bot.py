
import os
import telebot
from dotenv import load_dotenv
from telebot import types
import random

# Завантаження токена з файлу .env
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise ValueError("Не знайдено токен BOT_TOKEN у файлі .env")

bot = telebot.TeleBot(TOKEN)

# База команд Формули-1
teams = [
    "Ferrari",
    "Mercedes",
    "McLaren",
    "Red Bull Racing"
]

# База гонщиків
drivers = [
    "Lewis Hamilton",
    "Max Verstappen",
    "Charles Leclerc",
    "Lando Norris"
]

# База гоночних трас
tracks = [
    "Monza",
    "Silverstone",
    "Monaco",
    "Spa-Francorchamps"
]

# База цікавих фактів
facts = [
    "Формула-1 є найвищим рівнем міжнародних кільцевих автоперегонів.",
    "Monaco Grand Prix проходить на міських вулицях.",
    "Monza відома як одна з найшвидших трас Формули-1.",
    "Команди Формули-1 використовують складні гібридні силові установки."
]

# База запитань для вікторини
questions = [
    {
        "question": "Яка команда має емблему з конем?",
        "answers": ["Ferrari", "Mercedes", "McLaren"],
        "correct": "Ferrari"
    },
    {
        "question": "У якій країні проходить Гран-прі Монте-Карло?",
        "answers": ["Італія", "Монако", "Велика Британія"],
        "correct": "Монако"
    },
    {
        "question": "Яка траса відома назвою Monza?",
        "answers": ["Італія", "Франція", "Іспанія"],
        "correct": "Італія"
    }
]

# Зберігання поточного запитання для кожного користувача
user_questions = {}


# Команда початку роботи
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        "🏎 Вітаю у Formula World Bot!\n\n"
        "Тут ти можеш дізнаватися більше про Формулу-1 "
        "та перевіряти свої знання.\n\n"
        "Використовуй /help, щоб побачити команди."
    )


# Команда допомоги
@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(
        message.chat.id,
        "📌 Команди Formula World Bot:\n\n"
        "/start — початок роботи\n"
        "/help — список команд\n"
        "/quiz — вікторина про Формулу-1\n"
        "/teams — список команд\n"
        "/drivers — список гонщиків\n"
        "/tracks — список трас\n"
        "/facts — цікаві факти"
    )


# Перегляд команд
@bot.message_handler(commands=['teams'])
def show_teams(message):
    bot.send_message(
        message.chat.id,
        "🏁 Команди Формули-1:\n\n" + "\n".join(teams)
    )


# Перегляд гонщиків
@bot.message_handler(commands=['drivers'])
def show_drivers(message):
    bot.send_message(
        message.chat.id,
        "🏎 Гонщики:\n\n" + "\n".join(drivers)
    )


# Перегляд трас
@bot.message_handler(commands=['tracks'])
def show_tracks(message):
    bot.send_message(
        message.chat.id,
        "🌍 Гоночні траси:\n\n" + "\n".join(tracks)
    )


# Перегляд цікавих фактів
@bot.message_handler(commands=['facts'])
def show_facts(message):
    bot.send_message(
        message.chat.id,
        "💡 Цікавий факт:\n\n" + random.choice(facts)
    )


# Запуск вікторини
@bot.message_handler(commands=['quiz'])
def quiz(message):
    question = random.choice(questions)

    user_questions[message.from_user.id] = question

    keyboard = types.ReplyKeyboardMarkup(
        resize_keyboard=True,
        one_time_keyboard=True
    )

    for answer in question["answers"]:
        keyboard.add(types.KeyboardButton(answer))

    bot.send_message(
        message.chat.id,
        "🧠 Вікторина Formula World!\n\n" + question["question"],
        reply_markup=keyboard
    )


# Перевірка відповіді на вікторину
@bot.message_handler(func=lambda message: message.from_user.id in user_questions)
def check_answer(message):
    question = user_questions[message.from_user.id]

    if message.text == question["correct"]:
        bot.send_message(
            message.chat.id,
            "✅ Правильно! Чудові знання Формули-1!",
            reply_markup=types.ReplyKeyboardRemove()
        )
    else:
        bot.send_message(
            message.chat.id,
            "❌ Неправильно. Правильна відповідь: "
            + question["correct"],
            reply_markup=types.ReplyKeyboardRemove()
        )

    del user_questions[message.from_user.id]


# Запуск бота
print("Formula World Bot запущено!")
bot.infinity_polling()
