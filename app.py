from flask import Flask, render_template, request, redirect, url_for, flash,session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
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

# Create database tables
with app.app_context():
    db.create_all()

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

# Display Registered Users
@app.route("/controler")
def controler():
    users = User.query.all()
    return render_template("controler.html", users=users)

if __name__ == "__main__":
    app.run(debug=True)
