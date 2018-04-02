#! /usr/bin/env python3
"""Do API management CLI."""

import os
from subprocess import run

import click

from helpers import load_settings
from helpers.db import (apply_migrations, create_migrations, db_exists,
                        delete_database)
from helpers.shell import success

os.environ.setdefault('SETTINGS_MODULE', 'settings')
settings = load_settings()

OK = click.style('OK', fg='green')
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
    """Create a database and apply migrations on it."""
    name = settings.DATABASE_NAME
    if db_exists(name):
        raise click.UsageError(
            click.style('Database {} already exists.'.format(name), fg='red')
        )
    if apply_migrations():
        click.echo(OK)


@cli.command()
@click.argument('message')
def makemigrations(message: str):
    """Generate migrations with Alembic."""
    if create_migrations(message):
        click.echo(OK)


@cli.command()
def migrate():
    """Run migrations using `alembic upgrade head`."""
    if apply_migrations():
        click.echo(OK)


@cli.command()
def rmdb():
    """Delete the database altogether."""
    name = settings.DATABASE_NAME
    if db_exists(name):
        click.confirm(
            'This will erase the database permanently. Continue?',
            abort=True)
        if delete_database(name):
            click.secho('Removed database {}'.format(name), fg='green')
    else:
        click.secho('No database found.', fg='red')


@cli.command()
@click.option('--verbose', '-v', is_flag=True, help='Turn verbosity up')
def test(verbose):
    """Run the tests."""
    verbose_opts = verbose and ['-v'] or []
    if success(['python', '-m', 'pytest', *verbose_opts]):
        click.secho('Tests passed! 🎉', fg='green')


if __name__ == '__main__':
    cli()
