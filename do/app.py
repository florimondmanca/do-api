"""Do REST API application."""

from datetime import datetime, timedelta

import falcon
import falcon_jsonify

from .middleware import CORS, ResponseLoggerMiddleware

response_logger = ResponseLoggerMiddleware()
logger = response_logger.logger


LISTS = [
    {
        'id': 1,
        'title': 'Shopping',
        'tasks': [0, 1, 2]
    },
    {
        'id': 2,
        'title': 'Trips',
        'tasks': []
    }
]

TASKS = [
    {
        'id': 0,
        'list_id': 1,
        'title': 'Buy grosseries',
        'due_date': falcon.dt_to_http(
            datetime.now() + timedelta(days=1)),
        'completed': False,
        'priority': 2,
    },
    {
        'id': 1,
        'list_id': 1,
        'title': 'Have a nap',
        'due_date': falcon.dt_to_http(
            datetime.now() - timedelta(hours=1)),
        'completed': False,
        'priority': 0,
    },
    {
        'id': 2,
        'list_id': 1,
        'title': 'Make a sandwich',
        'completed': False,
        'priority': 0,
    }
]


def find_or_404(collection, index=False, **kwargs):
    """Find an item matching criteria in a collection, or faise a 404 error.

    Parameters
    ----------
    collection : iterable
    index : boolean, optional (default: False)
        Determines what is returned by this function.
    **kwargs : dict
        Key-value pairs to filter through the collection and find the item.

    Returns
    -------
    item : object or int
        If index=True, returns the position of the item in the collection,
        otherwise returns the item object itself.
    """
    for i, item in enumerate(collection):
        if all(item[k] == v for k, v in kwargs.items()):
            if index:
                return i
            return item
    raise falcon.HTTPNotFound()


def query(collection, **kwargs):
    """Find all items in a collection that meet criteria.

    Note: this is a generator.
    """
    for item in collection:
        if all(item[k] == v for k, v in kwargs.items()):
            yield item


def remove_empty(dictionnary):
    """Remove items whose value is None in a dictionnary."""
    return {k: v for k, v in dictionnary.items() if v is not None}


class ListResource:
    """Manipulate lists."""

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
            for list_ in LISTS
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
        doc = find_or_404(LISTS, id=id)
        doc['tasks'] = list(query(TASKS, list_id=id))
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
        list_ = find_or_404(LISTS, id=task['list_id'])
        task['id'] = len(list_['tasks'])

        TASKS.append(task)
        list_['tasks'].append(task['id'])

        response.status = falcon.HTTP_201
        response.json = task


class TaskDetailResource:
    """Manipulate a task."""

    def on_patch(self, request, response, id: int):
        """Update a task.

        The following fields can be passed in the payload to be updated:
            title, due_date, completed, priority
        Any other field will be ignored.

        Example payload:
        ```
        {
            "completed": true
        }
        ```

        Example response: no response body.
        """
        task = find_or_404(TASKS, id=id)
        updatable = ('title', 'due_date', 'completed', 'priority')
        updated_fields = remove_empty({
            param: request.json.pop(param, None) for param in updatable
        })
        task.update(**updated_fields)
        response.status = falcon.HTTP_200

    def on_delete(self, request, response, id: int):
        """Delete a task."""
        task_index = find_or_404(TASKS, index=True, id=id)
        print(task_index)
        TASKS.pop(task_index)
        response.status = falcon.HTTP_204


app = falcon.API(middleware=[
    CORS(
        allow_all_methods=True,
        allow_all_origins=True,
        allowed_headers=['content-type'],
    ).middleware,
    response_logger,
    falcon_jsonify.Middleware(help_messages=True),
])

# Resources and routes
app.add_route('/lists', ListResource())
app.add_route('/lists/{id:int}', ListDetailResource())
app.add_route('/tasks/', TaskResource())
app.add_route('/tasks/{id:int}', TaskDetailResource())

# WSGI application
application = app
