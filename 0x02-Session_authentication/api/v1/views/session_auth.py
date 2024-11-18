#!/usr/bin/env python3
"""
Handles routes for session authentication
"""

import flask
from flask import request, jsonify, abort
from models.user import User
from api.v1.views import app_views
from os import getenv


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login() -> str:
    """
    logs in a user
    """
    email = request.form.get('email')

    if email is None:
        return jsonify({"error": "email missing"}), 400

    password = request.form.get('password')

    if password is None:
        return jsonify({"error": "password missing"}), 400

    try:
        user_object = User.search({'email': email})

    except Exception as e:
        return jsonify({"error": "no user found for this email"}), 404

    if not user_object:
        return jsonify({"error": "no user found for this email"}), 404

    for user in user_object:
        if not user.is_valid_password(password):
            return jsonify({"error": "wrong password"}), 401

    from api.v1.app import auth

    user = user_object[0]
    session_id = auth.create_session(user.id)

    SESSION_NAME = getenv("SESSION_NAME")

    response = jsonify(user.to_json())
    response.set_cookie(SESSION_NAME, session_id)

    return response


@app_views.route('auth_session/logout',
                 methods=['DELETE'], strict_slashes=False)
def logout():
    """
    logs out person by deleting session
    """
    from api.v1.app import auth

    delete = auth.destroy_session(request)

    if not delete:
        abort(404)

    return jsonify({}), 200
