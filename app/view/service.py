#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author: Jialiang Shi
from typing import Optional
from flask_sugar import Blueprint
from flask import current_app as app
from flask_jwt_extended import jwt_required
from app.aliyun.k8s import K8sClient
from app.serializer.service import CreateService, DeleteService
from app.utils.decorator import jwt_permission_required


service_bp = Blueprint('service', __name__, url_prefix='/service', tags=['Service'])


@service_bp.get("/list")
def retrieve_services(cluster_id: str, namespace: Optional[str] = None,
                      name: Optional[str] = None, tag: Optional[str] = None):
    client = K8sClient(
        app.config.get("ALIYUN_ACCESS_KEY"),
        app.config.get("ALIYUN_ACCESS_SECRET"),
        cluster_id
    )

    if name:
        field_selector = "metadata.name={}".format(name)
    else:
        field_selector = None

    if tag:
        label_selector = "app={}".format(tag)
    else:
        label_selector = None

    services = client.list_service(namespace, label_selector=label_selector, field_selector=field_selector)

    return services


@service_bp.post("/create", status_code=201, security=[{'jwt_token': []}])
@jwt_required()
@jwt_permission_required("MODERATE")
def create_service(payload: CreateService):
    cluster_id = payload.cluster_id
    namespace = payload.namespace
    content = payload.content

    client = K8sClient(
        app.config.get("ALIYUN_ACCESS_KEY"),
        app.config.get("ALIYUN_ACCESS_SECRET"),
        cluster_id
    )

    result = client.create_service(namespace, content=content)
    return result


@service_bp.post("/delete", status_code=201, security=[{'jwt_token': []}])
@jwt_required()
@jwt_permission_required("MODERATE")
def delete_service(payload: DeleteService):
    cluster_id = payload.cluster_id
    namespace = payload.namespace
    name = payload.name

    client = K8sClient(
        app.config.get("ALIYUN_ACCESS_KEY"),
        app.config.get("ALIYUN_ACCESS_SECRET"),
        cluster_id
    )

    result = client.delete_service(namespace, name)
    return result
