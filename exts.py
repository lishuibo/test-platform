from flask_cache import Cache
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from utils.alidayu import AlidayuAPI

__author__ = 'litl'
db = SQLAlchemy()
mail = Mail()
cache = Cache()
alidayu = AlidayuAPI()