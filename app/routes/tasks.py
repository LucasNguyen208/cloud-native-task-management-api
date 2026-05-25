from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.extensions import db
from app.models.task import Task
from app.models.user import User
from app.validators.task_validators import (
    validate_request_body,
    validate_title,
    validate_description,
    validate_task_status,
)
from app.errors.exceptions import APIError
from app.utils.db_helpers import safe_commit

tasks_bp = Blueprint("tasks", __name__)


@tasks_bp.route("", methods=["POST"])
@jwt_required()
def create_task():
    """
    Create a new task
    ---
    tags:
      - Tasks

    security:
      - BearerAuth: []

    parameters:
      - in: body
        name: body
        required: true

        schema:
          type: object

          required:
            - title

          properties:
            title:
              type: string
              example: Implement Swagger

            description:
              type: string
              example: Add API documentation using Flasgger

            assigned_to:
              type: integer
              example: 1

    responses:
      201:
        description: Task created

      400:
        description: Validation failed

      404:
        description: Assigned user not found
    """
    data = request.get_json()

    # =========================
    # Request Validation
    # =========================

    if not validate_request_body(data):
        raise APIError("Request body is required", 400)

    title = data.get("title")
    description = data.get("description")
    assigned_to = data.get("assigned_to")

    # =========================
    # Required Fields Validation
    # =========================

    if not title:
        raise APIError("Title is required", 400)

    # =========================
    # Length Validation
    # =========================

    if not validate_title(title):
        raise APIError("Title must be between 3 and 255 characters", 400)

    if not validate_description(description):
        raise APIError("Description cannot exceed 1000 characters", 400)

    # =========================
    # Foreign Key Validation
    # =========================

    if assigned_to is not None:
        assigned_user = User.query.get(assigned_to)

        if not assigned_user:
            raise APIError("Assigned user not found", 404)

    current_user_id = get_jwt_identity()

    new_task = Task(
        title=title,
        description=description,
        created_by=current_user_id,
        assigned_to=assigned_to,
    )

    db.session.add(new_task)
    safe_commit()

    return jsonify({"message": "Task created successfully"}), 201


@tasks_bp.route("", methods=["GET"])
@jwt_required()
def get_tasks():
    """
    Get all tasks
    ---
    tags:
      - Tasks

    security:
      - BearerAuth: []

    responses:
      200:
          description: List of tasks retrieved successfully
    """
    tasks = Task.query.all()

    result = []

    for task in tasks:
        result.append(
            {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "status": task.status,
                "created_by": task.created_by,
                "assigned_to": task.assigned_to,
            }
        )

    return jsonify(result), 200


@tasks_bp.route("/<int:task_id>", methods=["GET"])
@jwt_required()
def get_task(task_id):
    """
    Get a single task by ID
    ---
    tags:
      - Tasks

    security:
      - BearerAuth: []

    parameters:
      - in: path
        name: task_id
        type: integer
        required: true

    responses:
      200:
        description: Task retrieved successfully

      404:
        description: Task not found
    """
    task = Task.query.get(task_id)

    if not task:
        raise APIError("Task not found", 404)

    result = {
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "status": task.status,
        "created_by": task.created_by,
        "assigned_to": task.assigned_to,
    }

    return jsonify(result), 200


@tasks_bp.route("/<int:task_id>", methods=["PUT"])
@jwt_required()
def update_task(task_id):
    """
    Update a task
    ---
    tags:
      - Tasks

    security:
      - BearerAuth: []

    parameters:
      - in: path
        name: task_id
        type: integer
        required: true

      - in: body
        name: body

        schema:
          type: object

          properties:
            title:
              type: string

            description:
              type: string

            status:
              type: string
              example: in_progress

            assigned_to:
              type: integer

    responses:
      200:
        description: Task updated successfully

      400:
        description: Validation failed

      403:
        description: Access forbidden

      404:
        description: Task not found
    """
    task = Task.query.get(task_id)
    if not task:
        raise APIError("Task not found", 404)

    current_user_id = int(get_jwt_identity())

    user = User.query.get(current_user_id)

    is_admin = user.role.name == "admin"
    is_creator = task.created_by == current_user_id

    if not is_admin and not is_creator:
        raise APIError("Access forbidden", 403)

    data = request.get_json()

    # =========================
    # Request Validation
    # =========================

    if not validate_request_body(data):
        raise APIError("Request body is required", 400)

    # =========================
    # Length Validation
    # =========================

    new_title = data.get("title")
    if new_title is not None:
        if not validate_title(new_title):
            raise APIError("Title must be between 3 and 255 characters", 400)

    new_description = data.get("description")
    if not validate_description(new_description):
        raise APIError("Description cannot exceed 1000 characters", 400)

    # =========================
    # Enum Validation
    # =========================

    new_status = data.get("status")

    if new_status is not None and not validate_task_status(new_status):
        raise APIError("Invalid task status", 400)

    # =========================
    # Foreign Key Validation
    # =========================

    assigned_to = data.get("assigned_to")

    if assigned_to is not None:
        assigned_user = User.query.get(assigned_to)

        if not assigned_user:
            raise APIError("Assigned user not found", 404)

    # =========================
    # Update Task
    # =========================

    task.title = data.get("title", task.title)
    task.description = data.get("description", task.description)
    task.status = data.get("status", task.status)
    task.assigned_to = data.get("assigned_to", task.assigned_to)

    safe_commit()

    return jsonify({"message": "Task updated successfully"}), 200


@tasks_bp.route("/<int:task_id>", methods=["DELETE"])
@jwt_required()
def delete_task(task_id):
    """
    Delete a task
    ---
    tags:
      - Tasks

    security:
      - BearerAuth: []

    parameters:
      - in: path
        name: task_id
        type: integer
        required: true

    responses:
      200:
        description: Task deleted successfully

      403:
        description: Access forbidden

      404:
        description: Task not found
    """
    task = Task.query.get(task_id)

    if not task:
        raise APIError("Task not found", 404)

    current_user_id = int(get_jwt_identity())

    user = User.query.get(current_user_id)

    is_admin = user.role.name == "admin"
    is_creator = task.created_by == current_user_id

    if not is_admin and not is_creator:
        raise APIError("Access forbidden", 403)

    db.session.delete(task)
    safe_commit()

    return jsonify({"message": "Task deleted successfully"}), 200
