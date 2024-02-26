from flask import request, jsonify, make_response
from flask_restx import Api, Resource, fields, reqparse
import random

from .rest_schema import *
from .task_dao import TaskCRUD
from .utils import to_date
from .models import User

from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import set_access_cookies
from flask_jwt_extended import unset_jwt_cookies


tasks_api = Api(version="1.0", title="Task Manager API")

new_task_model = tasks_api.model("NewTaskModel", NEW_TASK_SCHEMA)
edit_task_model = tasks_api.model("EditTaskModel", EDIT_TASK_SCHEMA)

task_controller = TaskCRUD()


@tasks_api.route("/tasks")
class TasksList(Resource):
    #@jwt_required()
    def get(self):
        filter_by_status = request.args.get("status")
        #task_controller._set_user(User.get_by_username(get_jwt_identity()).id)
        tasks = task_controller.read(filter_by=filter_by_status)
        response = [task.get_dict() for task in tasks]
        return response, 200

    #@jwt_required(optional=True)
    @tasks_api.expect(new_task_model, validate=True)
    def post(self):
        request_data = request.get_json()
        #task_controller._set_user(User.get_by_username(get_jwt_identity()).id)
        task = task_controller.create(
            title=request_data.get("title"),
            description=request_data.get("description"),
            completed=False,
            deadline=to_date(request_data.get("deadline")),
        )
        return {"id": task.id}, 201


@tasks_api.route("/tasks/<int:id>")
class Tasks(Resource):
    #@jwt_required()
    def get(self, id):
        #task_controller._set_user(User.get_by_username(get_jwt_identity()).id)
        task = task_controller.read(id)
        if not task:
            return {}, 404
        return task.get_dict(), 200

    #@jwt_required()
    @tasks_api.expect(edit_task_model, validate=True)
    def put(self, id):
        request_data = request.get_json()
        #task_controller._set_user(User.get_by_username(get_jwt_identity()).id)
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

    #@jwt_required()
    def delete(self, id):
        #task_controller._set_user(User.get_by_username(get_jwt_identity()).id)
        result = task_controller.delete(id)
        if not result:
            return "", 404
        return "", 204


@tasks_api.route("/login")
class Login(Resource):
    def post(self):
        request_data = request.get_json()
        username = request_data.get("username")
        password = request_data.get("password")

        user_exists = User.get_by_username(username)

        if not user_exists:
            return {"success": False, "msg": "Wrong credentials"}, 400

        if not user_exists.check_password(password):
            return {"success": False, "msg": "Wrong credentials"}, 400

        response = {"success": True}
        access_token = create_access_token(identity=username)
        temp_response = jsonify(response)
        set_access_cookies(temp_response, access_token)
        temp_response.headers.pop("Content-Type")
        temp_response.headers.pop("Content-Length")
        return response, 200, temp_response.headers


@tasks_api.route("/logout")
class Logout(Resource):
    def post(self):
        response = {"success": True}
        return response, 200, {"Set-Cookie": "{0}=".format("access_token_cookie")}
