# -*- conding: utf-8 -*-
import os

_basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG=True

SECRET_KEY = 'you-will-never-guess'

WTF_CSRF_ENABLED = True

LANGUAGES = {
    'en': 'English',
    'es': 'Espanol'
}

SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = 'mysql://Concurso:root@localhost/Discos'
#SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(_basedir, '../instance/app.db')