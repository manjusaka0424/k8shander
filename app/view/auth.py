#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author: Jialiang Shi
from flask_jwt_extended import (
    jwt_required,
    get_jwt,
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
)
from flask import current_app
from flask_sugar import Blueprint
from app.models.users import User
from app.utils.helpers import revoke_token, add_token_to_database
from app.serializer.auth import ObtainToken

auth_bp = Blueprint('auth', __name__, url_prefix='/auth', tags=['Auth'])


@auth_bp.post('/obtain/token', status_code=201)
def obtain_token(payload: ObtainToken):
    """
    curl -X POST http://localhost:5000/apis/auth/obtain/token -d "{\"username\":\"xxx\",\"password\":\"yyy\"}" -H 'Content-Type: application/json'
    """
    username = payload.username
    password = payload.password

    user = User.authenticate(username, password)
    if not user:
        return {"message": "Bad username or password"}, 400

    # Identity can be any data that is json serializable
    access_token = create_access_token(identity=username)
    refresh_token = create_refresh_token(identity=username)

    add_token_to_database(access_token, current_app.config['JWT_IDENTITY_CLAIM'])
    add_token_to_database(refresh_token, current_app.config['JWT_IDENTITY_CLAIM'])

    ret = {
        'access_token': access_token,
        'refresh_token': refresh_token
    }
    return ret


@auth_bp.post('/refresh/access/token', status_code=201, security=[{'jwt_token': []}])
@jwt_required(refresh=True)
def refresh():
    """
    curl -X POST http://localhost:5000/apis/auth/refresh/access/token -H "Authorization: Bearer $refresh_token"
    """
    user_identity = get_jwt_identity()
    access_token = create_access_token(identity=user_identity)
    ret = {
        'access_token': access_token
    }

    add_token_to_database(access_token, current_app.config['JWT_IDENTITY_CLAIM'])

    return ret


@auth_bp.get('/me', security=[{'jwt_token': []}])
@jwt_required()
def about_me():
    """
    curl -X GET http://localhost:5000/apis/auth/me -H "Authorization: Bearer $access_token"
    """
    identity = get_jwt_identity()
    search_user = User.query.filter_by(username=identity).first()
    if search_user is None:
        return {"message": "unknown user"}, 400

    ret = search_user.to_dict()
    return ret


@auth_bp.post('/revoke/access/token', status_code=201, security=[{'jwt_token': []}])
@jwt_required()
def revoke_access_token():
    """
    curl -X POST http://localhost:5000/apis/auth/revoke/access/token -H "Authorization: Bearer $access_token"
    """
    jti = get_jwt()["jti"]
    user_identity = get_jwt_identity()
    revoke_token(jti, user_identity)
    return {"message": "token revoked"}


@auth_bp.post("/revoke/refresh/token", status_code=201, security=[{'jwt_token': []}])
@jwt_required(refresh=True)
def revoke_refresh_token():
    """
    curl -X POST http://localhost:5000/apis/auth/revoke/refresh/token  -H "Authorization: Bearer $refresh_token"
    """
    jti = get_jwt()["jti"]
    user_identity = get_jwt_identity()
    revoke_token(jti, user_identity)
    return {"message": "token revoked"}
