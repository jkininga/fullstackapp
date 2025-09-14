from . import db
from .user_project import user_project

class Project(db.Model):
    __tablename__ = "projects"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)

    users = db.relationship(
        "User",
        secondary=user_project,
        back_populates="projects"
    )
