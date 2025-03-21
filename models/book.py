from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from sqlalchemy import text
from models import db

class Book(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(100),nullable=False)
    semester=db.Column(db.Integer,nullable=True)