#! /usr/bin/env python3
"""Do API management CLI."""

import sys
import os
from subprocess import run

import click

from helpers import load_settings
from helpers.db import apply_migrations, create_migrations
from helpers.shell import success

os.environ.setdefault('SETTINGS_MODULE', 'settings')
settings = load_settings()
database = settings.DATABASE_BACKEND

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
@click.argument('message')
def makemigrations(message: str):
    """Generate migrations with Alembic."""
    if create_migrations(message):
        click.echo(OK)
    else:
        sys.exit(1)


@cli.command()
def createdb():
    """Create a database and apply migrations on it."""
    if database.exists():
        raise click.UsageError(
            click.style('Database already exists at {}.'
                        .format(database.url), fg='red')
        )
    else:
        database.create()
        click.echo(OK)


@cli.command()
def dropdb():
    """Drop the database."""
    message = 'This will permanently drop the database. Continue?'
    if click.confirm(message, abort=True):
        database.drop()
        click.echo(OK)


@cli.command()
def migrate():
    """Run migrations using `alembic upgrade head`."""
    if apply_migrations():
        click.echo(OK)
    else:
        sys.exit(1)


@cli.command()
@click.option('--verbose', '-v', is_flag=True, help='Turn verbosity up')
def test(verbose):
    """Run the tests."""
    verbose_opts = verbose and ['-v'] or []
    if success(['python', '-m', 'pytest', *verbose_opts]):
        click.secho('Tests passed! 🎉', fg='green')
    else:
        sys.exit(1)


if __name__ == '__main__':
    cli()
