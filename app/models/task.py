from app.extensions import db


class Task(db.Model):
    __tablename__ = "tasks"

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(255), nullable=False)

    description = db.Column(db.Text, nullable=True)

    status = db.Column(db.String(50), nullable=False, default="todo")

    created_by = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    assigned_to = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)

    creator = db.relationship(
        "User", foreign_keys=[created_by], backref="created_tasks"
    )

    assignee = db.relationship(
        "User", foreign_keys=[assigned_to], backref="assigned_tasks"
    )

    def __repr__(self):
        return f"<Task {self.title}>"
