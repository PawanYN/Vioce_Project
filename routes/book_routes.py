
from flask import Flask,Blueprint, render_template, redirect, url_for, request, flash,session
from flask_login import login_required
from models.book import Book
from models.userbook import UserBook

book_routes = Blueprint('book_routes', __name__)

@book_routes.route('/user_book', methods=["GET", "POST"])
def user_books():
    if "user_id" not in session:
        return redirect(url_for("login"))  # Redirect if not logged in

    user_id = session["user_id"]
    books = Book.query.all()

    # Fetch the user's current book statuses
    user_books = {ub.book_id: ub.status for ub in UserBook.query.filter_by(user_id=user_id).all()}

    if request.method == "POST":
        for book in books:
            status = request.form.get(f"book_{book.id}", "Not Started")  # Default to "Not Started"

            # Check if the user already has an entry for this book
            user_book = UserBook.query.filter_by(user_id=user_id, book_id=book.id).first()

            if user_book:
                user_book.status = status  # Update status
            else:
                new_user_book = UserBook(user_id=user_id, book_id=book.id, status=status)
                db.session.add(new_user_book)

        db.session.commit()
        flash("Book statuses updated successfully!", "success")
        return redirect(url_for("user_books"))

    return render_template("user_books.html", books=books, user_books=user_books)


@book_routes.route('/add_book', methods=["POST"])
@login_required
def add_book():
    if "user_id" not in session:
        return redirect(url_for("login"))

    book_name = request.form["book_name"]
    semester = request.form["semester"]

    new_book = Book(name=book_name, semester=int(semester))
    db.session.add(new_book)
    db.session.commit()

    flash("Book added successfully!", "success")
    return redirect(url_for("controler"))

@book_routes.route('/delete_book/<int:book_id>')
@login_required
def delete_book(book_id):
    if "user_id" not in session:
        return redirect(url_for("login"))
    
    # Delete related user_book records first
    UserBook.query.filter_by(book_id=book_id).delete()
    
    # Now delete the book
    book = Book.query.get(book_id)
    if book:
        db.session.delete(book)
        db.session.commit()
        flash("Book deleted successfully!", "success")

    return redirect(url_for("controler"))