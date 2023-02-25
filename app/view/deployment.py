#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author: Jialiang Shi
from typing import Optional
from flask_sugar import Blueprint
from flask import current_app as app
from flask_jwt_extended import jwt_required
from app.aliyun.k8s import K8sClient
from app.serializer.deployment import CreateDeployment, DeleteDeployment
from app.utils.decorator import jwt_permission_required


deployment_bp = Blueprint('deployment', __name__, url_prefix='/deployment', tags=['Deployment'])


@deployment_bp.get("/list")
def retrieve_deployments(cluster_id: str, namespace: Optional[str] = None,
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

    deployment = client.list_deployment(namespace, label_selector, field_selector)

    return deployment


@deployment_bp.post("/create", status_code=201, security=[{'jwt_token': []}])
@jwt_required()
@jwt_permission_required("MODERATE")
def create_deployment(payload: CreateDeployment):
    cluster_id = payload.cluster_id
    namespace = payload.namespace
    content = payload.content

    client = K8sClient(
        app.config.get("ALIYUN_ACCESS_KEY"),
        app.config.get("ALIYUN_ACCESS_SECRET"),
        cluster_id
    )

    result = client.create_deployment(namespace, content=content)
    return result


@deployment_bp.post("/delete", status_code=201, security=[{'jwt_token': []}])
@jwt_required()
@jwt_permission_required("MODERATE")
def delete_deployment(payload: DeleteDeployment):
    cluster_id = payload.cluster_id
    namespace = payload.namespace
    name = payload.name

    client = K8sClient(
        app.config.get("ALIYUN_ACCESS_KEY"),
        app.config.get("ALIYUN_ACCESS_SECRET"),
        cluster_id
    )

    result = client.delete_deployment(namespace, name)
    return result
