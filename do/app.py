import json
from datetime import datetime, timedelta

import falcon

from .cors import CORS


class TaskResource:

    def on_get(self, request, response):
        # Example document to return
        # TODO: retrieve from a storage
        doc = {
            'tasks': [
                {
                    'id': 1,
                    'title': 'Buy grosseries',
                    'due_date': falcon.dt_to_http(
                        datetime.now() + timedelta(days=1)),
                },
                {
                    'id': 2,
                    'title': 'Have a nap',
                    'due_date': falcon.dt_to_http(
                        datetime.now() - timedelta(hours=1)),
                }
            ]
        }
        response.status = falcon.HTTP_200
        response.body = json.dumps(doc, ensure_ascii=False)


app = falcon.API(middleware=[
    CORS(allow_all_origins=True).middleware,
])

# Resources and routes
app.add_route('/tasks', TaskResource())

# WSGI application
application = app
