from flask import Blueprint

# Define Blueprints
auth_bp = Blueprint("auth", __name__)
book_bp = Blueprint("book", __name__)
sadhana_bp = Blueprint("sadhana", __name__)
profile_bp = Blueprint("profile", __name__)

# Import Routes
from . import auth_routes, book_routes, sadhana_routes, profile_routes
