#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author: Jialiang Shi
from app.view.auth import auth_bp
from app.view.pod import pod_bp
from app.view.service import service_bp
from app.view.ingress import ingress_bp
from app.view.namespace import namespace_bp
from app.view.deployment import deployment_bp


bps = [pod_bp, ingress_bp, service_bp, namespace_bp, deployment_bp, auth_bp]


def init_blueprint(app):
    for bp in bps:
        app.register_blueprint(bp)
