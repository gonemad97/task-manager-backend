from .models import Task, db


class TaskCRUD:
    def create(self, title, description=None, completed=False, deadline=None):
        task = Task(
            title=title,
            description=description,
            completed=completed,
            deadline=deadline,
        )
        task.save()
        return task

    def read(self, id=None, filter_by=None):
        if id:
            return Task.query.filter_by(id=id).first()
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
        result = Task.query.filter_by(id=id).delete()
        db.session.commit()
        return bool(result)
