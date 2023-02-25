#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author: Jialiang Shi
import os
import re
import logging
from datetime import datetime, timedelta
from flask import Flask, current_app as app
from flask_sqlalchemy import get_debug_queries
from flask_jwt_extended import (
    get_jwt,
    create_access_token,
    get_jwt_identity,
    set_access_cookies
)
from werkzeug.exceptions import (
    BadRequest,
    NotFound,
    Forbidden,
    Unauthorized,
    Conflict
)
from flask_sugar import Sugar as FlaskAPI
from flask_migrate import Migrate
from app.utils.common import get_abs_dir
from app.config import config
from app.view import init_blueprint
from app.controller.admin import admin
from app.controller.security import create_security
from app.utils.helpers import add_token_to_database
from app.controller.commands import (
    initdb,
    create_superuser,
    clean
)
from app.controller.extensions import (
    toolbar,
    db,
    jwt,
)
from app.controller.jwt import (
    check_if_token_revoked,
    user_loader_callback,
    my_revoked_token_callback,
    my_invalid_token_callback,
    my_expired_token_callback,
    my_unauthorized_token_callback
)

apps_abs_dir = get_abs_dir(__file__)


def refresh_expiring_jwts(response):
    """ Refresh tokens that are within 30 minute(s) of expiring """
    try:
        exp_timestamp = get_jwt()["exp"]
        now = datetime.now()
        target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
        if target_timestamp > exp_timestamp:
            access_token = create_access_token(identity=get_jwt_identity())
            add_token_to_database(access_token, app.config['JWT_IDENTITY_CLAIM'])
            set_access_cookies(response, access_token)
        return response
    except (RuntimeError, KeyError):
        # Case where there is not a valid JWT. Just return the original response
        return response


def query_profiler(response):
    for q in get_debug_queries():
        if q.duration >= app.config['SLOW_QUERY_THRESHOLD']:
            app.logger.warning(
                'Slow query: Duration: %fs\n Context: %s\nQuery: %s\n '
                % (q.duration, q.context, q.statement)
            )
    return response


def register_extensions(app):
    """Register Flask extensions."""
    extensions = [db, jwt]
    if app.config['DEBUG']:
        extensions.append(admin)
        extensions.append(toolbar)

    for extension in extensions:
        extension.init_app(app)


def register_commands(app):
    """Register Click commands."""
    commands = [initdb, create_superuser, clean]
    for command in commands:
        app.cli.add_command(command)


def init_jwt():
    jwt.token_in_blocklist_loader(check_if_token_revoked)
    jwt.user_lookup_loader(user_loader_callback)
    jwt.revoked_token_loader(my_revoked_token_callback)
    jwt.invalid_token_loader(my_invalid_token_callback)
    jwt.expired_token_loader(my_expired_token_callback)
    jwt.unauthorized_loader(my_unauthorized_token_callback)


def register_error_handlers(_app):
    @_app.errorhandler(BadRequest)
    def bad_request(e: BadRequest):
        return {"message": getattr(e, "description")}, 400

    @_app.errorhandler(Forbidden)
    def forbidden(e: Forbidden):
        return {"message": getattr(e, "description")}, 403

    @_app.errorhandler(Unauthorized)
    def unauthorized_access(e: Unauthorized):
        return {"message": getattr(e, "description")}, 401

    @_app.errorhandler(NotFound)
    def not_found(e: NotFound):
        return {"message": getattr(e, "description")}, 404

    @_app.errorhandler(Conflict)
    def conflict(e: Conflict):
        return {"message": getattr(e, "description")}, 409


tags_metadata = [
    {
        "name": "Auth",
        "description": "Manage user Authentication and Authorization.",
    },
]


def create_app(env=None):
    app_ = FlaskAPI(
        __name__,
        title="Aliyun Kubernetes APIs",
        openapi_json_url="/apis/openapi.json",
        swagger_url="/apis/swagger",
        redoc_url="/apis/redoc",
        rapidoc_url="/apis/rapidoc",
        doc_version="0.0.1",
        tags=tags_metadata,
        doc_route_filter=lambda view, rule: re.match("^(/pod|/ingress|/service|/namespace|/deployment|/auth/)", rule.rule) is not None,
        security_schemes={'jwt_token': {'type': 'apiKey', 'in': 'header', 'name': 'Authorization'}}
    )
    if env is None:
        env = os.environ.get('FLASK_ENV', 'default')
    app_.config.from_object(config.get(env))

    register_extensions(app_)
    register_commands(app_)

    if app_.config['SQLALCHEMY_DATABASE_URI'].startswith("sqlite:"):
        Migrate(app_, db, render_as_batch=True)
    else:
        Migrate(app_, db)

    init_blueprint(app_)
    register_error_handlers(app_)
    security = create_security(app_)

    init_jwt()

    app_.after_request(refresh_expiring_jwts)

    if app_.config['DEBUG']:
        app_.after_request(query_profiler)

    gunicorn_logger = logging.getLogger('gunicorn.api')
    app_.logger.handlers = gunicorn_logger.handlers
    app_.logger.setLevel(gunicorn_logger.level)

    return app_


app = create_app()
