import os

__author__ = 'litl'

SECRET_KEY = os.urandom(24)
CMS_USER_ID = 'abcdefg'

DEBUG = True
# DB_URI = "mysql+pymysql://root:123456@127.0.0.1:3306/bbs?charset=utf8"

SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://root:123456@127.0.0.1:3306/bbs?charset=utf8"
SQLALCHEMY_TRACK_MODIFICATIONS = False

MAIL_SERVER = "SMTP.qq.com"
MAIL_PORT = "587"
MAIL_USE_TLS = True
# MAIL_USE_SSL
MAIL_USERNAME = "407378019@qq.com"
MAIL_PASSWORD = "ctgndqbvakyabgda"
MAIL_DEFAULT_SENDER = "407378019@qq.com"

CACHE_TYPE = 'redis'
CACHE_REDIS_HOST = '10.10.10.87'
CACHE_REDIS_PORT = 6379
CACHE_REDIS_DB = ''
CACHE_REDIS_PASSWORD = '123456'

CELERY_RESULT_BACKEND = "redis://:123456@10.10.10.87:6379/0"
CELERY_BROKER_URL = "redis://:123456@10.10.10.87:6379/0"

ALIDAYU_APP_KEY = 'LTAI4Fry3Po5CGFvSJuPaWGe'
ALIDAYU_APP_SECRET = 'wA3oVPbcH8u8uJtjYORX4hoUcJip7Z'
ALIDAYU_SIGN_NAME = 'bbs论坛'
ALIDAYU_TEMPLATE_CODE = 'SMS_180055247'

FRONT_USER_ID = 'FFFF'

UEDITOR_UPLOAD_PATH = os.path.join(os.path.dirname(__file__), 'images')

CMS_PER_PAGE = 10
PER_PAGE = 10