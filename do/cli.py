#! /usr/bin/env python3
"""Do API management CLI."""

from subprocess import run

import click

from db import create_tables


@click.group()
def cli():
    """Main entry point."""


@cli.command()
def start():
    """Start the server."""
    run(['gunicorn', '--reload','wsgi'])


@cli.command()
def initdb():
    """Initialize the database."""
    create_tables()


if __name__ == '__main__':
    cli()
