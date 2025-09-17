from flask import Flask
from config import Config
from models import db,User
from flask_migrate import Migrate
from routes.auth import jwt

from flask_jwt_extended import JWTManager



from routes import user_bp, project_bp, auth_bp

from flask_cors import CORS

app = Flask(__name__, instance_relative_config=True)
app.config.from_object(Config)

app.config["JWT_SECRET_KEY"] = "super-secret"

CORS(app, origins = ["http://localhost:5174"])
# initialize database
db.init_app(app)
migrate = Migrate(app, db)
jwt.init_app(app)

app.register_blueprint(user_bp)
app.register_blueprint(project_bp)
app.register_blueprint(auth_bp)

# import models so Alembic detects them
with app.app_context():
    from models import user, projects, user_project

# simple test route
@app.route('/')
def index():
    return '<h1>Welcome to backend</h1>'



if __name__ == "__main__":
    app.run(debug=True, port=5555)

