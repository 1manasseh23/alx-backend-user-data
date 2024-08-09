#!/usr/bin/env python3
"""Module for session expiration.

This module provides a class that extends session authentication with
support for session expiration.
"""

import os
from datetime import datetime, timedelta
from .session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    """
    SessionExpAuth is a class that extends the functionality of the SessionAuth
    class by adding session expiration to the authentication mechanism.
    """

    def __init__(self):
        """
        Constructor for the SessionExpAuth class.
        Initializes the session_duration attribute based on the
        SESSION_DURATION environment variable.
        """
        super().__init__()
        self.session_duration = int(os.environ.get("SESSION_DURATION", 0))

    def create_session(self, user_id: int) -> str:
        """Creates a new session for a user and assigns a session ID.

        The session ID is stored in the user_id_by_session_id dictionary with
        the user_id and creation time as values. The session has an expiration
        time defined by the session_duration attribute.

        Args:
            user_id (int): The ID of the user to create a session for.

        Returns:
            str: The session ID if the session was successfully created,
                 None otherwise.
        """
        session_id = super().create_session(user_id)

        if session_id is None:
            return None

        self.user_id_by_session_id[session_id] = {
            'user_id': user_id,
            'created_at': datetime.now()
        }

        return session_id

    def user_id_for_session_id(self, session_id: str) -> int:
        """Gets the user ID associated with a session ID.

        The session is considered valid if it was created within the
        session_duration time.

        Args:
            session_id (str): The session ID to get the user ID for.

        Returns:
            int: The user ID associated with the session ID if the session is
                 valid, None otherwise.
        """
        if session_id is None:
            return None

        session_data = self.user_id_by_session_id.get(session_id)
        if session_data is None:
            return None

        if self.session_duration <= 0:
            return session_data.get("user_id")

        created_at = session_data.get('created_at')
        if created_at is None:
            return None

        expiration_time = created_at + timedelta(seconds=self.session_duration)
        if expiration_time < datetime.now():
            return None

        return session_data.get("user_id")
