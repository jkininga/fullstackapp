from flask import Blueprint
from flask_restful import Api, Resource

user_bp = Blueprint("user_bp", __name__)
api = Api(user_bp)

class UserResource(Resource):
    def get(self, user_id=None):
        if user_id:
            return {"message": f"Get user {user_id}"}
        return {"message": "Get all users"}

    def post(self):
        return {"message": "Create a new user"}

    def put(self, user_id):
        return {"message": f"Update user {user_id}"}

    def delete(self, user_id):
        return {"message": f"Delete user {user_id}"}

api.add_resource(UserResource, "/users", "/users/<int:user_id>")
