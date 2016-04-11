import os

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config.from_object('concurso.settings')
db = SQLAlchemy(app)
Bootstrap(app)

lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'


from . import views, models


@lm.user_loader
def load_user(id):
	return models.User.query.get(int(id))
