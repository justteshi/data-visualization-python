"""MySQL connection configuration for the legacy visualization application."""

import os

from dotenv import load_dotenv
from mysql import connector


class DatabaseConfigurationError(RuntimeError):
    """Raised when database environment variables are missing or invalid."""


class DatabaseConnectionError(RuntimeError):
    """Raised when MySQL cannot be reached with the configured settings."""


def _database_config():
    load_dotenv()

    variable_names = (
        "DB_HOST",
        "DB_PORT",
        "DB_NAME",
        "DB_USER",
        "DB_PASSWORD",
    )
    values = {name: os.environ.get(name) for name in variable_names}
    missing = [name for name, value in values.items() if value is None]

    if missing:
        raise DatabaseConfigurationError(
            "Missing required database environment variables: "
            + ", ".join(missing)
        )

    try:
        port = int(values["DB_PORT"])
    except ValueError as error:
        raise DatabaseConfigurationError(
            "DB_PORT must be an integer between 1 and 65535."
        ) from error

    if not 1 <= port <= 65535:
        raise DatabaseConfigurationError(
            "DB_PORT must be an integer between 1 and 65535."
        )

    return {
        "host": values["DB_HOST"],
        "port": port,
        "database": values["DB_NAME"],
        "user": values["DB_USER"],
        "password": values["DB_PASSWORD"],
    }


def connect_mysql():
    """Create a MySQL connection using environment-based configuration."""
    try:
        return connector.connect(**_database_config())
    except connector.Error:
        raise DatabaseConnectionError(
            "Unable to connect to MySQL. Check the DB_* configuration and "
            "confirm that the database server is available."
        ) from None
