
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from sqlalchemy import text
from models import db

class TargetSetting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    start_date = db.Column(db.Date, nullable=False)  # Start of the week
    end_date = db.Column(db.Date, nullable=False)  # End of the week
    book_reading_hours = db.Column(db.Float, default=0)  # In hours
    personal_hearing_hours = db.Column(db.Float, default=0)  # In hours
    study_hours = db.Column(db.Float, default=0)  # In hours
    college_classes = db.Column(db.Integer, default=0)  # Number of classes
   
    user = db.relationship("User", backref=db.backref("target_settings", lazy=True))