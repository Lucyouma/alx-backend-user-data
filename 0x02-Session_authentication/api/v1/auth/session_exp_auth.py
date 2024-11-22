#!/usr/bin/env python3
"""
module for session expiration
"""
from api.v1.auth.session_auth import SessionAuth
import os
from models.user import User
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """
    session expiration class
    """
    def __init__(self):
        """
        class initialization
        assign session duration attr based on env variable
        SSESSION DURATION, defaults to zero
        """
        try:
            self.session_duration = int(os.getenv("SESSION_DURATION", 0))

        except ValueError:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """
        creates session id; calls a super function
        """
        session_id = super().create_session(user_id)

        if session_id is None:
            return None

        session_dictionary = {
                "user_id": user_id,
                "created_at": datetime.now()
        }

        self.user_id_by_session_id[session_id] = session_dictionary
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        retrieves user id from session
        """
        if session_id is None:
            return None

        if session_id not in self.user_id_by_session_id.keys():
            return None

        session_dictionary = self.user_id_by_session_id.get(session_id)

        if session_dictionary is None:
            return None

        if self.session_duration <= 0:
            return session_dictionary.get('user_id')

        created_at = session_dictionary.get('created_at')

        if created_at is None:
            return None

        expired_time = created_at + timedelta(seconds=self.session_duration)

        if expired_time < datetime.now():
            return None

        return session_dictionary.get('user_id')
