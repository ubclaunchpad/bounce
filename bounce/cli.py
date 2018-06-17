"""
Defines Bounce's command line interface.
"""

import click

from .server import Server
from .server.api.users import UsersEndpoint
from .server.config import ServerConfig


@click.group()
def cli():
    """Represents a group of CLI commands."""
    pass


@cli.command()
@click.option(
    '--port',
    '-l',
    help='port the HTTP server should listen on',
    envvar='PORT')
@click.option(
    '--pg-host',
    '-h',
    help='hostname of the Postgres instance the server should rely on',
    envvar='POSTGRES_HOST')
@click.option(
    '--pg-port',
    '-s',
    help='port the Postgres daemon is listening on',
    envvar='POSTGRES_PORT')
@click.option(
    '--pg-user',
    '-u',
    help='name of the Postgres user the server should use to access the DB',
    envvar='POSTGRES_USER')
@click.option(
    '--pg-password',
    '-p',
    help='password the server should use to access the DB',
    envvar='POSTGRES_PASSWORD')
@click.option(
    '--pg-database',
    '-d',
    help='the name of the Postgres database the server should use',
    envvar='POSTGRES_DB')
def start(port, pg_host, pg_port, pg_user, pg_password, pg_database):
    """Starts the Bounce webserver with the given configuration."""
    conf = ServerConfig(port, pg_host, pg_port, pg_user, pg_password,
                        pg_database)
    # Register your new endpoints here
    endpoints = [UsersEndpoint]
    serv = Server(conf, endpoints)
    serv.start()
