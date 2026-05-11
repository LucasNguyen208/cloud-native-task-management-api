from flask import Flask
from app.config import Config
from app.extensions import db, migrate, jwt
from app.models import Role, User

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    @app.route("/")
    def home():
        return {
            "message": "Cloud-Native Task Management API is running"
        }
    
    return app