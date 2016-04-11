from flask.ext.wtf import Form
from wtforms import (StringField, BooleanField, TextField,
         validators, DateField, SubmitField)


class Regist_Form(Form):
    email = StringField('Email', validators=[validators.DataRequired()])
    nickname = StringField('Nickname', validators=[validators.DataRequired()])
    birthday = DateField('Birthday')
    submit = SubmitField("Sign Up")


class Login_Form(Form):
    email = StringField('Email', validators=[validators.DataRequired()])
    submit = SubmitField("Login")
