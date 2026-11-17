from flask import Blueprint, jsonify, render_template
from flask_login import login_required

main_bp = Blueprint("main", __name__)


@main_bp.get("/")
def index():
    return render_template("landing.html")


@main_bp.get("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html", active_page="overview")


@main_bp.get("/health")
def health():
    return jsonify({"status": "ok", "service": "autocloud-ai"})

