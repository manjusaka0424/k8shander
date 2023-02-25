#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author: Jialiang Shi
from flask import jsonify, current_app as app
from app.models.users import User
from app.utils.helpers import is_token_revoked


class UserObject:
    def __init__(self, username, permissions):
        self.username = username
        self.permissions = permissions


# Checks if a token has been blacklisted and will be called automatically when
# JWT_BLACKLIST_ENABLED is true. We add the token's unique identifier (jti) to the blacklist.
def check_if_token_revoked(jwt_header, jwt_payload):
    return is_token_revoked(jwt_payload)


# This function is called whenever a protected endpoint is accessed,
# and must return an object based on the tokens identity.
# This is called after the token is verified, so you can use
# get_jwt_claims() in here if desired. Note that this needs to
# return None if the user could not be loaded for any reason,
# such as not being found in the underlying data store
def user_loader_callback(jwt_header, jwt_data):
    identity_claim = app.config['JWT_IDENTITY_CLAIM']
    identity = jwt_data[identity_claim]
    user = User.query.filter_by(username=identity).first()
    if not user:
        return None

    return UserObject(
        username=identity,
        permissions=user.has_permissions()
    )


def my_revoked_token_callback(jwt_header, jwt_data):
    """Checks if a token has been revoked."""
    message = "The token has been revoked."
    return jsonify({"message": message}), 401


# Using the expired_token_loader decorator, we will now call
# this function whenever an expired but otherwise valid access
# token attempts to access an endpoint
def my_expired_token_callback(jwt_header, jwt_data):
    token_type = jwt_data['type']
    message = "{} token has expired.".format(token_type)
    return jsonify({"message": message}), 401


def my_invalid_token_callback(reason):
    """If invalid token attempts to access a protected route."""
    message = "invalid token. reason: {}".format(reason)
    return jsonify({"message": message}), 401


def my_unauthorized_token_callback(jwt_header):
    message = "unauthorized access"
    return jsonify({"message": message}), 401
