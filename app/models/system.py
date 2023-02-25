#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author: Jialiang Shi
from datetime import datetime
from app.controller.extensions import db
from app.models.base import Model as BaseModel


class Request(db.Model):
    __tablename__ = "request"

    id = db.Column(db.Integer, primary_key=True)

    method = db.Column(db.String(8))
    module = db.Column(db.String(64))

    full_path = db.Column(db.String(256))
    ip = db.Column(db.String(64))
    timestamp = db.Column(db.DateTime(), default=datetime.now)
    user_agent = db.Column(db.Text)

    status_code = db.Column(db.Integer)
    arguments = db.Column(db.PickleType, default=dict())

    def __repr__(self):
        return '<Request %r>' % self.id
