from flask import Flask, render_template, request, redirect, url_for, flash,session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from sqlalchemy import text

from datetime import date, datetime, timedelta

import os

app = Flask(__name__)

# Configuration
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "108"

# Initialize Database & Bcrypt
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)


# User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    mobile = db.Column(db.String(15), unique=True, nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    gender = db.Column(db.String(10))
    dob = db.Column(db.String(10))
    address = db.Column(db.String(255))
    profile_picture = db.Column(db.String(255))
    security_question = db.Column(db.String(100))
    security_answer = db.Column(db.String(100))

class Book(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(100),nullable=False)
    semester=db.Column(db.Integer,nullable=True)

# New Table to Track User's Book Reading Status
class UserBook(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey("book.id", ondelete="CASCADE"), nullable=False)
    status = db.Column(db.String(20), nullable=False, default="Not Started")  # Options: Not Started, Reading, Completed

    user = db.relationship("User", backref=db.backref("user_books", lazy=True))
    book = db.relationship("Book", backref=db.backref("book_users", lazy=True))
    
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
    

# with app.app_context():
#     db.session.execute(text("DROP TABLE IF EXISTS Target_Setting;"))
#     db.session.commit()
#     print("✅ TargetSetting table dropped and recreated successfully!")


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



# Apply changes
with app.app_context():
    db.create_all()

@app.context_processor
def inject_user():
    user=None
    if "user_id" in session:
        user = User.query.get(session["user_id"])
    return dict(user=user,date=date)


@app.context_processor
def inject_utilities():
    return dict(timedelta=timedelta, date=date)

# Login Route
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            session["user_id"] = user.id
            session["username"] = user.username
            session["profile_picture"] = user.profile_picture
            return redirect(url_for("home"))
        else:
            flash("Invalid username or password", "danger")
    
    return render_template("login.html")

# Registration Route
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        email = request.form["email"]
        mobile = request.form["mobile"]
        username = request.form["username"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]
        gender = request.form["gender"]
        dob = request.form["dob"]
        address = request.form["address"]
        security_question = request.form["security_question"]
        security_answer = request.form["security_answer"]

        if password != confirm_password:
            flash("Passwords do not match!", "danger")
            return redirect(url_for("register"))

        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")

        profile_picture = None
        if "profile_picture" in request.files:
            file = request.files["profile_picture"]
            if file.filename:
                profile_picture = os.path.join("static/uploads", file.filename)
                file.save(profile_picture)

        existing_user = User.query.filter((User.email == email) | (User.username == username)).first()
        if existing_user:
            flash("Email or Username already exists!", "danger")
            return redirect(url_for("register"))

        new_user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            mobile=mobile,
            username=username,
            password=hashed_password,
            gender=gender,
            dob=dob,
            address=address,
            profile_picture=profile_picture,
            security_question=security_question,
            security_answer=security_answer,
        )

        db.session.add(new_user)
        db.session.commit()
        flash("Registration successful! You can now log in.", "success")
        return redirect(url_for("login"))

    return render_template("registration.html")

# Home Page (After Login)
@app.route("/home")
def home():
    if "user_id" not in session:
        return redirect(url_for("login"))  # Redirect if not logged in

    user = User.query.get(session["user_id"])
    return render_template("home.html", user=user)

# Logout Route
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/profile", methods=["GET", "POST"])
def profile():
    if "user_id" not in session:
        return redirect(url_for("login"))  # Redirect if not logged in

    user = User.query.get(session["user_id"])

    if request.method == "POST":
        # Update user details
        user.first_name = request.form["first_name"]
        user.last_name = request.form["last_name"]
        user.email = request.form["email"]
        user.mobile = request.form["mobile"]
        user.gender = request.form["gender"]
        user.dob = request.form["dob"]
        user.address = request.form["address"]

        # Handle profile picture upload
        if "profile_picture" in request.files:
            file = request.files["profile_picture"]
            if file.filename:
                profile_picture_path = os.path.join("static/uploads", file.filename)
                file.save(profile_picture_path)
                user.profile_picture = profile_picture_path  # Save to DB

        db.session.commit()
        flash("Profile updated successfully!", "success")
        return render_template("profile.html", user=user)  # Reload profile page with updated data

    return render_template("profile.html", user=user)


@app.route("/user_books", methods=["GET", "POST"])
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


# Display Registered Users
@app.route("/controler")
def controler():
    if "user_id" not in session:
        return redirect(url_for("login"))  # Restrict access

    users = User.query.all()
    books = Book.query.all()
    return render_template("controler.html", users=users, books=books)

