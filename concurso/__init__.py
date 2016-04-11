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


@app.before_request
def before_request():
	g.user = current_user


@lm.user_loader
def load_user(id):
	return User.query.get(int(id))


from . import views, models