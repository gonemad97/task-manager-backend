from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(400), nullable=True)
    completed = db.Column(db.Boolean, default=False)
    deadline = db.Column(db.Date, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def save(self):
        db.session.add(self)
        db.session.commit()

    def get_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "completed": self.completed,
            "deadline": str(self.deadline),
        }


class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    username = db.Column(db.String(32), nullable=False)
    password = db.Column(db.Text())

    def save(self):
        db.session.add(self)
        db.session.commit()

    def set_password(self, password):
        self.password = password

    def check_password(self, password):
        return self.password == password

    @classmethod
    def get_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def get_by_username(cls, username):
        return cls.query.filter_by(username=username).first()
