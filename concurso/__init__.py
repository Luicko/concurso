from __future__ import absolute_import

import os

from flask import Flask, request
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask_bootstrap import Bootstrap
from flask_debugtoolbar import DebugToolbarExtension
from flask.ext.mysql import MySQL
from flask.ext.babel import Babel


# Setup extensions

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('concurso.settings')
app.config.from_pyfile('settings.conf')

db = SQLAlchemy(app)

lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'

babel = Babel(app)
toolbar = DebugToolbarExtension(app)
Bootstrap(app)


from . import models, views, settings


@lm.user_loader
def load_user(id):
    """
    LoginManager callback to assign `current_user` proxy object.

    :param id: User ID
    :returns: :class:`User`
    """
    return models.User.query.get(int(id))


@babel.localeselector
def get_locale():
    """
    Locale selection callback.

    :returns: str
    """
    #user = getattr(g, 'user', None)
    #if user is not None:
    #    return user.locale
    return request.accept_languages.best_match(
        settings.LANGUAGES.keys())