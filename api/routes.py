from flask import request
from flask_restx import Api, Resource

from .rest_schema import *
from .task_dao import TaskCRUD
from .utils import to_date


tasks_api = Api(version="1.0", title="Task Manager API")

new_task_model = tasks_api.model("NewTaskModel", NEW_TASK_SCHEMA)
edit_task_model = tasks_api.model("EditTaskModel", EDIT_TASK_SCHEMA)

task_controller = TaskCRUD()


@tasks_api.route("/tasks")
class TasksList(Resource):
    def get(self):
        filter_by_status = request.args.get("status")
        tasks = task_controller.read(filter_by=filter_by_status)
        response = [task.get_dict() for task in tasks]
        return response, 200

    @tasks_api.expect(new_task_model, validate=True)
    def post(self):
        request_data = request.get_json()
        task = task_controller.create(
            title=request_data.get("title"),
            description=request_data.get("description"),
            completed=False,
            deadline=to_date(request_data.get("deadline")),
        )
        return {"id": task.id}, 201


@tasks_api.route("/tasks/<int:id>")
class Tasks(Resource):
    def get(self, id):
        task = task_controller.read(id)
        if not task:
            return {}, 404
        return task.get_dict(), 200

    @tasks_api.expect(edit_task_model, validate=True)
    def put(self, id):
        request_data = request.get_json()
        task = task_controller.update(
            id=id,
            title=request_data.get("title"),
            description=request_data.get("description"),
            completed=request_data.get("completed"),
            deadline=to_date(request_data.get("deadline")),
        )

        if not task:
            return "", 404

        return task.get_dict(), 201

    def delete(self, id):
        result = task_controller.delete(id)
        if not result:
            return "", 404
        return "", 204