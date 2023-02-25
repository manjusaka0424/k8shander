#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author: Jialiang Shi
import hashlib
from datetime import datetime
from flask import current_app as app
from werkzeug.local import LocalProxy
from flask_security import UserMixin
from flask_security.utils import verify_password, hash_password
from app.controller.extensions import db
from app.models.rights import Role

_datastore = LocalProxy(lambda: app.extensions['security'].datastore)


class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, comment='邮箱')
    password = db.Column(db.String(256), comment='密码')
    active = db.Column(db.Boolean, default=True, comment='是否激活')
    first_name = db.Column(db.String(64), comment='名')
    last_name = db.Column(db.String(64), comment='姓')

    username = db.Column(db.String(64), unique=True, comment='用户名')
    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False)

    confirmed_at = db.Column(db.DateTime(), comment='确认时间')

    last_login_at = db.Column(db.DateTime())
    current_login_at = db.Column(db.DateTime())
    last_login_ip = db.Column(db.String(128))
    current_login_ip = db.Column(db.String(128))
    login_count = db.Column(db.Integer)

    avatar_hash = db.Column(db.String(32))

    locked = db.Column(db.Boolean, default=False, comment='是否锁定')
    create_at = db.Column(db.DateTime(), default=datetime.now, comment='创建时间')

    roles = db.relationship('Role', secondary='roles_users')

    def __repr__(self):
        return '<User %r>' % self.email

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        self.set_role()
        self.generate_avatar()

    def set_role(self):
        if len(self.roles) == 0:
            if User.query.first() is None:
                self.roles.append(Role.query.filter_by(name='Administrator').first())
            else:
                self.roles.append(Role.query.filter_by(name='User').first())
            db.session.commit()

    def generate_avatar(self):
        if self.email is not None and self.avatar_hash is None:
            self.avatar_hash = self.gravatar_hash()
            db.session.commit()

    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "active": self.active,
            "locked": self.locked,
        }

    def gravatar_hash(self):
        return hashlib.md5(self.email.lower().encode('utf-8')).hexdigest()

    def gravatar(self, size=100, default='identicon', rating='g'):
        url = 'https://secure.gravatar.com/avatar'
        hash = self.avatar_hash or self.gravatar_hash()
        return '{url}/{hash}?s={size}&d={default}&r={rating}'.format(
            url=url,
            hash=hash,
            size=size,
            default=default,
            rating=rating
        )

    def validate_password(self, password):
        return verify_password(password, self.password)

    def set_password(self, password):
        self.password = hash_password(password)

    @staticmethod
    def authenticate(username, password):
        user = User.query.filter_by(username=username).first()
        if not user:
            return None

        # Do the passwords match
        if not verify_password(password, user.password):
            return None

        return user

    def lock(self):
        self.locked = True
        locked_role = Role.query.filter_by(name='Locked').first()
        self.roles = [locked_role]
        db.session.commit()

    def unlock(self):
        self.locked = False
        user_role = Role.query.filter_by(name='User').first()
        self.roles = [user_role]
        db.session.commit()

    @property
    def is_admin(self):
        return self.has_role('Administrator')

    def has_roles(self):
        roles = [item.name for item in self.roles]
        return roles

    def has_permissions(self):
        permissions = []
        for role in self.roles:
            permissions.extend(role.permissions)

        return [item.name for item in list(set(permissions))]

    def can(self, perm):
        return perm in self.has_permissions()


class TokenBlockList(db.Model):
    __tablename__ = "tokenblocklist"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    user = db.relationship("User", lazy="joined")

    jti = db.Column(db.String(36), nullable=False, unique=True)
    token_type = db.Column(db.String(10), nullable=False)
    revoked = db.Column(db.Boolean, nullable=False)
    expires = db.Column(db.DateTime, nullable=False)

    def to_dict(self):
        result = {
            "id": self.id,
            "jti": self.jti,
            "token_type": self.token_type,
            "revoked": self.revoked
        }

        if self.user:
            result.update({"identity": self.user.username})

        return result
