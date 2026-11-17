from flask import Blueprint, render_template
from flask_login import login_required

docker_bp = Blueprint("docker", __name__)


@docker_bp.get("/docker")
@login_required
def docker():
    return render_template("docker.html", active_page="docker")

