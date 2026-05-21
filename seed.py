from app import create_app, db
from app.models.role import Role

app = create_app()

with app.app_context():
    roles = ["admin", "manager", "user"]

    for role_name in roles:
        existing_role = Role.query.filter_by(name=role_name).first()

        if not existing_role:
            role = Role(name=role_name)
            db.session.add(role)

    db.session.commit()

    print("Roles seeded successfully!")
