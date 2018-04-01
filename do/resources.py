"""API resources definitions."""

from pprint import pprint
import falcon
from db import Database as db
from db import List, Task
from utils import find_or_404, find_maybe, query, remove_empty


class ListResource:
    """Manipulate task lists."""

    def on_get(self, request, response):
        """Retrieve all lists.

        Example response:

        ```
        [
            {
                "title": "Shopping",
                "id": 2
            },
            {
                "title": "Trips",
                "id": 3
            }
        ]
        ```
        """
        lists = []
        for list_ in db.lists:
            lists.append({
                'title': list_['title'],
                'id': list_['id'],
                'tasks': list(query(db.tasks, list_id=list_['id'])),
            })
        json = lists
        # lists = self.session.query(List).all()
        # json = [list.serialized for list in lists]
        response.json = json

    def on_post(self, request, response):
        """Create a new list.

        Payload parameters:

        - title: str, required
            Title of the list.
        """
        list_ = {
            'title': request.get_json('title'),
        }
        list_['id'] = len(db.lists)
        list_['tasks'] = []

        db.lists.append(list_)

        response.status = falcon.HTTP_201
        response.json = list_


class ListDetailResource:
    """Manipulate a task list."""

    def on_get(self, request, response, id: int):
        """Retrieve a list and its tasks.

        Example response:

        ```
        {
            "id": 2,
            "title": "Shopping",
            "tasks": [
                {
                    "id": 1,
                    "list_id": 2,
                    "title": "Buy groceries",
                    "due_date": null,
                    "completed": false,
                    "priority": 0
                }
            ]
        }
        ```
        """
        doc = find_or_404(db.lists, id=id).copy()
        doc['tasks'] = list(query(db.tasks, list_id=id))
        response.json = doc

    def on_delete(self, request, response, id):
        """Delete a list."""
        index, list_ = find_or_404(db.lists, with_index=True, id=id)

        # Remove associated tasks
        for task_id in list_['tasks']:
            task_index = find_maybe(db.tasks, index=True, id=task_id)
            if task_index is not None:
                db.tasks.pop(task_index)

        db.lists.pop(index)
        response.status_code = falcon.HTTP_204


class TaskResource:
    """Manipulate tasks."""

    def on_post(self, request, response):
        """Create a new task.

        Payload parameters:

        title: str, required
            Title of the task.
        list_id: int, required
            ID of the list to add this task to.
        due_date: str, optional (default: None)
            Date by which the task has to be done.
            Send in ISO format.
        completed: bool, optional (default: False)
            Whether this task is completed.
        Priority: int, optional (default: 0)
            How urgent is the task. The higher the more important.

        Example response:
        ```
        {
            'id': 2,
            'list_id': 2,
            'title': 'Make a sandwich',
            'due_date': null,
            'completed': false,
            priority: 0
        }
        ```
        """
        task = {
            'title': request.get_json('title'),
            'list_id': request.get_json('list_id'),
            'due_date': request.get_json('due_date', default=None),
            'completed': request.get_json('completed', dtype=bool,
                                          default=False),
            'priority': request.get_json('priority', dtype=int, default=0),
        }
        # Add the task to a list
        list_ = find_or_404(db.lists, id=task['list_id'])
        task['id'] = len(list_['tasks'])

        db.tasks.append(task)
        list_['tasks'].append(task['id'])

        response.status = falcon.HTTP_201
        response.json = task


class TaskDetailResource:
    """Manipulate a task."""

    def on_patch(self, request, response, id: int):
        """(Partially) update a task.

        Example payload: `{"completed": true}`

        The following fields can be passed in the payload to be updated
        (any other field will be ignored):

        - title: str
        - due_date: str (ISO format)
        - completed: bool
        - priority: int
        """
        task = find_or_404(db.tasks, id=id)
        updated_fields = {
            'title': request.get_json('title', default=None),
            'due_date': request.get_json('due_date', default=None),
            'completed': request.get_json('completed', default=None),
            'priority': request.get_json('priority', default=None),
        }
        cleaned_fields = remove_empty(updated_fields)
        task.update(**cleaned_fields)
        response.status = falcon.HTTP_200

    def on_delete(self, request, response, id: int):
        """Delete a task."""
        index, task = find_or_404(db.tasks, with_index=True, id=id)

        # Remove the task from its list
        list_ = find_maybe(db.lists, id=task['list_id'])
        list_['tasks'].remove(task['id'])

        db.tasks.pop(index)
        response.status = falcon.HTTP_204
