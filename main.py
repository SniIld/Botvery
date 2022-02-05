#  Copyright (c) ChernV (@otter18), 2021.

import os
import random

import telebot
from setup import bot, logger
from webhook import app

# --------------- dialog params -------------------
dialog = {
    'hello': {
        'in': ['привет', 'hello', 'hi', 'privet', 'hey'],
        'out': ['Приветствую', 'Здравствуйте', 'Привет!', 'hello', 'hi', 'privet', 'hey']
    },
    'how r u': {
        'in': ['как дела', 'как ты', 'how are you'],
        'out': ['Хорошо', 'Отлично', 'Good. And how are u?', 'Зависть от того какие у тебя дела']
    },
    'name': {
        'in': ['зовут', 'name', 'имя'],
        'out': [
            'Я telegram-template-bot',
            'Я бот шаблон, но ты можешь звать меня в свой проект',
            'Это секрет. Используй команду /help, чтобы узнать'
        ]
    }
}


# --------------- bot -------------------
@bot.message_handler(commands=['help', 'start'])
def say_welcome(message):
    logger.info(f'</code>@{message.from_user.username}<code> ({message.chat.id}) used /start or /help')
    bot.send_message(
        message.chat.id,
        '<b>Hello! This is a telegram bot template written by <a href="https://github.com/otter18">otter18</a></b>',
        parse_mode='html'
    )


GamesForTwo = ['Селестия', 'Шахматы', 'Звёздная империя', 'Остров сокровищ', 'Домино', 'История',
               'Глубоководное приключение']
GameMoreTwo = ['Семь Чудес', 'Хадара', 'Селестия', 'Остров Котов', 'Лобатряс', 'Азул квадратный',
               'Остров сокровищ', 'Финка', 'Корова', 'Бликальчики', 'Черепашки', 'Мемология', 'Уно', 'Вампирчики',
               'Вантед', 'Билет на поезд', 'Пандемия', 'Средневековая академия', 'Атлантида', 'Азул ромбический',
               'Глубоководное приключение', 'Грядка', 'Нормы', 'История']
Player = ['Папа', 'Мама', 'Кирилл', 'Никита']


@bot.message_handler(commands=['game'])
def stratGameSelection(message):
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton(text='Два', callback_data='two player'))
    markup.add(telebot.types.InlineKeyboardButton(text='Больше двух', callback_data='more two player'))
    bot.send_message(message.chat.id, text="Сколько игроков будет играть?", reply_markup=markup)


@bot.message_handler(commands=["id"])
def get_id(message):
    logger.info(f'</code>@{message.from_user.username}<code> used /id')
    bot.send_message(message.chat.id, f"user_id = {message.chat.id}")


@bot.message_handler(func=lambda message: True)
def echo(message):
    for t, resp in dialog.items():
        if sum([e in message.text.lower() for e in resp['in']]):
            logger.info(f'</code>@{message.from_user.username}<code> ({message.chat.id}) used {t}:\n\n%s', message.text)
            bot.send_message(message.chat.id, random.choice(resp['out']))
            return

    logger.info(f'</code>@{message.from_user.username}<code> ({message.chat.id}) used echo:\n\n%s', message.text)
    bot.send_message(message.chat.id, message.text)


if __name__ == '__main__':
    if os.environ.get("IS_PRODUCTION", "False") == "True":
        app.run()
    else:
        bot.infinity_polling()
