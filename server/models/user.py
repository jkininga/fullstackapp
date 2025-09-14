from . import db
from .user_project import user_project

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    projects = db.relationship(
        "Project",
        secondary=user_project,
        back_populates="users"
    )
