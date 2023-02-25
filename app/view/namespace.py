#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author: Jialiang Shi
from typing import Optional
from flask_sugar import Blueprint
from flask import current_app as app
from flask_jwt_extended import jwt_required
from app.aliyun.k8s import K8sClient
from app.serializer.namespace import CreateNamespace, DeleteNamespace
from app.utils.decorator import jwt_permission_required


namespace_bp = Blueprint('namespace', __name__, url_prefix='/namespace', tags=['Namespace'])


@namespace_bp.get("/list")
def retrieve_namespaces(cluster_id: str, name: Optional[str] = None):
    client = K8sClient(
        app.config.get("ALIYUN_ACCESS_KEY"),
        app.config.get("ALIYUN_ACCESS_SECRET"),
        cluster_id
    )

    if name:
        field_selector = "metadata.name={}".format(name)
    else:
        field_selector = None

    namespace = client.list_namespace(field_selector=field_selector)

    return namespace


@namespace_bp.post("/create", status_code=201, security=[{'jwt_token': []}])
@jwt_required()
@jwt_permission_required("MODERATE")
def create_namespace(payload: CreateNamespace):
    cluster_id = payload.cluster_id
    name = payload.name

    client = K8sClient(
        app.config.get("ALIYUN_ACCESS_KEY"),
        app.config.get("ALIYUN_ACCESS_SECRET"),
        cluster_id
    )

    result = client.create_namespace(name)

    return result


@namespace_bp.post("/delete", status_code=201, security=[{'jwt_token': []}])
@jwt_required()
@jwt_permission_required("MODERATE")
def delete_namespace(payload: DeleteNamespace):
    cluster_id = payload.cluster_id
    name = payload.name

    client = K8sClient(
        app.config.get("ALIYUN_ACCESS_KEY"),
        app.config.get("ALIYUN_ACCESS_SECRET"),
        cluster_id
    )

    result = client.delete_namespace(name)

    return result
