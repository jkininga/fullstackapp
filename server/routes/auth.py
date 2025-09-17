# routes/auth.py
from flask import Blueprint, request
from flask_jwt_extended import JWTManager

from flask_restful import Resource, Api
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
    get_jwt
)
from sqlalchemy.exc import IntegrityError

jwt_blocklist = set()

jwt = JWTManager()

@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]  # unique ID for a JWT
    return jti in jwt_blocklist

from models import db, User

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")
auth_api = Api(auth_bp)


class RegisterResource(Resource):
    def post(self):
        data = request.get_json(silent=True) or {}
        email = (data.get("email") or "").strip().lower()
        username = (data.get("username") or "").strip()
        password = data.get("password")

        if not email or not username or not password:
            return {"error": "email, username, and password are required"}, 400
        if len(password) < 6:
            return {"error": "password must be at least 6 characters"}, 400
        if User.query.filter_by(email=email).first():
            return {"error": "email already registered"}, 409

        user = User(email=email, username=username)
        user.set_password(password)  # assumes your User model has this method

        db.session.add(user)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return {"error": "username or email already in use"}, 409

        return user.to_dict(rules=("-projects", "-password_hash")), 201


class LoginResource(Resource):
    def post(self):
        data = request.get_json(silent=True) or {}
        email = (data.get("email") or "").strip().lower()
        password = data.get("password")

        if not email or not password:
            return {"error": "email and password are required"}, 400

        user = User.query.filter_by(email=email).first()
        if not user or not user.check_password(password):
            return {"error": "invalid credentials"}, 401

        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user": user.to_dict(rules=("-projects", "-password_hash"))
        }, 200


class MeResource(Resource):
    @jwt_required()
    def get(self):
        uid = get_jwt_identity()
        user = User.query.get_or_404(uid)
        return user.to_dict(rules=("-password_hash",)), 200


class RefreshResource(Resource):
    @jwt_required(refresh=True)
    def post(self):
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)

        if not user:
            return {"error": "User not found"}, 404

        new_access_token = create_access_token(identity=current_user_id)

        return {
            "access_token": new_access_token,
            "user": user.to_dict(rules=("-projects", "-password_hash"))
        }, 200
        
        
class LogoutResource(Resource):
    @jwt_required()
    def post(self):
        jti = get_jwt()["jti"]  # unique identifier for the token
        jwt_blocklist.add(jti)  # add it to the blocklist
        return {"msg": "Successfully logged out"}, 200


# Mount under /api/auth/...
auth_api.add_resource(RegisterResource, "/register")
auth_api.add_resource(LoginResource, "/login")
auth_api.add_resource(MeResource, "/me")
auth_api.add_resource(RefreshResource, "/refresh")
auth_api.add_resource(LogoutResource, "/logout")
