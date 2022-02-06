#  Copyright (c) ChernV (@otter18), 2021.

import os
import random

import telebot
from telebot import types
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
        'out': ['Хорошо', 'Отлично', 'Good. And how are u?', 'Идеально', 'Все тип-топ']
    },
    'name': {
        'in': ['зовут', 'name', 'имя'],
        'out': [
            'Я telegram-template-bot',
            'Я бот шаблон, но ты можешь звать меня в свой проект',
            'Это секрет. Используй команду /help, чтобы узнать'
        ]
    },
    'repetition': {
        'in': ['почему ты повторяешь', 'повторюха муха'],
        'out': ['Что поделать?', 'Вот такой я', 'Это создатель виноват', 'Спроси создателя']
    }
}


# --------------- bot -------------------
@bot.message_handler(commands=['help', 'info'])
def say_welcome(message):
    # logger.info(f'</code>@{message.from_user.username}<code> ({message.chat.id}) used /start or /help')
    keyboard = types.InlineKeyboardMarkup()
    url_button = types.InlineKeyboardButton(text="Написанный otter18", url="https://github.com/otter18")
    keyboard.add(url_button)
    bot.send_message(message.chat.id, "Привет! Это шаблон телеграмм бота", reply_markup=keyboard)


GamesForTwo = ['Селестия', 'Шахматы', 'Звёздная империя', 'Остров сокровищ', 'Домино', 'История',
               'Глубоководное приключение', 'Микро-Макро']
GameMoreTwo = ['Семь Чудес', 'Хадара', 'Селестия', 'Остров Котов', 'Лобатряс', 'Азул квадратный',
               'Остров сокровищ', 'Финка', 'Корова', 'Бликальчики', 'Черепашки', 'Мемология', 'Уно', 'Вампирчики',
               'Вантед', 'Билет на поезд', 'Пандемия', 'Средневековая академия', 'Атлантида', 'Азул ромбический',
               'Глубоководное приключение', 'Грядка', 'Нормы', 'История', 'Микро-Макро']
Player = ['Папа', 'Мама', 'Кирилл', 'Никита']


@bot.message_handler(commands=['game'])
def stratGameSelection(message):
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton(text='Два', callback_data='two player'))
    markup.add(telebot.types.InlineKeyboardButton(text='Больше двух', callback_data='more two player'))
    markup.add(telebot.types.InlineKeyboardButton(text='Выбрать кто первый', callback_data='choice player'))
    bot.send_message(message.chat.id, text="Сколько игроков будет играть?", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    answer = ''
    if call.data == 'two player':
        answer = f'Botvery выбрал {random.choice(GamesForTwo)}'
    elif call.data == 'more two player':
        answer = f'Botvery выбрал {random.choice(GameMoreTwo)}'
    elif call.data == 'choice player':
        answer = f'Botvery выбрал игрока {random.choice(Player)}'

    bot.send_message(call.message.chat.id, answer)
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)


@bot.message_handler(commands=['subject'])
def subjectSelection(message):
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton(text='Англ', callback_data='English'))
    markup.add(telebot.types.InlineKeyboardButton(text='Математика', callback_data='Math'))
    markup.add(telebot.types.InlineKeyboardButton(text='Физика', callback_data='Physics'))
    bot.send_message(message.chat.id, text='Выберите школьный предмет:', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def answerSubjectSelection(call):
    answer = ''
    if call.data == 'English':
        answer = 'https://i.postimg.cc/gj6fhTjB/photo-2022-02-05-20-46-24.jpg'
    elif call.data == 'Math':
        answer = 'Это Математика'
    elif call.data == 'Physics':
        answer = 'Это Физика'
    bot.send_message(call.message.chat.id, answer)


@bot.message_handler(commands=["id"])
def get_id(message):
    # logger.info(f'</code>@{message.from_user.username}<code> used /id')
    bot.send_message(message.chat.id, f"user_id = {message.chat.id}")


@bot.message_handler(func=lambda message: True)
def echo(message):
    for t, resp in dialog.items():
        if sum([e in message.text.lower() for e in resp['in']]):
            # logger.info(f'</code>@{message.from_user.username}<code> ({message.chat.id}) used {t}:\n\n%s', message.text)
            bot.send_message(message.chat.id, random.choice(resp['out']))
            return

    # logger.info(f'</code>@{message.from_user.username}<code> ({message.chat.id}) used echo:\n\n%s', message.text)
    bot.send_message(message.chat.id, message.text)


if __name__ == '__main__':
    if os.environ.get("IS_PRODUCTION", "False") == "True":
        app.run()
    else:
        bot.infinity_polling()

#   ---------------------------------------------ПЛАНЫ------------------------------------------------------
#   1) Создать помощник английского
#   2) Создать помощник физики
#   3) Создать помощник математики
#   4) Сделать вывод определенной информации, в определенное время
