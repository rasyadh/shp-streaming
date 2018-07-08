import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    DEBUG       = False
    TESTING     = False
    CSRF_ENABLED= True
    SECRET_KEY  = 'streamshp'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///streamshp.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProductionConfig(Config):
    DEBUG = False

class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True

class TestingConfig(Config):
    TESTING = True