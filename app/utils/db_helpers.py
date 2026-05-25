from sqlalchemy.exc import IntegrityError

from app.extensions import db

from app.errors.exceptions import APIError


def safe_commit():

    try:
        db.session.commit()

    except IntegrityError:
        db.session.rollback()

        raise APIError(
            "Username or email already exists",
            409,
        )

    except Exception:
        db.session.rollback()

        raise APIError(
            "Database operation failed",
            500,
        )
