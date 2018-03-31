"""Do REST API application."""

import json
from datetime import datetime, timedelta

import falcon

from .middleware import CORS
from .middleware import ResponseLoggerMiddleware

response_logger = ResponseLoggerMiddleware()
logger = response_logger.logger


LISTS = [
    {
        'id': 1,
        'title': 'Shopping',
        'tasks': [
            {
                'id': 1,
                'title': 'Buy grosseries',
                'due_date': falcon.dt_to_http(
                    datetime.now() + timedelta(days=1)),
                'completed': False,
                'priority': 2,
            },
            {
                'id': 2,
                'title': 'Have a nap',
                'due_date': falcon.dt_to_http(
                    datetime.now() - timedelta(hours=1)),
                'completed': False,
                'priority': 0,
            },
            {
                'id': 3,
                'title': 'Make a sandwich',
                'completed': False,
                'priority': 0,
            }
        ]
    },
    {
        'id': 2,
        'title': 'Trips',
        'tasks': []
    }
]


def find_or_404(collection, **kwargs):
    for item in collection:
        if all(item[k] == v for k, v in kwargs.items()):
            return item
    raise falcon.HTTPNotFound()


def read_json_or_bad_request(request):
    try:
        return json.load(request.bounded_stream)
    except json.JSONDecodeError as e:
        raise falcon.HTTPBadRequest(title='JSON is malformed',
                                    description=e.msg)


def check_required_or_bad_request(data: dict, required):
    for param in required:
        if param not in data:
            raise falcon.HTTPMissingParam(param)


class ListResource:

    def on_get(self, request, response):
        # TODO: retrieve from storage
        doc = [
            {
                **{k: list_[k] for k in ('id', 'title')},
                'url': '/lists/{}'.format(list_['id'])
            }
            for list_ in LISTS
        ]
        response.status = falcon.HTTP_200
        response.body = json.dumps(doc, ensure_ascii=False)


class ListDetailResource:

    def on_get(self, request, response, id: int):
        doc = find_or_404(LISTS, id=id)
        response.status = falcon.HTTP_200
        response.body = json.dumps(doc, ensure_ascii=False)


class TaskResource:

    def on_post(self, request, response, list_id: int):
        list_ = find_or_404(LISTS, id=list_id)
        task = read_json_or_bad_request(request)
        check_required_or_bad_request(task, ('title',))

        task['id'] = len(list_['tasks'])
        task.setdefault('due_date', None)
        task.setdefault('completed', False)
        task.setdefault('priority', 0)

        list_['tasks'].append(task)

        logger.info(str(task))
        response.status = falcon.HTTP_201
        response.body = json.dumps(task, ensure_ascii=False)


app = falcon.API(middleware=[
    CORS(allow_all_origins=True, allowed_headers=['content-type']).middleware,
    response_logger,
])

# Resources and routes
app.add_route('/lists', ListResource())
app.add_route('/lists/{id:int}', ListDetailResource())
app.add_route('/tasks/{list_id:int}', TaskResource())

# WSGI application
application = app
