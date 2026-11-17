from flask import Blueprint, render_template
from flask_login import login_required

monitoring_bp = Blueprint("monitoring", __name__)


@monitoring_bp.get("/monitoring")
@login_required
def monitoring():
    return render_template("monitoring.html", active_page="monitoring")

