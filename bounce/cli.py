"""
Defines Bounce's command line interface.
"""

import logging

import click
from sanic.log import logger

from .server import Server
from .server.api.clubs import ClubEndpoint, ClubsEndpoint
from .server.api.users import UserEndpoint, UsersEndpoint
from .server.config import ServerConfig


@click.group()
def cli():
    """Represents a group of CLI commands."""
    pass


@cli.command()
@click.option(
    '--port',
    '-n',
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
@click.option(
    '--loglevel',
    '-l',
    help='the level to log at [critical, error, warning, info, debug]',
    default='debug')
def start(port, pg_host, pg_port, pg_user, pg_password, pg_database, loglevel):
    """Starts the Bounce webserver with the given configuration."""
    # Set log level
    logger.setLevel(getattr(logging, loglevel.upper()))
    conf = ServerConfig(port, pg_host, pg_port, pg_user, pg_password,
                        pg_database)
    # Register your new endpoints here
    endpoints = [UsersEndpoint, UserEndpoint, ClubsEndpoint, ClubEndpoint]
    serv = Server(conf, endpoints)
    serv.start()
