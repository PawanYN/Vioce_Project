from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from sqlalchemy import text
from models import db

class Sadhana(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    date = db.Column(db.Date, nullable=False, unique=True)  # Date of entry
    nidra_to_bed = db.Column(db.Integer, default=0)
    nidra_wakeup = db.Column(db.Integer, default=0)
    nidra_day_sleep = db.Column(db.Integer, default=0)
    japa = db.Column(db.Integer, default=0)
    pathan_books = db.Column(db.Integer, default=0)
    hearing = db.Column(db.Integer, default=0)
    counselor_class = db.Column(db.Integer, default=0)
    mangal_arati = db.Column(db.Integer, default=0)
    morning_class = db.Column(db.Integer, default=0)
    study_target = db.Column(db.Integer, default=0)
    college_class = db.Column(db.Integer, default=0)
    cleanliness = db.Column(db.Integer, default=0)
    sadhana_card_filled = db.Column(db.Integer, default=0)
    cleaning_alloted_area = db.Column(db.Integer, default=0)

    user = db.relationship("User", backref=db.backref("sadhana_records", lazy=True))
