"""

Unit test

"""

import unittest
import json
from api import app
from task import db
import time

class TestTask(unittest.TestCase):

    def test_add_task(self):
        """
        Test on adding a task
        """
        tester = app.test_client()
        payload = json.dumps({
            "task": "Backup log",
            "date": "10/7/2022"
        })
        response = tester.post('/tasks', headers={"Content-Type": "application/json"}, data=payload)
        self.assertEqual(201, response.status_code)

    def test_get_task_by_id(self):
        """
        Test on getting a task by id
        """
        tester = app.test_client()
        response = tester.get("/tasks/1")
        statuscode = response.status_code
        self.assertEqual(200, statuscode)

    def test_get_all_tasks(self):
        """
        Test on getting all tasks
        """
        tester = app.test_client()
        response = tester.get("/tasks")
        statuscode = response.status_code
        self.assertEqual(200, statuscode)
        self.assertEqual(response.content_type, "application/json")


    def test_get_all_tasks_bydate(self):
        """
        Test on getting a task by a given date 
        """
        tester = app.test_client()
        payload = json.dumps({
            "task": "test update",
            "date": "11/07/2022"
        })

        response = tester.post('/tasks', headers={"Content-Type": "application/json"}, data=payload)
        if response.status_code == 201:
             responseresult = response.text
             seg = responseresult.split(" ")

             response = tester.get("/tasks?date=11/07/2022")
             self.assertEqual(200, response.status_code)

             if response.text != None:
                self.assertTrue(response.text.find("11/07/2022") != -1)

        else:
            self.assertFalse()



    def test_update_tasks(self):
        """
        Test on update a task 
        """
        tester = app.test_client()
        payload = json.dumps({
            "task": "test update",
            "date": "11/7/2022"
        })

        response = tester.post('/tasks', headers={"Content-Type": "application/json"}, data=payload)
        if response.status_code == 201:
             responseresult = response.text
             if responseresult != None:
                seg = responseresult.split(" ")
                payload = json.dumps({
                     "task": "update success",
                    "date": "12/7/2022"
                })
                response = tester.put('/tasks/'+str(seg[-1]), headers={"Content-Type": "application/json"}, data=payload)
                self.assertEqual(200, response.status_code)
             else:
                 self.assertFalse()

        else:
            self.assertFalse()


    def test_delete_tasks(self):
        """
        Test on deleting a task 
        """
        tester = app.test_client()

        payload = json.dumps({
            "task": "test delete",
            "date": "11/7/2022"
        })

        response = tester.post('/tasks', headers={"Content-Type": "application/json"}, data=payload)
        if response.status_code == 201:
             responseresult = response.text
             if responseresult != None:
                seg = responseresult.split(" ")

                payload = json.dumps({
                     "task": "Backup log Update",
                    "date": "12/7/2022"
                })

                response = tester.delete('/tasks/'+str(seg[-1]), headers={"Content-Type": "application/json"})
                self.assertEqual(200, response.status_code)

             else:
                 self.assertFalse()
        else:
            self.assertFalse()

    def test_get_all_tasks_with_database_issue(self):
        """
        Test on getting all tasks with internal exception 
        Drop the db to simulate internal exception
        """
        tester = app.test_client()
        db.drop_all()

        response = tester.get("/tasks")
        statuscode = response.status_code
        db.create_all()

        self.assertEqual(500, statuscode)
        if response.text != None:
            self.assertEqual(response.text, "Get all tasks failed")













if __name__ == '__main__':
    unittest.main()
