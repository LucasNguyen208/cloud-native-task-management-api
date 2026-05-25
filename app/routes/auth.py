from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

from app.extensions import db, bcrypt
from app.models.user import User
from app.models.role import Role
from app.middleware.rbac import role_required
from app.validators.auth_validators import (
    validate_request_body,
    validate_required_fields,
    validate_email_format,
    validate_username,
    validate_password,
)
from app.errors.exceptions import APIError
from app.utils.db_helpers import safe_commit

auth_bp = Blueprint("auth", __name__)

# @auth_bp.route("/test-error", methods=["GET"])
# def test_error():
#     raise APIError("Test error", 418)


@auth_bp.route("/register", methods=["POST"])
def register():
    """
    Register a new user
    ---
    tags:
      - Authentication

    parameters:
      - in: body
        name: body
        required: true

        schema:
          type: object

          required:
            - username
            - email
            - password

          properties:
            username:
              type: string
              example: long

            email:
              type: string
              example: long@example.com

            password:
              type: string
              example: password123

    responses:
      201:
        description: User registered successfully

      400:
        description: Validation failed

      409:
        description: Username or email already exists
    """
    data = request.get_json()

    # =========================
    # Request Validation
    # =========================

    if not validate_request_body(data):
        raise APIError("Request body is required", 400)

    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    # =========================
    # Required Fields Validation
    # =========================

    if not validate_required_fields(username, email, password):
        raise APIError("Username, email and password are required", 400)

    # =========================
    # Email Format Validation
    # =========================

    if not validate_email_format(email):
        raise APIError("Invalid email format", 400)

    # =========================
    # Length Validation
    # =========================

    if not validate_username(username):
        raise APIError("Username must be between 3 and 50 characters", 400)

    if not validate_password(password):
        raise APIError("Password must be at least 8 characters long", 400)

    default_role = Role.query.filter_by(name="user").first()

    hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")

    new_user = User(
        username=username,
        email=email,
        password_hash=hashed_password,
        role_id=default_role.id,
    )

    db.session.add(new_user)
    safe_commit()

    return jsonify({"message": "User registered successfully"}), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    """
    Login user
    ---
    tags:
      - Authentication

    parameters:
      - in: body
        name: body
        required: true

        schema:
          type: object

          required:
            - email
            - password

          properties:
            email:
              type: string
              example: long@example.com

            password:
              type: string
              example: password123

    responses:
      200:
        description: Login successful

      400:
        description: Invalid request

      401:
        description: Invalid credentials
    """
    data = request.get_json()

    # =========================
    # Request Validation
    # =========================

    if not validate_request_body(data):
        raise APIError("Request body is required", 400)

    email = data.get("email")
    password = data.get("password")

    # =========================
    # Required Fields Validation
    # =========================

    if not validate_required_fields(email, password):
        raise APIError("Email and password are required", 400)

    user = User.query.filter_by(email=email).first()

    if not user:
        raise APIError("Invalid email or password", 401)

    is_password_correct = bcrypt.check_password_hash(user.password_hash, password)

    if not is_password_correct:
        raise APIError("Invalid email or password", 401)

    access_token = create_access_token(identity=str(user.id))

    return jsonify({"access_token": access_token}), 200


@auth_bp.route("/profile", methods=["GET"])
@jwt_required()
def profile():
    """
    Get current user profile
    ---
    tags:
      - Authentication

    security:
      - BearerAuth: []

    responses:
      200:
        description: User profile retrieved successfully

      401:
        description: Missing or invalid token

      404:
        description: User not found
    """
    current_user_id = get_jwt_identity()

    user = User.query.get(current_user_id)

    return (
        jsonify(
            {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "role": user.role.name,
            }
        ),
        200,
    )


@auth_bp.route("/admin", methods=["GET"])
@jwt_required()
@role_required("admin")
def admin_only():
    """
    Admin-only endpoint
    ---
    tags:
      - Authentication

    security:
      - BearerAuth: []

    responses:
      200:
        description: Admin access granted

      403:
        description: Access forbidden
    """
    return jsonify({"message": "Welcome Admin"}), 200
