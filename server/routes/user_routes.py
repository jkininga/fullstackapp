from flask import Blueprint, request
from flask_restful import Api, Resource
from models.user import User
from models import db

user_bp = Blueprint("user_bp", __name__)
api = Api(user_bp)

class UserResource(Resource):
    def get(self, user_id=None):
        """Get all users or a single user"""
        if user_id:
            user = User.query.get(user_id)
            if not user:
                return {"error": "User not found"}, 404
            return user.to_dict(), 200
        users = User.query.all()
        return [u.to_dict() for u in users], 200

    def post(self):
        """Create a new user"""
        data = request.get_json()
        if not data or not data.get("username") or not data.get("email"):
            return {"error": "Username and email required"}, 400

        new_user = User(
            username=data["username"],
            email=data["email"]
        )
        db.session.add(new_user)
        db.session.commit()
        return new_user.to_dict(), 201

    def put(self, user_id):
        """Update an existing user"""
        user = User.query.get(user_id)
        if not user:
            return {"error": "User not found"}, 404

        data = request.get_json()
        user.username = data.get("username", user.username)
        user.email = data.get("email", user.email)

        db.session.commit()
        return user.to_dict(), 200

    def delete(self, user_id):
        """Delete a user"""
        user = User.query.get(user_id)
        if not user:
            return {"error": "User not found"}, 404

        db.session.delete(user)
        db.session.commit()
        return {"message": "User deleted"}, 204

api.add_resource(UserResource, "/users", "/users/<int:user_id>")

