from flask_restx import fields

NEW_TASK_SCHEMA = {
    "title": fields.String(required=True, min_length=1, max_length=200),
    "description": fields.String(required=False, min_length=1, max_length=400),
    "deadline": fields.Date(required=False),
}

EDIT_TASK_SCHEMA = {
    "title": fields.String(required=False, min_length=1, max_length=200),
    "description": fields.String(required=False, min_length=1, max_length=400),
    "completed": fields.Boolean(required=False),
    "deadline": fields.Date(required=False),
}
