from flask.ext.wtf import Form
from wtforms import (StringField, BooleanField, TextField,
         validators, DateField, SubmitField)
from wtforms.validators import DataRequired


class Regist_Form(Form):
    email = StringField('Email', validators=[DataRequired()])
    nickname = StringField('Nickname', validators=[DataRequired()])
    birthday = DateField('Birthday')
    submit = SubmitField("Sign Up")


class Login_Form(Form):
    email = StringField('email')
