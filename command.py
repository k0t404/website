from telegram import ReplyKeyboardRemove
from data.users import User
from data import db_session
from telegram import ReplyKeyboardMarkup
# t.me/help_with_items_bot - ссылка на бота


async def start(update, context):
    await update.message.reply_text(
        "Я бот-справочник. Введите email и пароль от своего аккаунта",
        # reply_markup=markup
    )
    email, password = update.message.text.split()
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.email == email).first()
    if user and user.check_password(password):
        reply_keyboard = [['/Вывести все ваши товары', '/Вывести определенный ваш товар'],
                          ['/Удалить товар', '/Добавить товар', '/Помощь']]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
        await update.message.reply_text(
            "Вы прошли авторизацию. Выберите действие с отслеживаемыми товарами",
            reply_markup=markup
        )
    else:
        await update.message.reply_text('Неправильный логин или пароль')


async def helper(update, context):
    await update.message.reply_text("Я бот-справочник.")
    await update.message.reply_text("Я могу:")
    await update.message.reply_text("Вывести все выбранные вами товары")
    await update.message.reply_text("Вывести определенный выбранный вами товар")
    await update.message.reply_text("Добавить товар")
    await update.message.reply_text("Удaлить товар")
    reply_keyboard = [['Вывести все ваши товары', 'Вывести определенный ваш товар'],
                      ['Удалить товар', 'Добавить товар']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
    await update.message.reply_text(
        reply_markup=markup
    )


async def all_things(update, context):
    await update.message.reply_text("Не готово")


async def one_thing(update, context):
    await update.message.reply_text("Не готово")


async def delete_thing(update, context):
    await update.message.reply_text("Не готово")


async def add_thing(update, context):
    await update.message.reply_text("Не готово")


async def close_keyboard(update, context):
    await update.message.reply_text(
        "Ok",
        reply_markup=ReplyKeyboardRemove()
    )