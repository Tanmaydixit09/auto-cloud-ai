from flask import Blueprint, render_template
from flask_login import login_required

infrastructure_bp = Blueprint("infrastructure", __name__)


@infrastructure_bp.get("/infrastructure")
@login_required
def infrastructure():
    return render_template("infrastructure.html", active_page="infrastructure")

