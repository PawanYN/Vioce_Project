from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .user import User
from .book import Book
from .userbook import UserBook
from .sadhana import Sadhana
from .target_setting import TargetSetting
