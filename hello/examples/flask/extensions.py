# -*- coding: utf-8 -*-

# from flask_sqlalchemy import SQLAlchemy
#
# db = SQLAlchemy()

from flask_mail import Mail

mail = Mail()

from flask_cache import Cache

cache = Cache()

from flask_login import LoginManager

login_manager = LoginManager()

from flask_openid import OpenID

oid = OpenID()

from flask_jwt import JWT

jwt = JWT()

# email info
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
