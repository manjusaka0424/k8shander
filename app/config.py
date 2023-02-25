import os
from kombu import Queue, Exchange
basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig:
    SECRET_KEY = b'_5#y2L"F4Q8z\n\xec]flask_app/'
    DEBUG = False
    TESTING = False
    DATABASE_URI = 'sqlite:///:memory:'

    # Flask-Security setup
    SECURITY_LOGIN_WITHOUT_CONFIRMATION = True
    SECURITY_REGISTERABLE = True
    SECURITY_SEND_REGISTER_EMAIL = True
    SECURITY_RECOVERABLE = True
    SECURITY_URL_PREFIX = '/account'

    SECURITY_PASSWORD_HASH = 'pbkdf2_sha512'
    SECURITY_PASSWORD_SALT = "ATGUOHAELKiubahiughaerGOJAEGj"
    SECURITY_TRACKABLE = True
    SECURITY_CONFIRMABLE = True
    SECURITY_BLUEPRINT_NAME = "security"

    DEBUG_TB_INTERCEPT_REDIRECTS = False

    JWT_SECRET_KEY = 'a3f@>da12sr$482jLdg+#d'
    JWT_ACCESS_TOKEN_EXPIRES = 24*3600  # default value is 15 minutes
    JWT_REFRESH_TOKEN_EXPIRES = 30*24*3600  # default value is 30 days
    JWT_BLACKLIST_ENABLED = True
    JWT_IDENTITY_CLAIM = 'sub'
    JWT_TOKEN_LOCATION = ["headers", "cookies"]
    JWT_COOKIE_SECURE = False

    SQLALCHEMY_ECHO = False
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True

    SLOW_QUERY_THRESHOLD = 1

    ALIYUN_ACCESS_KEY = ""
    ALIYUN_ACCESS_SECRET = ""


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')


class TestingConfig(DevelopmentConfig):
    pass


class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'mysql://deploy:deploy@wz_123@localhost/analysis'


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
