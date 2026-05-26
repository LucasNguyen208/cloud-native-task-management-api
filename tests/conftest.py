import os

os.environ["ENV_FILE"] = ".env.test"

import pytest

from app import create_app
from app.extensions import db
from app.models.role import Role


@pytest.fixture
def app():

    app = create_app()

    app.config.update(TESTING=True)

    db_uri = app.config["SQLALCHEMY_DATABASE_URI"]

    assert (
        "task_management_test" in db_uri
    ), f"Refusing to run tests against non-test database: {db_uri}"

    with app.app_context():
        roles = Role.query.all()

        if not roles:
            db.session.add(Role(id=1, name="admin"))

            db.session.add(Role(id=2, name="manager"))

            db.session.add(Role(id=3, name="user"))

            db.session.commit()

        yield app


@pytest.fixture(autouse=True)
def cleanup_db(app):

    with app.app_context():
        yield

        db.session.rollback()

        db.session.execute(db.text("DELETE FROM tasks"))

        db.session.execute(db.text("DELETE FROM users"))

        db.session.commit()


@pytest.fixture
def client(app):

    return app.test_client()
