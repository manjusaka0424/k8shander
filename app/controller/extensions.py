#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author: Jialiang Shi
from flask_sqlalchemy import SQLAlchemy
from flask_debugtoolbar import DebugToolbarExtension
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
toolbar = DebugToolbarExtension()
jwt = JWTManager()
