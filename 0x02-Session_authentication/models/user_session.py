#!/usr/bin/env python3
"""
Module for user session.

This module defines the `UserSession` class, which represents a session
associated with a user. It inherits from the `Base` class.
"""

from models.base import Base


class UserSession(Base):
    """
    User session class.

    This class is used to create and manage user sessions, storing the
    session ID and associated user ID.
    """

    def __init__(self, *args: list, **kwargs: dict):
        """
        Initializes a UserSession instance.

        Args:
            *args (list): Variable length argument list.
            **kwargs (dict): Arbitrary keyword arguments, expected to contain
            'user_id' and 'session_id'.
        """
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')
