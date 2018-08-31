"""Configuration for the Bounce webserver."""


class ServerConfig:
    """Stores configuration for the server."""

    def __init__(self, port, secret, pg_host, pg_port, pg_user, pg_password,
                 pg_database, allowed_origin, image_dir):
        self._server_port = port
        self._secret = secret
        self._postgres_host = pg_host
        self._postgres_port = pg_port
        self._postgres_user = pg_user
        self._postgres_password = pg_password
        self._postgres_db = pg_database
        self._allowed_origin = allowed_origin
        self._image_dir = image_dir

    # Expose attributes as properties so they can't be modified after
    # they've been set.

    @property
    def secret(self):
        """Returns the secret for this server."""
        return self._secret

    @property
    def server_port(self):
        """Returns the port the server should listen on."""
        return self._server_port

    @property
    def postgres_host(self):
        """Returns the hostname of the Postgres instance this server uses."""
        return self._postgres_host

    @property
    def postgres_port(self):
        """Returns the port Postgres is listening on."""
        return self._postgres_port

    @property
    def postgres_user(self):
        """Returns the username to use when querying our Postgres DB."""
        return self._postgres_user

    @property
    def postgres_password(self):
        """Returns the password to use when querying our Postgres DB."""
        return self._postgres_password

    @property
    def postgres_db(self):
        """Returns the name of our Postgres DB."""
        return self._postgres_db

    @property
    def allowed_origin(self):
        """Returns the name of the domain that is allowed to access data served
        by this server, or None is one is not configured.
        """
        return self._allowed_origin or None

    @property
    def image_dir(self):
        """Returns the path to the location images are stored at."""
        return self._image_dir
