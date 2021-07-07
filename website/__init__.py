from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from flask_mail import Mail, Message
from flask_recaptcha import ReCaptcha

db = SQLAlchemy()
DB_NAME = 'database.db'
recaptcha = ReCaptcha()


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret_key'

    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'

    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USERNAME'] = 'yagosik4@gmail.com'
    app.config['MAIL_PASSWORD'] = 'Yaronnoni301'  # HIDE
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True

    app.config.update(dict(
        RECAPTCHA_ENABLED=True,
        RECAPTCHA_SITE_KEY="6Lcr7n4bAAAAAGTb4eEcLKzYBt-jtMxPTHtdnorv",  #
        RECAPTCHA_SECRET_KEY="6Lcr7n4bAAAAAFtVS5AY73h36D0UrlHwFjT3C8aG",
    ))

    recaptcha.init_app(app)

    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Note

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('CREATED DATABASE!')
