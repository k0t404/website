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
from command import help_command, date, time, address, phone, help, site, work_time, echo, close_keyboard, start


app = Flask(__name__)
api = Api(app)
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(
    days=365
)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


@app.errorhandler(404)
def not_found(error):
    return make_response(flask.jsonify({'error': 'Not found'}), 404)


@app.errorhandler(400)
def bad_request(_):
    return make_response(flask.jsonify({'error': 'Bad Request'}), 400)


@app.route("/")
def index():
    db_sess = db_session.create_session()
    if current_user.is_authenticated:
        items = db_sess.query(Items).filter(
            (Items.user == current_user) | (Items.is_private != True))
    else:
        items = db_sess.query(Items).filter(Items.is_private != True)
    return render_template("index.html", items=items)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/account")
def account():
    db_sess = db_session.create_session()
    if current_user.is_authenticated:
        items = db_sess.query(Items).filter(
            (Items.user == current_user) | (Items.is_private != True))
    else:
        items = None
    return render_template("account.html", items=items)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route("/cookie_test")
def cookie_test():
    visits_count = int(request.cookies.get("visits_count", 0))
    if visits_count:
        res = make_response(
            f"Вы пришли на эту страницу {visits_count + 1} раз")
        res.set_cookie("visits_count", str(visits_count + 1),
                       max_age=60 * 60 * 24 * 365 * 2)
    else:
        res = make_response(
            "Вы пришли на эту страницу в первый раз за последние 2 года")
        res.set_cookie("visits_count", '1',
                       max_age=60 * 60 * 24 * 365 * 2)
    return res


@app.route("/session_test")
def session_test():
    visits_count = session.get('visits_count', 0)
    session['visits_count'] = visits_count + 1
    return make_response(
        f"Вы пришли на эту страницу {visits_count + 1} раз")


@app.route('/items/<int:id>',  methods=['GET', 'POST'])
@login_required
def add_items(id):
    form = ItemsForm()
    db_sess = db_session.create_session()
    info = db_sess.query(Items).filter(Items.id == id).first()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        items = Items()
        items.title = form.title.data
        items.content = form.content.data
        items.is_private = form.is_private.data
        items.price = info.price
        items.link = info.link
        items.creator = info.user.name
        current_user.items.append(items)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/')
    return render_template('items.html', title='Добавление в отслеживаемое', form=form)


@app.route('/items_add',  methods=['GET', 'POST'])
@login_required
def add_new_items():
    form = ItemsForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        items = Items()
        items.title = form.title.data
        items.content = form.content.data
        items.is_private = form.is_private.data
        items.price = form.price.data
        items.link = form.link.data
        items.creator = current_user.name
        current_user.items.append(items)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/')
    return render_template('items_add.html', title='Создать отслеживаемое', form=form)


@app.route('/items_edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_items(id):
    form = ItemsForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        items = db_sess.query(Items).filter(Items.id == id, Items.user == current_user).first()
        if items:
            form.title.data = items.title
            form.content.data = items.content
            form.is_private.data = items.is_private
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        items = db_sess.query(Items).filter(Items.id == id, Items.user == current_user).first()
        if items:
            items.title = form.title.data
            items.content = form.content.data
            items.is_private = form.is_private.data
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('items_edit.html',
                           title='Редактирование отслеживаемого',
                           form=form
                           )


@app.route('/items_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def items_delete(id):
    db_sess = db_session.create_session()
    items = db_sess.query(Items).filter(Items.id == id,
                                      Items.user == current_user
                                      ).first()
    if items:
        db_sess.delete(items)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html', message="Неправильный логин или пароль", form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация', form=form, message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация', form=form, message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/')
    return render_template('register.html', title='Регистрация', form=form)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)
logger = logging.getLogger(__name__)

# Определяем функцию-обработчик сообщений.
# У неё два параметра, updater, принявший сообщение и контекст - дополнительная информация о сообщении.


def main():
    db_session.global_init("db/blogs.db")

    '''db_sess = db_session.create_session()
    user = User()
    user.id = 1
    user.name = 'Ridley'
    user.about = 'f'
    user.hashed_password = 'w12'
    user.email = 'scott_chief@mars.org'

    db_sess.add(user)

    user = User()
    user.name = 'Riley'
    user.about = 'ff'
    user.hashed_password = 'w12f'
    user.email = 'scott_chief@mafrs.org'

    db_sess.add(user)
    db_sess.commit()
    
    items = Items()
    items.title = 'fssfe'
    items.content = 'smth'
    items.created_date = datetime.date.today()
    items.is_private = False
    items.user_id = 1
    items.price = 500
    items.creator =  'Ridley'

    db_sess.add(items)

    items = Items()
    items.title = 'dee'
    items.content = 'ge'
    items.created_date = datetime.date.today()
    items.is_private = False
    items.user_id = 3
    items.price = 500
    items.creator = 'q'

    db_sess.add(items)

    items = Items()
    items.title = 'fike'
    items.content = 'yhjh'
    items.created_date = datetime.date.today()
    items.is_private = False
    items.user_id = 4
    items.price = 500
    items.creator = 'admin'

    db_sess.add(items)
    db_sess.commit()'''

    api.add_resource(users_resources.UsersListResource, '/api/v2/users')
    api.add_resource(users_resources.UsersResource, '/api/v2/users/<int:users_id>')
    api.add_resource(items_resources.ItemListResource, '/api/v2/items')
    api.add_resource(items_resources.ItemResource, '/api/v2/items/<int:items_id>')
    app.register_blueprint(items_api.blueprint)
    app.run()

    "-------------BOT_____BOT-----BOT_____BOT-----BOT_____BOT-------------"
    # Создаём объект Application.
    # Вместо слова "TOKEN" надо разместить полученный от @BotFather токен
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("date", date))
    application.add_handler(CommandHandler("time", time))
    application.add_handler(CommandHandler("address", address))
    application.add_handler(CommandHandler("phone", phone))
    application.add_handler(CommandHandler("site", site))
    application.add_handler(CommandHandler("work_time", work_time))
    application.add_handler(CommandHandler("help", help))
    application.add_handler(CommandHandler("close", close_keyboard))

    text_handler = MessageHandler(filters.TEXT, echo)

    # Регистрируем обработчик в приложении.
    application.add_handler(text_handler)

    # Запускаем приложение.
    application.run_polling()


if __name__ == '__main__':
    main()
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
