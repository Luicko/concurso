from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, TextField, validators, DateField
from wtforms.validators import DataRequired

class Regist_Form(Form):
	email = StringField('Email', validators=[DataRequired()])
	nickname = StringField('Nickname', validators=[DataRequired()])
	birthday = DateField('Birthday')

class Login_Form(Form):
	email = StringField('email')