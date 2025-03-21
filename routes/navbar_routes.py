from flask import Flask,Blueprint, render_template, redirect, url_for, request, flash,session
from flask_login import login_required, current_user,login_user
from flask_bcrypt import Bcrypt
from models.user import User 

navbar_routes = Blueprint('navbar_routes', __name__)
bcrypt = Bcrypt()  # Initialize Bcrypt

@navbar_routes.route('/')
def landing():
    return render_template("index.html")

@navbar_routes.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            session["user_id"] = user.id
            session["username"] = user.username
            flash("Sucessful")
            return redirect(url_for("navbar_routes.home"))
        else:
            flash("Invalid username or password", "danger")
    
    return render_template("login.html")

@navbar_routes.route('/register', methods=["GET", "POST"])
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

@navbar_routes.route('/home')
def home():
    if "user_id" not in session:
        return render_template("index.html") # Redirect if not logged in

    user = User.query.get(session["user_id"])
    return render_template("index.html", user=user)


@navbar_routes.route('/logout')
@login_required
def logout():
    session.clear()
    return render_template("index.html")

@navbar_routes.route('/profile')
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
