# Do API

This is the backend API for the Do project.

Made with [Falcon](https://falcon.readthedocs.io/en/stable/). Uses the [SQLAlchemy](http://www.sqlalchemy.org) ORM and [Alembic](http://alembic.zzzcomputing.com) for database migrations. The management CLI is written with [click](http://click.pocoo.org/5/) and tests are written with [pytest](https://docs.pytest.org/en/latest/contents.html).

## Installation

Make sure you have **Python 3.3+** installed, then create a virtual environment and install dependencies:

```bash
$ python3 -m venv env
$ . env/bin/activate
$ pip install -r requirements.txt
```

## Quick start

After installing, setup the database:

```bash
$ cd do/
$ ./cli.py initdb
```

then start the Gunicorn server:

```bash
$ ./cli.py start
```

## Using the CLI

The `cli.py` script provides a few management commands. You can execute it while in the project's root directory using `$ python cli.py ...` or simply `$ ./cli.py ...`.

Commands:

- `--help`: show the entry point's documentation.

- `<COMMAND> --help`: show help details about a command.

- `start`: start the app server.

- `initdb`: initialize the database. This wrapper around `migrate` first checks that no database already exists.

- `makemigrations MESSAGE`: autogenerate a new migration. A descriptive message must be provided.

- `migrate`: upgrade the database using the migrations found in `migrations/versions/`. Note that if no database exists, it will create one.

- `rmdb`: delete the database (if one exists).

- `test`: run the tests. This will create a test database and will not affect any database previously created.

## API documentation

> TODO

## Running tests

You can run the tests from the CLI:

```bash
$ cd do/
$ ./cli.py test
```

For finer control, you may want to use pytest directly. For example, to prevent pytest from capturing output:

```bash
$ python -m pytest -s
```
