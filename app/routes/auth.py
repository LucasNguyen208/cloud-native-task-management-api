from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

from app.extensions import db, bcrypt
from app.models.user import User
from app.models.role import Role
from app.middleware.rbac import role_required

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["POST"])
def register():

    data = request.get_json()

    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    existing_user = User.query.filter_by(email=email).first()

    if existing_user:
        return jsonify({"message": "Email already exists"}), 400

    default_role = Role.query.filter_by(name="user").first()

    hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")

    new_user = User(
        username=username,
        email=email,
        password_hash=hashed_password,
        role_id=default_role.id,
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201


@auth_bp.route("/login", methods=["POST"])
def login():

    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({"message": "Invalid email or password"}), 401

    is_password_correct = bcrypt.check_password_hash(user.password_hash, password)

    if not is_password_correct:
        return jsonify({"message": "Invalid email or password"}), 401

    access_token = create_access_token(identity=str(user.id))

    return jsonify({"access_token": access_token}), 200


@auth_bp.route("/profile", methods=["GET"])
@jwt_required()
def profile():

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

    return jsonify({"message": "Welcome Admin"}), 200
