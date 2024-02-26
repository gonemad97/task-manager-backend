from .models import Task, db


class TaskCRUD:
    def __init__(self):
        self.user = None

    def _set_user(self, user):
        self.user = user

    def create(self, title, description=None, completed=False, deadline=None):
        task = Task(
            title=title,
            description=description,
            completed=completed,
            deadline=deadline,
            user_id=self.user,
        )
        task.save()
        return task

    def read(self, id=None, filter_by=None):
        if id:
            # user_tasks = Task.query.filter_by(user_id=self.user)
            # return user_tasks.filter_by(id=id).first()
            return Task.query.filter_by(id=id).first()
        # tasks = Task.query.filter_by(user_id=self.user)
        tasks = Task.query.all()
        if filter_by:
            completed_tasks = None
            if filter_by == "complete":
                completed_tasks = True
            if filter_by == "incomplete":
                completed_tasks = False
            if completed_tasks is not None:
                tasks = Task.query.filter_by(completed=completed_tasks).order_by(Task.id.desc())
        return tasks

    def update(self, id, title=None, description=None, completed=None, deadline=None):
        # user_tasks = Task.query.filter_by(user_id=self.user)
        # task = user_tasks.filter_by(id=id).first()
        task = Task.query.filter_by(id=id).first()
        if not task:
            return False

        if title:
            task.title = title
        if description:
            task.description = description
        if completed is not None:
            task.completed = completed
        if deadline:
            task.deadline = deadline

        db.session.commit()
        return Task.query.get(id)

    def delete(self, id):
        #user_tasks = Task.query.filter_by(user_id=self.user)
        #result = user_tasks.filter_by(id=id).delete()
        result = Task.query.filter_by(id=id).delete()
        db.session.commit()
        return bool(result)
