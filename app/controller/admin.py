#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author: Jialiang Shi
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from app.controller.extensions import db

ignore_tables = ['roles_permissions', 'roles_users']


def get_models(_db):
    """Get all the models in the db, all models should have a explicit __tablename__"""
    classes, models, table_names = [], [], []

    if hasattr(_db.Model, "_decl_class_registry"):
        _models = _db.Model._decl_class_registry.values()  # sqlalchemy<1.4
    else:
        _models = _db.Model.registry._class_registry.values()  # sqlalchemy>=1.4

    for class_ in _models:
        if hasattr(class_, "__tablename__"):
            if class_.__tablename__ not in ignore_tables:
                table_names.append(class_.__tablename__)
                classes.append(class_)

    tables = _db.metadata.tables.items()
    for table in tables:
        if table[0] in table_names:
            models.append(classes[table_names.index(table[0])])

    return models


admin = Admin(name='Admin', template_mode='bootstrap4')
for model in get_models(db):
    admin.add_view(ModelView(model, db.session))
