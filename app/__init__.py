# app/__init__.py - create_app factory
from flask import Flask
from .extensions import db, migrate, login_manager
from . import models


def create_app(config_class=None):
    app = Flask(__name__, static_folder="static", template_folder="templates")
    # load config
    if config_class is None:
        app.config.from_object("config.DevelopmentConfig")
    else:
        app.config.from_object(config_class)

    # initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

        # register a user_loader for Flask-Login
    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        try:
            return User.query.get(int(user_id))
        except Exception:
            return None


    # register blueprints
    from .main import bp as main_bp
    app.register_blueprint(main_bp)

    from .api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix="/api")

    # simple healthcheck route
    @app.route("/health")
    def health():
        return {"status":"ok", "app":"emmidear"}

    return app
