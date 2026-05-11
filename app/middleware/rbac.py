from functools import wraps

from flask import jsonify

from flask_jwt_extended import get_jwt_identity

from app.models.user import User


def role_required(required_role):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            current_user_id = get_jwt_identity()

            user = User.query.get(current_user_id)

            if not user:
                return jsonify({"message": "User not found"}), 404

            if user.role.name != required_role:
                return jsonify({"message": "Access forbidden"}), 403

            return func(*args, **kwargs)

        return wrapper

    return decorator
