#!/usr/bin/env python3
"""
module for basic authentication
"""


from api.v1.auth.auth import Auth
import base64
from typing import TypeVar
from models.user import User


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

    def decode_base64_authorization_header(self,
                                           base64_authorization_header: str
                                           ) -> str:
        """
        method to decode value of base64 string
        base64_authorization_header
        """
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            encoded_bytes = base64_authorization_header.encode('utf-8')
            converted = base64.b64decode(encoded_bytes)
            decoded = converted.decode('utf-8')

        except BaseException as e:
            return None

        return decoded

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header: str
                                 ) -> (str, str):
        """
        extracts user email and password from
        base64encoded
        """
        if decoded_base64_authorization_header is None:
            return None, None
        if not isinstance(decoded_base64_authorization_header, str):
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None
        creds = decoded_base64_authorization_header.split(':', 1)
        return creds[0], creds[1]

    def user_object_from_credentials(self,
                                     user_email: str, user_pwd: str
                                     ) -> TypeVar('User'):
        """
        returns instance for user given email and password
        """
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None
        try:
            exist_user = User.search({'email': user_email})

        except Exception as e:
            return None

        for user in exist_user:
            if user.is_valid_password(user_pwd):
                return user
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        retrieves a user instance for a request made withbais auth
        """
        encoded = self.authorization_header(request)
        user = self.extract_base64_authorization_header(encoded)
        decoded = self.decode_base64_authorization_header(user)
        email, pwd = self.extract_user_credentials(decoded)
        user = self.user_object_from_credentials(email, pwd)
        return user
