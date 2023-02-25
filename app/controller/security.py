#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author: Jialiang Shi
from flask_security import Security, AnonymousUser
from flask_security.datastore import SQLAlchemyUserDatastore
from app.controller.extensions import db
from app.models.users import User
from app.models.rights import Role


class Guest(AnonymousUser):
    def can(self, permission_name):
        return False

    @property
    def is_admin(self):
        return False


def create_security(app):
    """Setup Flask-Security"""
    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    security = Security(app,
                        user_datastore,
                        anonymous_user=Guest)

    return security
