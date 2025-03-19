from flask import render_template, session, redirect, url_for
from . import sadhana_bp
from app import db
from models import Sadhana, User

@sadhana_bp.route("/sadhana_home")
def sadhana_home():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))  

    user = User.query.get(session["user_id"])
    return render_template("sadhana_home.html", user=user)
