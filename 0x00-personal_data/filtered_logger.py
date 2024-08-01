#!/usr/bin/env python3
"""
This module provides a function to obfuscate sensitive fields in log messages.
"""

import logging
import re
from typing import List
import os
import mysql.connector
from mysql.connector import Error


def filter_datum(
    fields: List[str],
    redaction: str,
    message: str,
    separator: str
) -> str:
    """
    Obfuscates specified fields in a log message.

    This function replaces the values of the fields listed in `fields`
    with theprovided `redaction` string in the given `message`.
    The fields are separated by the provided `separator` character.

    Args:
        fields (List[str]): A list of field names to obfuscate.
        redaction (str): The string used to replace the values of the fields.
        message (str): The log message containing fields to be obfuscated.
        separator (str): The character separating fields in the log message.

    Returns:
        str: The log message with specified fields obfuscated.
    """
    fields_pattern = "|".join(map(re.escape, fields))
    pattern = (
        f'{re.escape(separator)}({fields_pattern})=[^;]*'
    )

    # Create the replacement pattern
    replacement = (
        fr'{separator}\1={redaction}'
    )

    # Apply the regex substitution
    return re.sub(pattern, replacement, message)


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class for hiding sensitive log information. """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """
        Initializes the RedactingFormatter with fields to be redacted.

        Args:
            fields (List[str]): List of field names to redact in log messages.
        """
        super().__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Formats the log record, redacting specified fields.

        Args:
            record (logging.LogRecord): The log record to format.

        Returns:
            str: The formatted log message with redacted fields.
        """
        message = super().format(record)
        return filter_datum(
            self.fields, self.REDACTION, message, self.SEPARATOR)


# Define the PII_FIELDS constant
PII_FIELDS = (
    "email",        # Email addresses
    "phone",        # Phone numbers
    "ssn",          # Social Security numbers
    "password",     # Passwords
    "ip",           # IP addresses
)


def get_logger() -> logging.Logger:
    """
    Creates and returns a logger named 'user_data'.

    The logger is configured to log messages up to INFO level and uses
    a StreamHandler with RedactingFormatter to redact PII fields.

    Returns:
        logging.Logger: Configured logger instance.
    """

    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    handler = logging.StreamHandler()
    formatter = RedactingFormatter(fields=PII_FIELDS)
    handler.setFormatter(formatter)

    logger.addHandler(handler)

    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """
    Connects to a MySQL database using credentials stored
    in environment variables.

    The following environment variables are used:
        - PERSONAL_DATA_DB_USERNAME: Database username (default: "root")
        - PERSONAL_DATA_DB_PASSWORD: Database password (default: empty string)
        - PERSONAL_DATA_DB_HOST: Database host (default: "localhost")
        - PERSONAL_DATA_DB_NAME: Database name (required)

    Returns:
        mysql.connector.connection.MySQLConnection: Connection
        to the MySQL database.

    Raises:
        Error: If unable to connect to the database.
    """
    try:
        # Retrieve database credentials from environment variables
        username = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
        password = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
        host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
        database = os.getenv("PERSONAL_DATA_DB_NAME")

        if not database:
            raise ValueError(
                "Database name must be set in the environment variable "
                "PERSONAL_DATA_DB_NAME"
            )

        print(
            f"Connecting to database '{database}' with user '{username}' "
            f"on host '{host}'"
        )

        # Connect to the database
        connection = mysql.connector.connect(
            user=username,
            password=password,
            host=host,
            database=database
        )

        return connection

    except Error as e:
        print(f"Error: {e}")
        raise
