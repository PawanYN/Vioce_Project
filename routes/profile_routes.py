from flask import render_template, request, redirect, url_for, flash, session
from . import profile_bp
from app import db
from models import User
import os

@profile_bp.route("/profile", methods=["GET", "POST"])
def profile():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))  

    user = User.query.get(session["user_id"])

    if request.method == "POST":
        user.first_name = request.form["first_name"]
        user.last_name = request.form["last_name"]
        user.email = request.form["email"]
        user.mobile = request.form["mobile"]
        user.gender = request.form["gender"]
        user.dob = request.form["dob"]
        user.address = request.form["address"]

        if "profile_picture" in request.files:
            file = request.files["profile_picture"]
            if file.filename:
                profile_picture_path = os.path.join("static/uploads", file.filename)
                file.save(profile_picture_path)
                user.profile_picture = profile_picture_path

        db.session.commit()
        flash("Profile updated successfully!", "success")
        return redirect(url_for("profile.profile"))

    return render_template("profile.html", user=user)
