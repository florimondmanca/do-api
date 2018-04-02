#! /usr/bin/env python3
"""Do API management CLI."""

import os
from subprocess import run, CompletedProcess

import click

from db import settings

# Commands
ALEMBIC_UPGRADE_HEAD = ['alembic', 'upgrade', 'head']
ALEMBIC_GENERATE = ['alembic', 'revision', '--autogenerate']
GUNICORN = ['gunicorn', '--reload', 'wsgi']


def success(cmd: CompletedProcess):
    """Return whether a process successfully terminated."""
    return cmd.returncode == 0


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
    if success(run(ALEMBIC_UPGRADE_HEAD)):
        print('OK')


@cli.command()
@click.argument('message')
def makemigrations(message: str):
    """Generate migrations with Alembic."""
    message_opts = message and ['-m', message] or []
    if success(run([*ALEMBIC_GENERATE, *message_opts])):
        print('OK')


@cli.command()
def migrate():
    """Run migrations using `alembic upgrade head`."""
    if success(run(ALEMBIC_UPGRADE_HEAD)):
        print('OK')


@cli.command()
def rmdb():
    """Delete the database altogether."""
    name = settings.DATABASE_NAME
    if os.path.exists(name):
        click.confirm(
            'This will erase the database permanently. Continue?',
            abort=True)
        if success(run(['rm', name])):
            print(f'Removed database {name}')
    else:
        print(f'No database found.')


if __name__ == '__main__':
    cli()
