from flask import Flask
from app.config import Config
from app.extensions import db, migrate, jwt, bcrypt
from app.models import Role, User
from app.routes.auth import auth_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.register_blueprint(auth_bp, url_prefix="/api/auth")

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    bcrypt.init_app(app)

    @app.route("/")
    def home():
        return {"message": "Cloud-Native Task Management API is running"}

    return app
