from flask.ext.babel import lazy_gettext as __

from flask.ext.wtf import Form
from wtforms import (StringField, BooleanField, TextField,
         validators, DateField, SubmitField, PasswordField)

from .utils import RedirectForm

from .models import User


class RegistrationForm(Form):
    email = StringField(__('Email'), validators=[
            validators.DataRequired(), validators.Email()])
    nickname = StringField('Nickname', validators=[validators.DataRequired()])
    birthday = DateField('Birthday',  format='%m/%d/%Y')
    password = PasswordField('Password', 
        [validators.Required()])
    submit = SubmitField('Sign Up')


class LoginForm(Form):
    email = StringField('Email', validators=[
            validators.DataRequired(), validators.Email()])
    password = PasswordField('Password', validators=[validators.DataRequired()])
    submit = SubmitField('Login')

    def validate_email(self, field):
        self._user = User.query.filter_by(email=field.data).first()
        if self._user is None:
            raise validators.ValidationError("Username doesn't exists.")