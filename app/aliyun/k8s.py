#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author: Jialiang Shi
import os
import yaml
from pathlib import Path
from kubernetes import client, config
from app.aliyun.ack import AliyunAckClient


class K8sClient:
    def __init__(self, access_key_id: str,
                 access_key_secret: str,
                 cluster_id: str,
                 cluster_name: str = None):
        """

        """
        ack_client = AliyunAckClient(access_key_id, access_key_secret)

        if not cluster_name:
            cluster_detail = ack_client.describe_cluster_detail(cluster_id)
            cluster_name = cluster_detail.get("name")

        f_name = str(Path.home()) + '/.kube/{}'.format(cluster_name)
        if not os.path.exists(f_name):
            user_config = ack_client.get_user_config(cluster_id)

            with open(f_name, 'w+') as f:
                f.write(user_config.get("config"))

        config.load_kube_config(f_name)

    @staticmethod
    def list_namespace(field_selector: str = None):
        """查询命名空间"""
        v1 = client.CoreV1Api()
        resp = v1.list_namespace(field_selector=field_selector)
        return resp.to_dict()

    @staticmethod
    def create_namespace(name: str):
        """创建命名空间"""
        v1 = client.CoreV1Api()
        # body = {
        #     "apiVersion": "v1",
        #     "kind": "Namespace",
        #     "metadata": {
        #         "name": name,
        #     }
        # }

        body = client.V1Namespace()
        body.metadata = client.V1ObjectMeta(name=name)

        resp = v1.create_namespace(body=body)
        return resp.to_dict()

    @staticmethod
    def delete_namespace(name: str):
        """删除命名空间"""
        v1 = client.CoreV1Api()

        body = client.V1DeleteOptions()
        resp = v1.delete_namespace(name, body=body)

        return resp.to_dict()

    @staticmethod
    def list_deployment(namespace: str = None, label_selector: str = None, field_selector: str = None):
        """查询部署"""
        v1 = client.AppsV1Api()

        if not namespace:
            resp = v1.list_deployment_for_all_namespaces(
                label_selector=label_selector,
                field_selector=field_selector
            )
        else:
            resp = v1.list_namespaced_deployment(
                namespace=namespace,
                label_selector=label_selector,
                field_selector=field_selector
            )

        return resp.to_dict()

    @staticmethod
    def create_deployment(namespace: str, content: str):
        """创建部署"""
        v1 = client.AppsV1Api()

        body = yaml.safe_load(content)
        resp = v1.create_namespaced_deployment(namespace=namespace, body=body)

        return resp.to_dict()

    @staticmethod
    def delete_deployment(namespace: str, name: str):
        """删除部署"""
        v1 = client.AppsV1Api()

        body = client.V1DeleteOptions()
        resp = v1.delete_namespaced_deployment(name, namespace, body=body)

        return resp.to_dict()

    @staticmethod
    def list_service(namespace: str = None, label_selector: str = None, field_selector: str = None):
        """查询服务"""
        v1 = client.CoreV1Api()

        if not namespace:
            resp = v1.list_service_for_all_namespaces(
                label_selector=label_selector,
                field_selector=field_selector
            )

        else:
            resp = v1.list_namespaced_service(
                namespace,
                label_selector=label_selector,
                field_selector=field_selector
            )

        return resp.to_dict()

    @staticmethod
    def create_service(namespace: str, content: str):
        """创建服务"""
        v1 = client.CoreV1Api()

        body = yaml.safe_load(content)
        resp = v1.create_namespaced_service(namespace=namespace, body=body)

        return resp.to_dict()

    @staticmethod
    def delete_service(namespace: str, name: str):
        """删除服务"""
        v1 = client.CoreV1Api()

        body = client.V1DeleteOptions()
        resp = v1.delete_namespaced_service(name, namespace, body=body)

        return resp.to_dict()

    @staticmethod
    def list_ingress(namespace: str = None, field_selector: str = None):
        """查询ingress"""
        v1 = client.ExtensionsV1beta1Api()

        if not namespace:
            resp = v1.list_ingress_for_all_namespaces(field_selector=field_selector)
        else:
            resp = v1.list_namespaced_ingress(namespace, field_selector=field_selector)

        return resp.to_dict()

    @staticmethod
    def create_ingress(namespace: str, content: str):
        """创建ingress"""
        v1 = client.ExtensionsV1beta1Api()

        body = yaml.safe_load(content)
        resp = v1.create_namespaced_ingress(namespace=namespace, body=body)

        return resp.to_dict()

    @staticmethod
    def delete_ingress(namespace: str, name: str):
        """删除ingress"""
        v1 = client.ExtensionsV1beta1Api()

        body = client.V1DeleteOptions()
        resp = v1.delete_namespaced_ingress(name=name, namespace=namespace, body=body)

        return resp.to_dict()

    @staticmethod
    def list_pod(namespace: str = None, label_selector: str = None, field_selector: str = None):
        """查询pod"""
        v1 = client.CoreV1Api()

        if not namespace:
            resp = v1.list_pod_for_all_namespaces(
                label_selector=label_selector,
                field_selector=field_selector
            )
        else:
            resp = v1.list_namespaced_pod(
                namespace,
                label_selector=label_selector,
                field_selector=field_selector
            )

        return resp.to_dict()

    @staticmethod
    def delete_pod(namespace: str, name: str):
        """删除pod"""
        v1 = client.CoreV1Api()

        body = client.V1DeleteOptions()
        resp = v1.delete_namespaced_pod(name=name, namespace=namespace, body=body)

        return resp.to_dict()

    @staticmethod
    def get_pod_console(namespace: str, name: str, container: str = None):
        """获取pod(容器)日志"""
        v1 = client.CoreV1Api()
        resp = v1.read_namespaced_pod_log(name=name, namespace=namespace, container=container)
        return resp

