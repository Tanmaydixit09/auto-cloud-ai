from flask import Blueprint, render_template
from flask_login import login_required

cicd_bp = Blueprint("cicd", __name__)


@cicd_bp.get("/cicd")
@login_required
def cicd():
    return render_template("cicd.html", active_page="cicd")

