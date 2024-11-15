from flask import request
from typing import List, TypeVar
"""
module template for
authentication class
"""


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
        """
        return False

    def authorization_header(self, request=None) -> str:
        """
        returns the authorization header in a request
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        returns the current user
        """
        return None