@app.route("/add_book", methods=["POST"])
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

@app.route("/delete_book/<int:book_id>")
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

@app.route("/sadhana", methods=["GET", "POST"])
def sadhana():
   
    return render_template("sadhana.html",date=date)

@app.route("/filling_card", methods=["GET", "POST"])
def filling_card():
    if "user_id" not in session:
        return redirect(url_for("login"))  # Ensure user is logged in

    user_id = session["user_id"]
    
    # Get the selected date from the URL, default to today
    selected_date = request.args.get("date", date.today().strftime("%Y-%m-%d"))
    selected_date = datetime.strptime(selected_date, "%Y-%m-%d").date()

    # Fetch the Sadhana record for the selected date
    sadhana_entry = Sadhana.query.filter_by(user_id=user_id, date=selected_date).first()

    if request.method == "POST":
        if not sadhana_entry:
            sadhana_entry = Sadhana(user_id=user_id, date=selected_date)
            db.session.add(sadhana_entry)

        # Safely convert form values to integers (handles empty strings)
        def safe_int(value, default=0):
            try:
                return int(value) if value.strip() else default
            except ValueError:
                return default

        sadhana_entry.nidra_to_bed = safe_int(request.form.get("nidra_to_bed", "0"))
        sadhana_entry.nidra_wakeup = safe_int(request.form.get("nidra_wakeup", "0"))
        sadhana_entry.nidra_day_sleep = safe_int(request.form.get("nidra_day_sleep", "0"))
        sadhana_entry.japa = safe_int(request.form.get("japa", "0"))
        sadhana_entry.pathan_books = safe_int(request.form.get("pathan_books", "0"))
        sadhana_entry.hearing = safe_int(request.form.get("hearing", "0"))
        sadhana_entry.counselor_class = safe_int(request.form.get("counselor_class", "0"))
        sadhana_entry.mangal_arati = safe_int(request.form.get("mangal_arati", "0"))
        sadhana_entry.morning_class = safe_int(request.form.get("morning_class", "0"))
        sadhana_entry.study_target = safe_int(request.form.get("study_target", "0"))
        sadhana_entry.college_class = safe_int(request.form.get("college_class", "0"))
        sadhana_entry.cleanliness = safe_int(request.form.get("cleanliness", "0"))
        sadhana_entry.sadhana_card_filled = safe_int(request.form.get("sadhana_card_filled", "0"))
        sadhana_entry.cleaning_alloted_area = safe_int(request.form.get("cleaning_alloted_area", "0"))

        db.session.commit()
        flash("Sadhana record updated successfully!", "success")

        return redirect(url_for("filling_card", date=selected_date.strftime("%Y-%m-%d")))

    return render_template("filling_card.html", sadhana_entry=sadhana_entry, selected_date=selected_date,date=date)

@app.route("/set_weekly_target", methods=["GET", "POST"])
def set_weekly_target():
    if "user_id" not in session:
        return redirect(url_for("login"))

    user_id = session["user_id"]

    # Get selected date from user input or default to today
    selected_date = request.args.get("date", date.today().strftime("%Y-%m-%d"))
    selected_date = datetime.strptime(selected_date, "%Y-%m-%d").date()

    # Find the Monday of the selected week
    start_date = selected_date - timedelta(days=selected_date.weekday())  
    end_date = start_date + timedelta(days=6)  # End of the week (Sunday)
    
    # Fetch existing target settings for the selected week
    target_entry = TargetSetting.query.filter_by(user_id=user_id, start_date=start_date, end_date=end_date).first()

    if request.method == "POST":
        if not target_entry:
            target_entry = TargetSetting(user_id=user_id, start_date=start_date, end_date=end_date)
            db.session.add(target_entry)

        target_entry.book_reading_hours = float(request.form.get("book_reading_hours", 0))
        target_entry.personal_hearing_hours = float(request.form.get("personal_hearing_hours", 0))
        target_entry.study_hours = float(request.form.get("study_hours", 0))
        target_entry.college_classes = int(request.form.get("college_classes", 0)) 

        db.session.commit()
        flash("Weekly target set successfully!", "success")

        return redirect(url_for("set_weekly_target", week_start=start_date.strftime("%Y-%m-%d")))

    return render_template("set_weekly_target.html", target_entry=target_entry, start_date=start_date, end_date=end_date)

