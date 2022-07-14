"""

Expose Restful endpoint

"""

from task import *
import logging
from datetime import datetime

logging.basicConfig(filename = 'file.log',
                    level = logging.INFO,
                    format = '%(asctime)s:%(levelname)s:%(name)s:%(message)s')

class TaskFormatError(Exception):
    """
    Customized exception to handle format issue of input taskname and date
    """
    def __init__(self, message):
        self.message = message

def validateinput(task_json):
    """
    Validate taskname and date
    Raise exception when then length of task name exceeds 80 characters or 
    the date format is not correct. Accepted date format is like dd/mm/yyyy 
    """

    if len(task_json["task"]) > 80:
        raise TaskFormatError("The length of task name exceeds 80 characters")
    try:
        date_time_obj = datetime.strptime(task_json["date"], '%d/%m/%Y')
        task_json["date"] = date_time_obj.date().strftime('%d/%m/%Y')
    except:
        raise TaskFormatError("The date or date format is not correct")


# route to get all tasks or all tasks on a specific date
@app.route('/tasks', methods=['GET'])
def get_tasks():
    '''
    Get all the tasks in the database
    Return Json value when successful
    Return not found/not exist when no result match
    Return error when input format issue or other exception
    '''
    try:
        date = request.args.get('date', type=str)

        # if data is None, simply return all tasks
        if date == None:
            return_value = Task.get_all_tasks()
            logging.info('Get all Tasks')
            if return_value == []:
                logging.info('No Tasks found')
                return Response('No Tasks found', 200, mimetype='application/json')
            else:
                return jsonify({'Tasks': return_value})
        # date is not None, return tasks on a specific date
        else:
            date_time_obj = datetime.strptime(date, '%d/%m/%Y')

            return_value = Task.get_tasks(date_time_obj.date().strftime('%d/%m/%Y'))
            if return_value == []:
                logging.info('Get Tasks expired on ' + date + ' Not exist ')
                return Response('Get Tasks expired on ' + date  + ' Not exist ', 200, mimetype='application/json')
            else:
                logging.info('Get all Tasks expired on ' + date)
                return jsonify({'Tasks': return_value})
    except ValueError as e:
        if date == None:
            logging.error('Get all Tasks failed ' + str(e))
            return Response("Get all tasks failed", 500, mimetype='application/json')
        else:
            logging.error('Get Tasks expired on  '+ date + " failed date format or value not correct" + str(e))
            return Response('Get Tasks expired on  '+ date + " failed, date format or value not correct ", 500, mimetype='application/json')
    except Exception as e:
        if date == None:
            logging.error('Get all Tasks failed ' + str(e))
            return Response("Get all tasks failed", 500, mimetype='application/json')
        else:
            logging.error('Get Tasks expired on  '+ date + " failed " + str(e))
            return Response('Get Tasks expired on  '+ date + " failed ", 500, mimetype='application/json')


# route to get task by id
@app.route('/tasks/<int:id>', methods=['GET'])
def get_task_by_id(id):
    """
    Get task on a specific id
    Return Json value when successful
    Return not found/not exist when no result match
    Return error when input format issue or other exception
    """
    try:
        return_value = Task.get_task(id)
        if return_value == None:
            logging.error('Get Tasks ' + str(id) + ' Not exist ')
            return Response('Get Tasks ' + str(id) + ' Not exist ', 200, mimetype='application/json')
        logging.info('Get task ' + str(id))
        return jsonify({'Tasks': return_value})
    except Exception as e:
        logging.error('Get Tasks ' + str(id) + ' failed ' + str(e))
        return Response('Get Tasks ' + str(id) + ' failed ', 500, mimetype='application/json')


# route to add new task
@app.route('/tasks', methods=['POST'])
def add_task():
    """
    Add a task by providing task name and date. Task id will be generated automatically 
    and incrementally
    Return ""Task added with ID <id>" when successful
    Return error when input format issue or other exception
    """
    try:
        request_data = request.get_json()  # getting data from client
        validateinput(request_data)
        taskid = Task.add_task(request_data["task"], request_data["date"])
        response = Response("Task added with ID " + str(taskid) , 201, mimetype='application/json')
        logging.info('Add task ' + str(request_data) + 'with ID ' + str(taskid))
        return response
    except TaskFormatError as e:
        logging.error('Add tasks ' + str(request_data) + ' failed ' + str(e))
        return Response('Add tasks ' + str(request_data) + ' failed ' + str(e) , 500, mimetype='application/json')
    except Exception as e:
        logging.error('Add tasks ' + str(request_data) + ' failed ' + str(e))
        return Response('Add tasks ' + str(request_data) + ' failed ', 500, mimetype='application/json')


# route to update task with PUT method
@app.route('/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    """
    Update a task by providing task id, task name and date
    Return "Task updated" when successful
    return not exist if the given id is not found
    Return error when input format issue or other exception
    """
    try:
        request_data = request.get_json()
        validateinput(request_data)
        tasktoupdate =  Task.get_task(id)
        if tasktoupdate == None:
            logging.error('Update task：task ' + str(id) + ' not exist! ')
            return Response('Update task ' + str(id)  + ' not exist ', 200, mimetype='application/json')
        Task.update_task(id, request_data['task'], request_data['date'])
        response = Response("Task updated", status=200, mimetype='application/json')
        logging.info('Update task ' + str(request_data))
        return response
    except TaskFormatError as e:
        logging.error('Update task ' + str(id) + ' with '+ str(request_data) + ' failed ' + str(e))
        return Response('Update task ' + str(id) + ' with ' + str(request_data) + ' failed ', 500, mimetype='application/json')
    except Exception as e:
        logging.error('Update task ' + str(id) + ' with '+ str(request_data) + ' failed ' + str(e))
        return Response('Update task ' + str(id) + ' with ' + str(request_data) + ' failed ', 500, mimetype='application/json')


# route to delete task using the DELETE method
@app.route('/tasks/<int:id>', methods=['DELETE'])
def remove_task(id):
    """
    Delete a task by providing task id
    """
    try:
        Task.delete_task(id)
        response = Response("Task deleted", status=200, mimetype='application/json')
        logging.info('Delete task ' + str(id))
        return response
    except Exception as e:
        logging.error('Delete tasks ' + str(id) + ' failed ' + str(e))
        return Response('Delete task ' + str(id) + ' failed ', 500, mimetype='application/json')



if __name__ == "__main__":
    app.run(port=1234, debug=True)
