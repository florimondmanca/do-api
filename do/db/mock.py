from datetime import datetime, timedelta

import falcon

LISTS = [
    {
        'id': 0,
        'title': 'Shopping',
        'tasks': [0, 1]
    },
    {
        'id': 1,
        'title': 'Trips',
        'tasks': [2]
    }
]

TASKS = [
    {
        'id': 0,
        'list_id': 0,
        'title': 'Buy grosseries',
        'due_date': falcon.dt_to_http(
            datetime.now() + timedelta(days=1)),
        'completed': False,
        'priority': 2,
    },
    {
        'id': 1,
        'list_id': 0,
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


class Database:
    lists = LISTS
    tasks = TASKS
