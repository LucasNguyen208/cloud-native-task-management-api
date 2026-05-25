from flask import Flask
from app.config import Config
from app.extensions import db, migrate, jwt, bcrypt
from app.models import Role as Role
from app.models import User as User
from app.routes.auth import auth_bp
from app.routes.tasks import tasks_bp
from flasgger import Swagger
from app.errors.handlers import register_error_handlers


def create_app():
    app = Flask(__name__)
    register_error_handlers(app)

    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    bcrypt.init_app(app)

    swagger_config = {
        "headers": [],
        "specs": [
            {
                "endpoint": "apispec",
                "route": "/apispec.json",
                "rule_filter": lambda rule: True,
                "model_filter": lambda tag: True,
            }
        ],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/apidocs/",
    }

    swagger_template = {
        "swagger": "2.0",
        "info": {
            "title": "Cloud-Native Task Management API",
            "description": "Task Management REST API with JWT Authentication and RBAC",
            "version": "1.0.0",
        },
        "securityDefinitions": {
            "BearerAuth": {
                "type": "apiKey",
                "name": "Authorization",
                "in": "header",
                "description": "Enter: Bearer <JWT_TOKEN>",
            }
        },
    }

    Swagger(app, config=swagger_config, template=swagger_template)

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(tasks_bp, url_prefix="/api/tasks")

    @app.route("/")
    def home():
        return {"message": "Cloud-Native Task Management API is running"}

    return app
