from flask import Blueprint, render_template
from flask_login import login_required

security_bp = Blueprint("security", __name__)


@security_bp.get("/security")
@login_required
def security():
    return render_template("security.html", active_page="security")

