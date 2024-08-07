#!/usr/bin/python3
""" Authentication module """

from flask import request
from typing import List, TypeVar


class Auth:
    """ Auth class to manage API authentication """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Method to determine if authentication is required.
        Args:
            path (str): The path to check.
            excluded_paths (List[str]): List of paths that do not require authentication.
        Returns:
            bool: True if authentication is required, False otherwise.
        """
        if path is None:
            return True
        if not excluded_paths:
            return True

        # Ensure path and excluded paths end with a slash
        if not path.endswith('/'):
            path += '/'

        for excluded_path in excluded_paths:
            if excluded_path.endswith('/'):
                if path == excluded_path:
                    return False
            elif path == excluded_path + '/':
                return False

        return True

    
    def authorization_header(self, request=None) -> str:
        """
        Method to get the Authorization header from the request.
        Args:
            request: The Flask request object.
        Returns:
            str: None for now, actual logic to be implemented later.
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Method to get the current user from the request.
        Args:
            request: The Flask request object.
        Returns:
            TypeVar('User'): None for now, actual
            logic to be implemented later.
        """
        return None
