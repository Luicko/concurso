# -*- encoding: utf-8 -*-

import os

_basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = False

SECRET_KEY = 'you-will-never-guess'

SQLALCHEMY_TRACK_MODIFICATIONS = False

WTF_CSRF_ENABLED = True

LANGUAGES = {
    'en': 'English',
    'es': 'Español'
}