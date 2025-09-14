from flask import Blueprint
from flask_restful import Api, Resource

project_bp = Blueprint("project_bp", __name__)
api = Api(project_bp)

class ProjectResource(Resource):
    def get(self, project_id=None):
        if project_id:
            return {"message": f"Get project {project_id}"}
        return {"message": "Get all projects"}

    def post(self):
        return {"message": "Create a new project"}

    def put(self, project_id):
        return {"message": f"Update project {project_id}"}

    def delete(self, project_id):
        return {"message": f"Delete project {project_id}"}

api.add_resource(ProjectResource, "/projects", "/projects/<int:project_id>")
