# Do API

This is the backend API for the Do project.

## Installation

- Make sure you have **Python 3.3+** installed.
- Create a virtual environment and install dependencies:

```bash
$ python3 -m venv env
$ . env/bin/activate
$ pip install -r requirements.txt
```

- Start the app using Gunicorn (`--reload` enables hot reload of the app on code changes):

```bash
$ ./env/bin/gunicorn --reload do.app
```

## Resources documentation (WIP)

### Tasks

#### `GET /tasks`

Return all the available tasks.

#### `GET /tasks/:id`

Return a task identified by its `id`.
