
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from sqlalchemy import text
from models import db

class UserBook(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey("book.id", ondelete="CASCADE"), nullable=False)
    status = db.Column(db.String(20), nullable=False, default="Not Started")  # Options: Not Started, Reading, Completed

    user = db.relationship("User", backref=db.backref("user_books", lazy=True))
    book = db.relationship("Book", backref=db.backref("book_users", lazy=True))