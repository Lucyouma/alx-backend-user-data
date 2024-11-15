#!/usr/bin/env python3
"""
module template for
authentication class
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """
    class to manage API authentication
    """
    def __init__(self):
        """
        class initialization
        """
        self.data = []

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        returns whether authentication is required
        - returns True if path is None or
        if excluded_path is empty or None
        - Handles paths to be slash tolerant
        """
        if path is None:
            return True

        if not excluded_paths:
            return True

        path = path.rstrip('/')
        excluded_paths = [p.rstrip('/') for p in excluded_paths]

        for excluded_path in excluded_paths:
            if excluded_path.endswith('*'):
                if path.startswith(excluded_path[:-1]):
                    return False
            elif path == excluded_path:
                return False

        # return path not in excluded_paths
        return True

    def authorization_header(self, request=None) -> str:
        """
        returns the authorization header in a request
        """
        if request is None:
            return None
        try:
            return request.headers.get('Authorization')
        except Exception as e:
            return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        returns the current user
        """
        return None