@app.route("/score_stat")
def score_stat():
    if "user_id" not in session:
        return redirect(url_for("login"))

    user_id = session["user_id"]

    # Get selected week (default to current week)
    selected_date = request.args.get("date", date.today().strftime("%Y-%m-%d"))
    selected_date = datetime.strptime(selected_date, "%Y-%m-%d").date()
    start_date = selected_date - timedelta(days=selected_date.weekday())  # Get Monday of the week
    end_date = start_date + timedelta(days=6)  # Get Sunday of the week

    # Fetch Sadhana records for the selected week
    sadhana_entries = Sadhana.query.filter(Sadhana.user_id == user_id, Sadhana.date.between(start_date, end_date)).all()
    
    # Fetch target values for the selected week
    target_entry = TargetSetting.query.filter_by(user_id=user_id, start_date=start_date, end_date=end_date).first()

    # Initialize total actual values
    actual_values = {
        "nidra_to_bed": 0,
        "nidra_wakeup": 0,
        "nidra_day_sleep": 0,
        "japa": 0,
        "pathan_books": 0,
        "hearing": 0,
        "counselor_class": 0,
        "mangal_arati": 0,
        "morning_class": 0,
        "study_target": 0,
        "college_class": 0,
        "cleanliness": 0,
        "sadhana_card_filled": 0,
        "cleaning_alloted_area": 0
    }

    # Sum up actual values from Sadhana records
    for sadhana in sadhana_entries:
        actual_values["nidra_to_bed"] += sadhana.nidra_to_bed
        actual_values["nidra_wakeup"] += sadhana.nidra_wakeup
        actual_values["nidra_day_sleep"] += sadhana.nidra_day_sleep
        actual_values["japa"] += sadhana.japa
        actual_values["pathan_books"] += sadhana.pathan_books
        actual_values["hearing"] += sadhana.hearing
        actual_values["counselor_class"] += sadhana.counselor_class
        actual_values["mangal_arati"] += sadhana.mangal_arati
        actual_values["morning_class"] += sadhana.morning_class
        actual_values["study_target"] += sadhana.study_target
        actual_values["college_class"] += sadhana.college_class
        actual_values["cleanliness"] += sadhana.cleanliness
        actual_values["sadhana_card_filled"] += sadhana.sadhana_card_filled
        actual_values["cleaning_alloted_area"] += sadhana.cleaning_alloted_area

    # Define maximum possible weekly values (assuming 7 days)
    max_values = {
        "nidra_to_bed": 25 * 7,  # Max is 25 per day
        "nidra_wakeup": 25 * 7,
        "nidra_day_sleep": 25 * 7,
        "japa": 25 * 7,
        "pathan_books": target_entry.book_reading_hours if target_entry else 7 * 7,  # Use targeted value or default 49
        "hearing": target_entry.personal_hearing_hours if target_entry else 7 * 7,  # Use targeted value or default 49
        "counselor_class": 10,
        "mangal_arati": 5 * 7,  # Max is 5 per day
        "morning_class": 5 * 7,
        "study_target": target_entry.study_hours if target_entry else 24 * 7,  # Use targeted value or default 168
        "college_class": target_entry.college_classes if target_entry else 7 * 7,  # Use targeted value or default 49
        "cleanliness": 5 * 7,
        "sadhana_card_filled": 5 * 7,
        "cleaning_alloted_area": 5 * 7
    }

    # Calculate percentage progress
    percentages = {}
    for key in actual_values:
        percentages[key] = round((actual_values[key] / max_values[key]) * 100, 2) if max_values[key] > 0 else 0
        percentages[key] =min(100,percentages[key])
    return render_template("score_stat.html", percentages=percentages, start_date=start_date, end_date=end_date)

@app.route("/history", methods=["GET", "POST"])
def history():
    if "user_id" not in session:
        return redirect(url_for("login"))

    user_id = session["user_id"]

    # Get the selected date range
    start_date = request.args.get("start_date", (date.today() - timedelta(days=30)).strftime("%Y-%m-%d"))
    end_date = request.args.get("end_date", date.today().strftime("%Y-%m-%d"))

    # Convert string to date objects
    start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
    end_date = datetime.strptime(end_date, "%Y-%m-%d").date()

    # Fetch Sadhana records for the given date range
    sadhana_entries = Sadhana.query.filter(Sadhana.user_id == user_id, Sadhana.date.between(start_date, end_date)).order_by(Sadhana.date.desc()).all()

    return render_template("history.html", sadhana_entries=sadhana_entries, start_date=start_date, end_date=end_date)



if __name__ == "__main__":
    app.run(debug=True)
