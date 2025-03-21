from flask import Blueprint, render_template
from flask_login import login_required

control_routes = Blueprint('control_routes', __name__)

@control_routes.route('/controler')
@login_required
def controler():
    return render_template('controler.html')
