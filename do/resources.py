"""API resources definitions."""

import falcon

from .db import Database as db
from .utils import find_or_404, query, remove_empty


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
        # TODO: retrieve from storage
        doc = [
            {
                'title': list_['title'],
                'id': list_['id'],
            }
            for list_ in db.lists
        ]
        response.json = doc


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
        doc = find_or_404(db.lists, id=id)
        doc['tasks'] = list(query(db.tasks, list_id=id))
        response.json = doc


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
        task_index = find_or_404(db.tasks, index=True, id=id)
        print(task_index)
        db.tasks.pop(task_index)
        response.status = falcon.HTTP_204
