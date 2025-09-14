from flask import Flask
from models import db
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# initialize database
db.init_app(app)

# simple test route
@app.route('/')
def index():
    return '<h1>Welcome to backend</h1>'

# register routes (will import later)
# from routes.user_routes import user_bp
# from routes.project_routes import project_bp
# app.register_blueprint(user_bp, url_prefix="/api")
# app.register_blueprint(project_bp, url_prefix="/api")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # quick setup for now
    app.run(debug=True)
