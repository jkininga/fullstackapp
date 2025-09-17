from flask import Blueprint, request
from flask_restful import Api, Resource
from models.projects import Project
from models import db
from flask_jwt_extended import jwt_required, get_jwt_identity

project_bp = Blueprint("project_bp", __name__)
api = Api(project_bp)

class ProjectResource(Resource):
    @jwt_required()
    def get(self, project_id=None):
        """Get all projects or a single project"""
        if project_id:
            project = Project.query.get(project_id)
            if not project:
                return {"error": "Project not found"}, 404
            return project.to_dict(), 200
        projects = Project.query.all()
        return [p.to_dict() for p in projects], 200
    
    @jwt_required()
    def post(self):
        """Create a new project"""
        data = request.get_json()
        if not data or not data.get("name"):
            return {"error": "Project name is required"}, 400

        new_project = Project(name=data["name"])
        db.session.add(new_project)
        db.session.commit()
        return new_project.to_dict(), 201
    
    @jwt_required()
    def put(self, project_id):
        """Update an existing project"""
        project = Project.query.get(project_id)
        if not project:
            return {"error": "Project not found"}, 404

        data = request.get_json()
        project.name = data.get("name", project.name)

        db.session.commit()
        return project.to_dict(), 200

    @jwt_required()
    def delete(self, project_id):
        """Delete a project"""
        project = Project.query.get(project_id)
        if not project:
            return {"error": "Project not found"}, 404

        db.session.delete(project)
        db.session.commit()
        return {"message": "Project deleted"}, 204

api.add_resource(ProjectResource, "/projects", "/projects/<int:project_id>")
