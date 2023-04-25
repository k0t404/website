from telegram import ReplyKeyboardRemove
from telegram import ReplyKeyboardMarkup
from flask import redirect, render_template
import logging
from data.items import Items
from data.users import User
from flask_login import current_user
from data import db_session
# t.me/help_with_items_bot - ссылка на бота


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)

reply_keyboard = [['/all_things', '/one_thing'],
                      ['/delete_thing', '/add_thing']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)



async def start(update, context):
    await update.message.reply_text(
        "Я бот-справочник. Введите email и пароль от своего аккаунта",)
    print(update.message.text.split())
    email, password = update.message.text.split()
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.email == email).first()
    if user and user.check_password(password):
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
    await update.message.reply_text(reply_markup=markup)


async def all_things(update, context):
    await update.message.reply_text("Не готово")


async def echo(update, context):
    await update.message.reply_text(
        reply_markup=markup
    )


async def one_thing(update, context):
    await update.message.reply_text("Не готово")


async def delete_thing(update, context):
    await update.message.reply_text("Не готово")


async def add_thing(update, context):
    await update.message.reply_text("Ввелите данные о товаре ввиде: ваше имя, название, описание, приватен ли предмет для прсмотра, цена, ссылка на товар")
    name_user, title, content, is_private, price, link = update.message.text.split(', ')
    db_sess = db_session.create_session()
    title = db_sess.query(Items).filter(Items.title == title).first()
    if title:
        await update.message.reply_text('Товар уже присутствует')
        return ''
    items = Items()
    items.title = title
    items.content = content
    items.is_private = is_private
    items.price = price
    items.link = link
    items.creator = name_user
    current_user.items.append(items)
    db_sess.merge(current_user)
    db_sess.commit()
    title = db_sess.query(Items).filter(Items.title == title).first()
    if title:
        await update.message.reply_text('Товар добавлен успешно')
    await update.message.reply_text('Товар не добавлен,попробуйте заново')





async def close_keyboard(update, context):
    await update.message.reply_text(
        "Ok",
        reply_markup=ReplyKeyboardRemove()
    )