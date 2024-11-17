#!/usr/bin/env python3
"""
module for session authentication
"""
from api.v1.auth.auth import Auth
import uuid
from models.user import User


class SessionAuth(Auth):
    """
    Session authentication class
    inherits from Auth
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        creates a session id for a user id
        """
        if user_id is None or not isinstance(user_id, str):
            return None

        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        returns user id based on session id
        """
        if session_id is None or not isinstance(session_id, str):
            return None
        user_id = self.user_id_by_session_id.get(session_id)
        return user_id

    def current_user(self, request=None) -> str:
        """
        returns user based on cookie value
        """
        cookie_id = self.session_cookie(request)

        if cookie_id is None:
            return None

        user_id = self.user_id_for_session_id(cookie_id)
        return User.get(user_id)

    def destroy_session(self, request=None) -> bool:
        """
        logs out user by deleting session
        """
        if request is None:
            return False

        session_id = self.session_cookie(request)

        if session_id is None:
            return False

        if self.user_id_for_session_id(session_id) is None:
            return False

        try:
            del self.user_id_by_session_id[session_id]
        except Exception as e:
            return False

        return True
