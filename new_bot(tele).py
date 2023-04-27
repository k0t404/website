import telebot
from data import db_session
from config import BOT_TOKEN
from command import url, starts, helper, authorization, add_thing, question, delete_thing, one_thing, all_things


bot = telebot.TeleBot(BOT_TOKEN)
db_session.global_init("db/blogs.db")


@bot.message_handler(commands=['start'])
def start(message):
    starts(message)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):

    if message.text == '👋 Поздороваться' or message.text == 'РеАвторизация':
        bot.send_message(message.from_user.id, 'Для авторизации введите: Авторизация ваш email ваш пароль') #ответ бота

    elif 'Авторизация' in message.text:
        messag = message.text.split()
        authorization(messag, message)

    elif message.text == 'Ссылка на сайт':
        url(message)

    elif message.text == 'Задать вопрос':
        question(message)

    elif message.text == 'Удалить товар':
        bot.send_message(message.from_user.id, "Чтобы удалить товар ввидите: Удаление имя пользователя название товара")

    elif 'Удаление' in message.text:
        delete_thing(message.text.split(), message)

    elif message.text == 'Что может бот?':
        helper(message)

    elif message.text == 'Добавить товар':
        bot.send_message(message.from_user.id,
                         "Ввелите данные о товаре ввиде: Новый товар, ваше имя, название, описание, "
                         "приватен ли предмет для прсмотра, цена, ссылка на товар, категория")

    elif message.text == 'Вывести определённый товар':
        bot.send_message(message.from_user.id, "Ввелите данные о товаре ввиде: Поиск_1 ваше_имя товар")

    elif 'Поиск_1' in message.text:
        messag = message.text.split()
        one_thing(message, messag)

    elif 'Новый товар' in message.text:
        add_thing(message, message.text.split(', '))

    elif message.text == 'Вывести все товары':
        bot.send_message(message.from_user.id, "Для вывода всех товаров ввидите: Полный вывод ваше_имя")

    elif 'Полный' in message.text:
        all_things(message, message.text.split())


    else:
        bot.send_message(message.from_user.id, "Используйте клавиатуру")


bot.polling(none_stop=True, interval=0) #обязательная для работы бота часть
