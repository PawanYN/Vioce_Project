from flask import render_template, request, redirect, url_for, flash, session
from . import book_bp
from app import db
from models import Book, UserBook

@book_bp.route("/user_books", methods=["GET", "POST"])
def user_books():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))  

    user_id = session["user_id"]
    books = Book.query.all()
    user_books = {ub.book_id: ub.status for ub in UserBook.query.filter_by(user_id=user_id).all()}

    if request.method == "POST":
        for book in books:
            status = request.form.get(f"book_{book.id}", "Not Started")
            user_book = UserBook.query.filter_by(user_id=user_id, book_id=book.id).first()
            
            if user_book:
                user_book.status = status
            else:
                new_user_book = UserBook(user_id=user_id, book_id=book.id, status=status)
                db.session.add(new_user_book)

        db.session.commit()
        flash("Book statuses updated successfully!", "success")
        return redirect(url_for("book.user_books"))

    return render_template("user_books.html", books=books, user_books=user_books)
