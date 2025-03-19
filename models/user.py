from . import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    mobile = db.Column(db.String(15), unique=True, nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    gender = db.Column(db.String(10))
    dob = db.Column(db.String(20))
    address = db.Column(db.Text)
    profile_picture = db.Column(db.String(255), default="static/default.jpg")
    security_question = db.Column(db.String(255))
    security_answer = db.Column(db.String(255))

    def __repr__(self):
        return f"<User {self.username}>"
