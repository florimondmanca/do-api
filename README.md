# Do API

This is the backend API for the Do project.

Made with [Falcon](https://falcon.readthedocs.io/en/stable/), the [SQLAlchemy](http://www.sqlalchemy.org) ORM and [Alembic](http://alembic.zzzcomputing.com) for database migrations. Management CLI written with [Click](http://click.pocoo.org/5/).

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
$ ./cli.py migrate
```

then start the Gunicorn server:

```bash
$ ./cli.py start
```

## Using the CLI

The `cli.py` script provides a few management commands. Make sure to always execute it in the project's root directory as `$ ./cli.py [...]`.

Commands:

- `--help`: show the entry point's documentation.

- `<COMMAND> --help`: show help about a command.

- `start`: start the app server.

- `initdb`: initialize the database. This creates a SQLite database file and runs an initial migration to get it up to date.

- `makemigrations MESSAGE`: autogenerate a new migration. A descriptive message must be provided.

- `migrate`: upgrade the database using the migrations found in `migrations/versions/`.

- `rmdb`: delete the database.

## Resources documentation

> TODO

## Running tests

> TODO
