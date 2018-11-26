# -*- coding: utf-8 -*-

from flask_babel import Babel

# from flask_sqlalchemy import SQLAlchemy
#
# db = SQLAlchemy()

from flask_mail import Mail

mail = Mail()

# from flask_cache import Cache
#
# cache = Cache(config={'CACHE_TYPE': 'simple'})

from flask_login import LoginManager

login_manager = LoginManager()

from flask_openid import OpenID

oid = OpenID()

from flask_jwt import JWT

jwt = JWT()

# email info, ref: https://pythonhosted.org/Flask-Mail/
from flask_mail import Message

def mail_send_helper(sender_name, sender_address, address, subject, body):
    try:
        msg = Message(
            subject,
            sender=(sender_name, sender_address),
            recipients=address)
        msg.body = body
        mail.send(msg)
        return True
    except:
        return False


def load_extensions(app):
    # flask-sqlalchemy
    # db.init_app(app)

    # flask-mail
    mail.init_app(app)

    # flask-cache
    # cache.init_app(app)

    # flask-babel
    babel = Babel(app)

    @babel.localeselector
    def get_locale():
        accept_languages = app.config.get('ACCEPT_LANGUAGES')
        return request.accept_languages.best_match(accept_languages)

    # flask-login
    login_manager.login_view = 'frontend.login'
    login_manager.refresh_view = 'frontend.reauth'

    @login_manager.user_loader
    def load_user(id):
        from imbalance.examples.flask.user.models import User
        user = User()
        user = user.get_by_id(id)
        if user is not None:
            session['id'] = str(user.id)
        else:
            session['id'] = -1
        return user

    login_manager.init_app(app)

    # flask-openid
    oid.init_app(app)

    # flask_jwt
    # jwt.init_app(app)
    pass