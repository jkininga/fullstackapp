from . import db
from .user_project import user_project
from sqlalchemy_serializer import SerializerMixin
# from werkzeug.security import generate_password_hash, check_password_hash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt()

class User(db.Model, SerializerMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), nullable=False, unique=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column("password_hash", db.String(128), nullable=False)

    projects = db.relationship(
        "Project",
        secondary=user_project,
        back_populates="users"
    )

    # prevent circular reference: user → project → user
    serialize_rules = ("-projects.users","-password_hash",)
    
     # stores hashed password in the db
    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode()
        
    # Confirms if password is correct when logging in 
    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)


