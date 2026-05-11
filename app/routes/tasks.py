from flask import Blueprint, request, jsonify
from flask_jwt_extended import (jwt_required, get_jwt_identity)

from app.extensions import db
from app.models.task import Task

tasks_bp = Blueprint("tasks", __name__)

@tasks_bp.route("", methods=["POST"])
@jwt_required()
def create_task():

    data = request.get_json()

    title = data.get("title")
    description = data.get("description")
    assigned_to = data.get("assigned_to")

    current_user_id = get_jwt_identity()

    new_task = Task(
        title=title,
        description=description,
        created_by=current_user_id,
        assigned_to=assigned_to
    )

    db.session.add(new_task)
    db.session.commit()

    return jsonify({
        "message": "Task created successfully"
    }), 201
