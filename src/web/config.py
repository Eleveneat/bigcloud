# -*- encoding: utf-8 -*-
# Copyright 2016 Vinzor Co.,Ltd.
#
# Flask config
#
# All configuration items that could not be change in runtime, should be placed
# here. Otherwise, they should be stored in database and updated by the
# administrators in runtime.
#
# 2016/2/16 Chen Weijian : Init

import os
from werkzeug.security import generate_password_hash as gen_hash

basedir = os.path.abspath((os.path.dirname(__file__)))


def from_env(key, default=None):
    return os.environ.get(key, default=default)


def from_env_int(key, default=0):
    value = from_env(key)
    try:
        return int(value)
    except:
        pass
    return default


def from_env_bool(key, default=False, ignore_case=True):
    true_values = ['True', 'T', 'Yes', 'Y', 'Ok', 'O']
    upper_true_values = [i.upper() for i in true_values]
    value = from_env(key)
    if value is not None and ignore_case:
        return value.upper() in upper_true_values
    else:
        return value in true_values


class Config:
    SECRET_KEY = from_env('SECRET_KEY', gen_hash('TOP_SECRET'))
    MAX_CONTENT_LENGTH = from_env_int('MAX_CONTENT_LENGTH', 10485760)

    # sqlalchemy
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = from_env('SQLALCHEMY_DATABASE_URI')

    # wtf and csrf
    WTF_CSRF_ENABLED = False
    WTF_CSRF_METHODS = ['PUT', 'POST', 'PATCH', 'DELETE']

    # i18n
    LANGUAGES = {
        'en': 'English',
        'zh': 'Chinese',
    }

    @classmethod
    def init_app(cls, app):
        pass


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:admin123@localhost:3306/bigcloud_cwj?charset=utf8'
    # DEBUG = True
    # SQLALCHEMY_ECHO = True
    # SQLALCHEMY_DATABASE_URI = from_env('SQLALCHEMY_DATABASE_URI') or \
    #      'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')
    # CELERY_RESULT_BACKEND = from_env('CELERY_RESULT_BACKEND') or \
    #     'db+sqlite:///' + os.path.join(basedir, 'celery-dev.sqlite')
    # CELERY_ALWAYS_EAGER = False     # enable this to debug celery task


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = from_env('SQLALCHEMY_DATABASE_URI') or \
                              'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')
    # CELERY_RESULT_BACKEND = from_env('CELERY_RESULT_BACKEND') or \
    #     'db+sqlite:///' + os.path.join(basedir, 'celery-test.sqlite')
    # PRESERVE_CONTEXT_ON_EXCEPTION = True


class ProductConfig(Config):
    SQLALCHEMY_DATABASE_URI = from_env('SQLALCHEMY_DATABASE_URI') or \
                              'sqlite:///' + os.path.join(basedir, 'data.sqlite')
    # CELERY_RESULT_BACKEND = from_env('CELERY_RESULT_BACKEND') or \
    #     'db+sqlite:///' + os.path.join(basedir, 'celery.sqlite')
    # SSL_DISABLE = from_env_bool('SSL_DISABLE', False)


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'product': ProductConfig,

    'default': DevelopmentConfig,
}
