from flask import Blueprint
from flask import jsonify


health_bp = Blueprint(
    "health",
    __name__
)


@health_bp.route(
    "/health",
    methods=["GET"]
)
def health():

    return jsonify(
        {
            "status":
            "healthy"
        }
    ), 200
