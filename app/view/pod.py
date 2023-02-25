#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author: Jialiang Shi
from typing import Optional
from flask_sugar import Blueprint
from flask import current_app as app
from app.aliyun.k8s import K8sClient


pod_bp = Blueprint('pod', __name__, url_prefix='/pod', tags=['Pod'])


@pod_bp.get("/list")
def retrieve_pods(cluster_id: str, namespace: Optional[str] = None,
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

    pod = client.list_pod(namespace, label_selector=label_selector, field_selector=field_selector)

    return pod


@pod_bp.get("/console")
def retrieve_pod_console(cluster_id: str, namespace: str, name: str, container: str = None):
    client = K8sClient(
        app.config.get("ALIYUN_ACCESS_KEY"),
        app.config.get("ALIYUN_ACCESS_SECRET"),
        cluster_id
    )

    console = client.get_pod_console(namespace, name, container)
    return {"data": console}
