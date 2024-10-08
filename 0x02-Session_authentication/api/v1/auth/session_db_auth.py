#!/usr/bin/env python3
"""Module for session database authentication.
This module provides a class that handles session authentication with
database storage and expiration support.
"""

from datetime import datetime, timedelta
from models.user_session import UserSession
from .session_exp_auth import SessionExpAuth


class SessionDBAuth(SessionExpAuth):
    """Session authentication class with database storage & expiration support.

    This class extends the session expiration authentication by adding
    functionality to store session data in a database.
    """

    def create_session(self, user_id: str) -> str:
        """Creates and stores a session ID for the user.

        Args:
            user_id (str): User ID to be associated with the session.

        Returns:
            str: Session ID if created successfully, None otherwise.
        """
        session_id = super().create_session(user_id)

        if isinstance(session_id, str):
            user_session = UserSession(user_id=user_id, session_id=session_id)
            user_session.save()
            return session_id
        return None

    def user_id_for_session_id(self, session_id: str) -> str:
        """Retrieves the user id of the user associated with given session id.

        Args:
            session_id (str): Session id.

        Returns:
            str: User id associated with the session id.
        """
        try:
            sessions = UserSession.search({'session_id': session_id})
        except Exception:
            return None

        if len(sessions) <= 0:
            return None

        # Check the expiration time of the session
        session = sessions[0]
        cur_time = datetime.now()
        time_span = timedelta(seconds=self.session_duration)
        exp_time = session.created_at + time_span

        if exp_time < cur_time:
            return None

        return session.user_id

    def destroy_session(self, request=None) -> bool:
        """Destroys an authenticated session.

        Args:
            request (flask.Request, optional): The request object containing
            the session cookie. Defaults to None.

        Returns:
            bool: True if the session was destroyed successfully,
            False otherwise.
        """
        session_id = self.session_cookie(request)
        if not session_id:
            return False

        try:
            sessions = UserSession.search({'session_id': session_id})
        except Exception:
            return False

        if not sessions:
            return False

        sessions[0].remove()
        return True
