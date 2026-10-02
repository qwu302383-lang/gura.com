from flask import Blueprint, render_template
from backend.config import GOOGLE_CLIENT_ID

main_bp = Blueprint("main", __name__)

@main_bp.get("/")
def home():
    return render_template("index.html", google_client_id=GOOGLE_CLIENT_ID)
