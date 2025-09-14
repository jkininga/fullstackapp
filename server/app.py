from flask import Flask
from config import Config
from models import db
from flask_migrate import Migrate

app = Flask(__name__, instance_relative_config=True)
app.config.from_object(Config)

# initialize database
db.init_app(app)
migrate = Migrate(app, db)

# import models so Alembic detects them
with app.app_context():
    from models import user, projects, user_project

# simple test route
@app.route('/')
def index():
    return '<h1>Welcome to backend</h1>'

# register routes later
# from routes.user_routes import user_bp
# from routes.project_routes import project_bp
# app.register_blueprint(user_bp, url_prefix="/api")
# app.register_blueprint(project_bp, url_prefix="/api")

if __name__ == "__main__":
    app.run(debug=True, port=5555)

