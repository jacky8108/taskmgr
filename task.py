"""
This module defines CRUD mechanism
"""
from flask_sqlalchemy import SQLAlchemy
from settings import *
import json

# Initializing database
db = SQLAlchemy(app)

class Task(db.Model):
    __tablename__ = 'task'  # creating a table name
    id = db.Column(db.Integer, primary_key=True)  # this is the primary key
    # nullable is false so the column can't be empty
    task = db.Column(db.String(80), nullable=False)
    date = db.Column(db.String(80), nullable=False)

    def json(self):
        """
        Define and convert output to json
        """
        return {'id': self.id, 'task': self.task,
                'date': self.date}


    def add_task(_task, _date):
        """
        Add task to database using _task, _date as parameters
        creating an instance of our Task constructor
        """
        new_task = Task(task=_task, date=_date)
        db.session.add(new_task)  # add new task to database session
        db.session.flush()
        db.session.commit()  # commit changes to session
        return new_task.id  # return the latest id

    def get_all_tasks():
        """
        Get all tasks in our database
        """
        return [Task.json(task) for task in Task.query.all()]

    def get_tasks(_date):
        """
        Get all tasks on a specific date
        """
        return [Task.json(task) for task in Task.query.filter_by(date=_date).all()]

    def get_task(_id):
        """
        Get task using the id of the task as parameter
        """
        tasktoreturn = Task.query.filter_by(id=_id).first()
        if tasktoreturn == None:
            return None
        else:
            return [Task.json(tasktoreturn)]

    def update_task(_id, _task, _date):
        """
        Update the details of a task using the id, task, and date as parameters
        """
        task_to_update = Task.query.filter_by(id=_id).first()
        task_to_update.task = _task
        task_to_update.date = _date
        db.session.commit()

    def delete_task(_id):
        """
        Delete a task from our database using the id of the task as a parameter"""
        Task.query.filter_by(id=_id).delete()
        # filter by id and delete
        db.session.commit()  # commiting the new change to our database
