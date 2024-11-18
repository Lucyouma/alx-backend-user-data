#!/usr/bin/env python3
"""
module for session storage in database
"""
from models.base import Base


class UserSession(Base):
    """
    User session class storage for storing
    user sessions in database
    """
    def __init__(self, *args: list, **kwargs: dict):
        """"
        constructor
        """
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')
