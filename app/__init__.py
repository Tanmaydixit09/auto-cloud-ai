import os
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask
from flask_login import LoginManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect

from config import Config

db = SQLAlchemy()
csrf = CSRFProtect()
login_manager = LoginManager()
limiter = Limiter(key_func=get_remote_address)


def create_app(test_config=None):
    load_dotenv()
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)
    app.config["DEBUG"] = os.getenv("FLASK_DEBUG", "false").lower() == "true"
    if test_config:
        app.config.update(test_config)

    Path(app.instance_path).mkdir(parents=True, exist_ok=True)
    db.init_app(app)
    csrf.init_app(app)
    login_manager.init_app(app)
    limiter.init_app(app)
    login_manager.login_view = "auth.login"
    login_manager.login_message_category = "info"

    from app.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    from app.routes.auth import auth_bp
    from app.routes.main import main_bp
    from app.routes.ai import ai_bp
    from app.routes.infrastructure import infrastructure_bp
    from app.routes.docker import docker_bp
    from app.routes.cicd import cicd_bp
    from app.routes.security import security_bp
    from app.routes.monitoring import monitoring_bp
    from app.routes.costs import costs_bp

    for blueprint in (
        auth_bp,
        main_bp,
        ai_bp,
        infrastructure_bp,
        docker_bp,
        cicd_bp,
        security_bp,
        monitoring_bp,
        costs_bp,
    ):
        app.register_blueprint(blueprint)

    with app.app_context():
        db.create_all()
        _create_demo_admin()
    return app


def _create_demo_admin():
    from app.models import User

    username = os.getenv("DEMO_ADMIN_USERNAME")
    email = os.getenv("DEMO_ADMIN_EMAIL")
    password = os.getenv("DEMO_ADMIN_PASSWORD")
    if not all((username, email, password)):
        return

    if User.query.count() == 0:
        user = User(username=username, email=email, is_admin=True)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

