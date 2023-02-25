#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author: Jialiang Shi
from functools import wraps
from werkzeug.exceptions import Forbidden
from flask import current_app as app, jsonify
from werkzeug.local import LocalProxy
from flask_jwt_extended import (
    get_jwt_identity,
    current_user as jwt_current_user
)
from app.models.users import User

_security = LocalProxy(lambda: app.extensions['security'])


def jwt_permission_required(permission):
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            current_permissions = jwt_current_user.permissions
            if permission not in current_permissions:
                raise Forbidden("Forbidden")
            return fn(*args, **kwargs)
        return decorated_view
    return wrapper


def jwt_admin_required(fn):
    @wraps(fn)
    def decorated_view(*args, **kwargs):
        identity = get_jwt_identity()
        user = User.query.filter_by(username=identity).first()
        if not user.is_admin:
            raise Forbidden("Forbidden")
        return fn(*args, **kwargs)
    return decorated_view
