#!/usr/bin/env python3
"""
module for basic authentication
"""


from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """
    Basic authentication class
    inherits from Auth class
    """
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """
        Returns Base64 part of Authorization header
        """
        if authorization_header is None:
            return None
        if type(authorization_header) is not str:
            return None
        if not authorization_header.startswith("Basic"):
            return None
        parts = authorization_header.split(' ')

        if len(parts) != 2:
            return None

        return parts[1]
