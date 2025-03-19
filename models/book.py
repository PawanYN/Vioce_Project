from . import db

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    cover_image = db.Column(db.String(255), nullable=True)

    def __repr__(self):
        return f"<Book {self.title}>"

class UserBook(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey("book.id"), nullable=False)
    status = db.Column(db.String(50), default="Not Started")  # "Not Started", "Reading", "Completed"

    user = db.relationship("User", backref="books")
    book = db.relationship("Book", backref="users")

    def __repr__(self):
        return f"<UserBook {self.user_id} - {self.book_id}>"
