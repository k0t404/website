from telegram import ReplyKeyboardRemove
from telegram import ReplyKeyboardMarkup
from flask import redirect, render_template
from data.items import Items
from data.users import User
from flask_login import current_user
from data import db_session
import flask
import os
from flask import Flask, redirect, render_template, make_response, request, session, abort
import datetime
from data.items import Items
from data.users import User
from form.user import LoginForm, RegisterForm, ItemsForm
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from data import db_session, items_api, items_resources, users_resources
from flask_restful import Api
import logging
from telegram.ext import Application, MessageHandler, filters
from config import BOT_TOKEN
from telegram.ext import CommandHandler
from command import close_keyboard, start, all_things, one_thing, delete_thing, add_thing, helper

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
    await update.message.reply_text("Ввелите данные о товаре ввиде: ваш мейл, название, описание, приватен ли предмет для прсмотра, цена, ссылка на товар")
    email, title, content, is_private, price, link = update.message.text.split(', ')
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
    items.creator = email
    current_user.items.append(items)
    db_sess.merge(current_user)
    db_sess.commit()
    title = db_sess.query(Items).filter(Items.title == title).first()
    if title:
        await update.message.reply_text('Товар добавлен успешно')
        return ''
    await update.message.reply_text('Товар не добавлен,попробуйте заново')
    return ''





async def close_keyboard(update, context):
    await update.message.reply_text(
        "Ok",
        reply_markup=ReplyKeyboardRemove()
    )

def main():
    db_session.global_init("db/blogs.db")
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", helper))
    application.add_handler(CommandHandler("all_things", all_things))
    application.add_handler(CommandHandler("one_thing", one_thing))
    application.add_handler(CommandHandler("delete_thing", delete_thing))
    application.add_handler(CommandHandler("add_thing", add_thing))

    text_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, add_thing)

    # Регистрируем обработчик в приложении.
    application.add_handler(text_handler)

    # Запускаем приложение.
    application.run_polling()


if __name__ == '__main__':
    main()