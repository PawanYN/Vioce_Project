from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Import Models
from .user import User
from .book import Book, UserBook
from .sadhana import Sadhana
