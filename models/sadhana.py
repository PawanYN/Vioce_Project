from . import db

class Sadhana(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    date = db.Column(db.Date, nullable=False)
    chanting_count = db.Column(db.Integer, nullable=False)
    reading_hours = db.Column(db.Float, nullable=False)
    wakeup_time = db.Column(db.String(10))
    notes = db.Column(db.Text)

    user = db.relationship("User", backref="sadhana_entries")

    def __repr__(self):
        return f"<Sadhana {self.user_id} - {self.date}>"
