import datetime
from telegram import ReplyKeyboardRemove
from telegram import ReplyKeyboardMarkup


async def start(update, context):
    reply_keyboard = [['/address', '/phone'],
                      ['/site', '/work_time']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
    await update.message.reply_text(
        "Я бот-справочник. Какая информация вам нужна?",
        reply_markup=markup
    )


async def help_command(update, context):
    """Отправляет сообщение когда получена команда /help"""
    await update.message.reply_text("Я пока не умею помогать... Я только ваше эхо.")


async def date(update, context):
    """Отправляет сообщение когда получена команда /date"""
    dt = datetime.datetime.now()
    date = str(dt).split()[0]
    await update.message.reply_text(date)


async def time(update, context):
    """Отправляет сообщение когда получена команда /time"""
    dt = datetime.datetime.now()
    time = str(dt).split()[1]
    await update.message.reply_text(time)


async def help(update, context):
    await update.message.reply_text(
        "Я бот справочник.")


async def address(update, context):
    await update.message.reply_text(
        "Адрес: г. Москва, ул. Льва Толстого, 16")


async def phone(update, context):
    await update.message.reply_text("Телефон: +7(495)776-3030")


async def site(update, context):
    await update.message.reply_text(
        "Сайт: http://www.yandex.ru/company")


async def work_time(update, context):
    await update.message.reply_text(
        "Время работы: круглосуточно.")


async def echo(update, context):
    # У объекта класса Updater есть поле message,
    # являющееся объектом сообщения.
    # У message есть поле text, содержащее текст полученного сообщения,
    # а также метод reply_text(str),
    # отсылающий ответ пользователю, от которого получено сообщение.
    await update.message.reply_text(f'Я получил сообщение {update.message.text}')


async def close_keyboard(update, context):
    await update.message.reply_text(
        "Ok",
        reply_markup=ReplyKeyboardRemove()
    )