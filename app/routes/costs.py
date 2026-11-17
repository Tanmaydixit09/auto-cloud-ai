from flask import Blueprint, render_template
from flask_login import login_required

costs_bp = Blueprint("costs", __name__)


@costs_bp.get("/costs")
@login_required
def costs():
    return render_template("costs.html", active_page="costs")

