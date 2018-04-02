"""API resources definitions."""

import falcon
from models import List, Task
from utils import remove_empty, get_or_404


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
        lists = self.session.query(List).all()
        json = [list.serialized_simple for list in lists]
        response.json = json

    def on_post(self, request, response):
        """Create a new list.

        Payload parameters:

        - title: str, required
            Title of the list.
        """
        title = request.get_json('title', dtype=str)
        list_ = List(title=title)
        self.session.add(list_)
        self.session.commit()
        response.status = falcon.HTTP_201
        response.json = list_.serialized


class ListDetailResource:
    """Manipulate a task list."""

    def get_object(self, id) -> List:
        return get_or_404(self.session, List, id=id)

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
        list_ = self.get_object(id)
        response.json = list_.serialized

    def on_delete(self, request, response, id):
        """Delete a list."""
        list_ = self.get_object(id)
        self.session.delete(list_)
        self.session.commit()
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
        title = request.get_json('title')
        list_id = request.get_json('list_id')
        due_date = request.get_json('due_date', default=None)
        completed = request.get_json('completed', dtype=bool, default=False)
        priority = request.get_json('priority', dtype=int, default=0)

        list_ = get_or_404(self.session, List, id=list_id)

        task = Task(
            title=title,
            list=list_,
            due_date=due_date,
            completed=completed,
            priority=priority)

        self.session.add(task)
        self.session.commit()

        response.status = falcon.HTTP_201
        response.json = task.serialized


class TaskDetailResource:
    """Manipulate a task."""

    def get_object(self, id) -> Task:
        return get_or_404(self.session, Task, id=id)

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
        task = self.get_object(id)
        updated_fields = {
            'title': request.get_json('title', default=None),
            'due_date': request.get_json('due_date', default=None),
            'completed': request.get_json('completed', default=None),
            'priority': request.get_json('priority', default=None),
        }
        cleaned_fields = remove_empty(updated_fields)
        if cleaned_fields:
            for field, value in cleaned_fields.items():
                setattr(task, field, value)
            self.session.add(task)
            self.session.commit()
        response.status = falcon.HTTP_200

    def on_delete(self, request, response, id: int):
        """Delete a task."""
        task = self.get_object(id)
        self.session.delete(task)
        self.session.commit()
        response.status = falcon.HTTP_204
