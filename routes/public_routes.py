from flask import Blueprint, render_template

public_routes = Blueprint('public_routes', __name__)

@public_routes.route('/about_us')
def about_us():
    return render_template('inspiration.html')
