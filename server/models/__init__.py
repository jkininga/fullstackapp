from flask_sqlalchemy import SQLAlchemy

# create the db instance
db = SQLAlchemy()

# import models so they register with SQLAlchemy
from .user import User
from .projects import Project
from .user_project import user_project


