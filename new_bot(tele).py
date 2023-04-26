import telebot
from config import BOT_TOKEN
from telebot import types
from link_to_site import link
from data.users import User
from data import db_session

bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=['start'])
def start(message):

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("👋 Поздороваться")
    markup.add(btn1)
    bot.send_message(message.from_user.id, "👋 Привет! Я твой бот-сборщик товаров!", reply_markup=markup)


def url(message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text='Наш сайт', url=f'{link}')
    markup.add(btn1)
    bot.send_message(message.from_user.id, "По кнопке ниже можно перейти на наш сайт")


@bot.message_handler(content_types=['text'])
def get_text_messages(message):

    if message.text == '👋 Поздороваться' or message.text == 'РеАвторизация':
        bot.send_message(message.from_user.id, 'Для авторизации введите: Авторизация {ваш email} {ваш пароль}') #ответ бота

    elif 'Авторизация' in message.text.split():
        pop, email, password = message.text.split()
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == email).first()
        if user and user.check_password(password):
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)  # создание новых кнопок
            btn1 = types.KeyboardButton('Что может бот?')
            btn4 = types.KeyboardButton('Ссылка на сайт')
            btn2 = types.KeyboardButton('Добавить товар')
            btn3 = types.KeyboardButton('Удалить товар')
            btn5 = types.KeyboardButton('Вывести определённый товар')
            btn6 = types.KeyboardButton('Вывести все товары')
            markup.add(btn1, btn2, btn3, btn4, btn6, btn5)
            bot.send_message(message.from_user.id, 'Вы прошли авторизацию, выберите действие', reply_markup=markup)
        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn6 = types.KeyboardButton('РеАвторизация')
            markup.add(btn6)
            bot.send_message(message.from_user.id, 'Неправильная почта или пароль, попробуйте заново', reply_markup=markup)