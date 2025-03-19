from flask import render_template, request, redirect, url_for, flash, session
from . import auth_bp
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from models import User

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            session["user_id"] = user.id
            session["username"] = user.username
            session["profile_picture"] = user.profile_picture
            return redirect(url_for("home"))
        else:
            flash("Invalid username or password", "danger")

    return render_template("login.html")


@auth_bp.route("/register", methods=["GET", "POST"])
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
            return redirect(url_for("auth.register"))

        hashed_password = generate_password_hash(password, method="sha256")

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
            security_question=security_question,
            security_answer=security_answer,
        )

        db.session.add(new_user)
        db.session.commit()
        flash("Registration successful! You can now log in.", "success")
        return redirect(url_for("auth.login"))

    return render_template("registration.html")


@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("landing"))
