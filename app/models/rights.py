#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author: Jialiang Shi
from flask import current_app as app
from werkzeug.local import LocalProxy
from app.controller.extensions import db
from flask_security import RoleMixin

_datastore = LocalProxy(lambda: app.extensions['security'].datastore)


class RolesPermissions(db.Model):
    __tablename__ = 'roles_permissions'

    id = db.Column(db.Integer, primary_key=True)
    role_id = db.Column('role_id', db.Integer, db.ForeignKey('role.id'))
    permission_id = db.Column('permission_id', db.Integer, db.ForeignKey('permission.id'))


class Permission(db.Model):
    __tablename__ = 'permission'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)

    def __repr__(self):
        return '<Permission %r>' % self.name


class RolesUsers(db.Model):
    __tablename__ = 'roles_users'

    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
    role_id = db.Column('role_id', db.Integer, db.ForeignKey('role.id'))


class Role(db.Model, RoleMixin):
    __tablename__ = 'role'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(32), unique=True)
    description = db.Column(db.String(255))

    permissions = db.relationship('Permission', secondary='roles_permissions')

    def __repr__(self):
        return '<Role %r>' % self.name

    def has_permission(self, perm):
        search_permission = Permission.query.filter_by(name=perm).first()
        return search_permission and search_permission in self.permissions

    def add_permission(self, perm):
        search_permission = Permission.query.filter_by(name=perm).first()
        if search_permission and not self.has_permission(perm):
            self.permissions.append(search_permission)
            db.session.commit()

    def remove_permission(self, perm):
        search_permission = Permission.query.filter_by(name=perm).first()
        if search_permission and self.has_permission(perm):
            self.permissions.remove(search_permission)
            db.session.commit()

    def reset_permissions(self):
        self.permissions = []
        db.session.commit()

    @staticmethod
    def init_roles():
        roles_permissions_map = {
            'Locked': [],
            'User': ['USER'],
            'Moderator': ['USER', 'MODERATE'],
            'Administrator': ['USER', 'MODERATE', 'ADMINISTER']
        }

        for role_name in roles_permissions_map:
            role = _datastore.find_or_create_role(name=role_name)
            for permission_name in roles_permissions_map[role_name]:
                permission = Permission.query.filter_by(name=permission_name).first()
                if permission is None:
                    permission = Permission(name=permission_name)
                    db.session.add(permission)
                role.permissions.append(permission)
        db.session.commit()
