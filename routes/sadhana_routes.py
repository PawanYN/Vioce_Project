from flask import Flask,Blueprint, render_template, redirect, url_for, request, flash,session
from flask_login import login_required
from datetime import date, timedelta , datetime
from models.sadhana import Sadhana
from models.target_setting import TargetSetting

sadhana_routes = Blueprint('sadhana_routes', __name__)

@sadhana_routes.route('/sadhana')
def sadhana():
    return render_template("sadhana.html",date=date)

@sadhana_routes.route('/filling_sadhana', methods=["GET", "POST"])
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

        return redirect(url_for("sadhana_routes.filling_card", date=selected_date.strftime("%Y-%m-%d")))

    return render_template("filling_card.html", sadhana_entry=sadhana_entry, selected_date=selected_date,date=date)

@sadhana_routes.route('/set_weekly_target', methods=["GET", "POST"])
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

@sadhana_routes.route('/score_stat')
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

@sadhana_routes.route('/history')
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

