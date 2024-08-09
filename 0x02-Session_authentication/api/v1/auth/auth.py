#!/usr/bin/env python3
"""
Module for authentication.

This module defines a base class `Auth` that provides methods to handle
authentication tasks such as checking if a path requires authentication,
retrieving authorization headers, and session cookies.
"""

import os
from typing import List, TypeVar
from flask import request


class Auth:
    """Template for all authentication systems implemented in this app.

    This class provides methods that are common to all authentication
    mechanisms, such as checking if a request path requires authentication,
    extracting authorization headers, and managing session cookies.
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Determines if a given path requires authentication.

        This method checks if the provided path is within the list of excluded
        paths. If the path is not excluded, authentication is required.

        Args:
            path (str): The path to check against the list of excluded paths.
            excluded_paths (List[str]): The list of excluded paths.

        Returns:
            bool: True if the path requires authentication, False otherwise.
        """
        if not path:
            return True

        if not excluded_paths:
            return True

        path = path.rstrip("/")

        for excluded_path in excluded_paths:
            if excluded_path.endswith("*") and path.startswith(excluded_path[:-1]):
                return False
            elif path == excluded_path.rstrip("/"):
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """Retrieves the value of the Authorization header from the request.

        Args:
            request (flask.request, optional): The request object. Defaults to None.

        Returns:
            str: The value of the Authorization header or None if not present.
        """
        if request is not None:
            return request.headers.get('Authorization', None)
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Retrieves the current user from the request.

        This method is intended to be overridden by subclasses to provide the
        logic for retrieving the current user based on the request.

        Args:
            request (flask.request, optional): The request object. Defaults to None.

        Returns:
            TypeVar('User'): The current user, or None if not available.
        """
        return None

    def session_cookie(self, request=None) -> str:
        """Retrieves the session cookie from the request.

        Args:
            request (flask.request, optional): The request object. Defaults to None.

        Returns:
            str: The value of the session cookie, or None if the request or cookie is invalid.
        """
        if request is not None:
            cookie_name = os.getenv('SESSION_NAME')
            return request.cookies.get(cookie_name)
        return None
