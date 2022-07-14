This is a program to showcase the use of restful api.

Python files:
settings.py    ---   Global settings
task.py        ---   DB manipulation
api.py         ---   Restful exposure
api_testing.py ---   Unittest
task           ---   shell script

I am using Python 3.10.5 in this project.

Before running this project, There are several prerequisites.

1. install some python modules by
pip install flask
pip install flask_sqlalchemy

2. Create db
Go to the working directory and run

>>> python
>>> from task import db
>>> db.create_all()

Then a file name "database" For Sqlite is generated.
Also a table is created with fields id(auto incr), task and date

3. Make an alias in shell script "task"
In shell file "task", make an ailas pointing to "jq" lib for json parsing as below
jq="./jq"

After that, run the api.py to launch restful service.

How to test the restful service？ Here are the examples.
1. By curl
curl -s -X GET http://127.0.0.1:1234/tasks      (list all tasks)
curl -s -X GET http://127.0.0.1:1234/tasks?date=07/13/2022     (list task with specific date)
curl -s -X GET http://127.0.0.1:1234/tasks/1                    (list a specific task)
curl -s -X POST http://127.0.0.1:1234/tasks -H 'Content-Type: application/json'  -d '{"task": "my job", "date": "07/13/2022"}'        (Add a task)
curl -s -X PUT  http://127.0.0.1:1234/tasks/1 -H 'Content-Type: application/json'  -d '{"task": "my job1", "date": "07/14/2022"}'     (update a task)
curl -s -X DELETE http://127.0.0.1:1234/tasks/1           (delete a task)

2. By running shell script
alias task="./task"

task list   --  List out all the tasks
task list <taskid>    --  List out the task with the specific taskid
task list --expiring-today    --  List out the tasks expired today
tasks add <taskname> <date>    --  Add a new task name and its due date
task update <taskid>  <taskname> <date>    --  Update the specific task with taskname and due date
task delete <taskid>     --  Delete the specific task


The program is logged to "file.log" in working directory