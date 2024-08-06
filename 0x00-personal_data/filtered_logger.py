#!/usr/bin/env python3
"""
Module for custom logging formatter that redacts specified fields.
"""

import logging
from typing import List
from filter_datum import filter_datum  # Assuming filter_datum is in filter_datum.py


def filter_datum(
        fields: List[str],
        redaction: str,
        message: str,
        separator: str
        ) -> str:
    """
    Obfuscates specified fields in a log message.

    This function replaces the values of the fields listed in `fields` with the 
    provided `redaction` string in the given `message`. The fields are separated 
    by the provided `separator` character.

    Args:
    fields (List[str]): A list of field names to obfuscate.
    redaction (str): The string used to replace the values of the fields.
    message (str): The log message containing fields to be obfuscated.
    separator (str): The character separating fields in the log m
    
    messtr: The log message with specified fields obfuscated.
    """
    
    pattern = f'{re.escape(separator)}({"|".join(map(re.escape, fields))})=[^replacement = fr'{separator}\1={redaction}'
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

    super().__init__(self.FORMAt)
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
    return filter_datum(self.fields, self.REDACTION, message, self.SEPARATOR)
