#! /usr/bin/env python3
"""Do API management CLI."""

from subprocess import run

import click

from helpers import load_settings
from helpers.db import (apply_migrations, create_migrations, db_exists,
                        delete_database)
from helpers.shell import success

settings = load_settings()


# Commands
GUNICORN = ['gunicorn', '--reload', 'wsgi']


@click.group()
def cli():
    """Main entry point."""


@cli.command()
def start():
    """Start the server."""
    run(GUNICORN)


@cli.command()
def initdb():
    """Initialize the database."""
    name = settings.DATABASE_NAME
    if db_exists(name):
        raise click.UsageError('Database {} already exists.'.format(name))
    if apply_migrations():
        print('OK')


@cli.command()
@click.argument('message')
def makemigrations(message: str):
    """Generate migrations with Alembic."""
    if create_migrations(message):
        print('OK')


@cli.command()
def migrate():
    """Run migrations using `alembic upgrade head`."""
    if apply_migrations():
        print('OK')


@cli.command()
def rmdb():
    """Delete the database altogether."""
    name = settings.DATABASE_NAME
    if db_exists(name):
        click.confirm(
            'This will erase the database permanently. Continue?',
            abort=True)
        if delete_database(name):
            print('Removed database {}'.format(name))
    else:
        print('No database found.')


if __name__ == '__main__':
    cli()
