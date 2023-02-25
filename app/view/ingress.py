#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author: Jialiang Shi
from typing import Optional
from flask_sugar import Blueprint
from flask import current_app as app
from flask_jwt_extended import jwt_required
from app.aliyun.k8s import K8sClient
from app.serializer.ingress import CreateIngress, DeleteIngress
from app.utils.decorator import jwt_permission_required


ingress_bp = Blueprint('ingress', __name__, url_prefix='/ingress', tags=['Ingress'])


@ingress_bp.get("/list")
def retrieve_ingresses(cluster_id: str, namespace: Optional[str] = None, name: Optional[str] = None):
    client = K8sClient(
        app.config.get("ALIYUN_ACCESS_KEY"),
        app.config.get("ALIYUN_ACCESS_SECRET"),
        cluster_id
    )

    if name:
        field_selector = "metadata.name={}".format(name)
    else:
        field_selector = None

    services = client.list_ingress(namespace, field_selector=field_selector)

    return services


@ingress_bp.post("/create", status_code=201, security=[{'jwt_token': []}])
@jwt_required()
@jwt_permission_required("MODERATE")
def create_ingresses(payload: CreateIngress):
    cluster_id = payload.cluster_id
    namespace = payload.namespace
    content = payload.content

    client = K8sClient(
        app.config.get("ALIYUN_ACCESS_KEY"),
        app.config.get("ALIYUN_ACCESS_SECRET"),
        cluster_id
    )

    result = client.create_ingress(namespace, content=content)
    return result


@ingress_bp.delete("/delete", status_code=201, security=[{'jwt_token': []}])
@jwt_required()
@jwt_permission_required("MODERATE")
def delete_ingresses(payload: DeleteIngress):
    cluster_id = payload.cluster_id
    namespace = payload.namespace
    name = payload.name

    client = K8sClient(
        app.config.get("ALIYUN_ACCESS_KEY"),
        app.config.get("ALIYUN_ACCESS_SECRET"),
        cluster_id
    )

    result = client.delete_ingress(namespace, name)
    return result
