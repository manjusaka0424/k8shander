#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author: Jialiang Shi
import json
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest
from aliyunsdkcore.auth.credentials import AccessKeyCredential


class AliyunAckClient:
    def __init__(self, access_key_id: str, access_key_secret: str, region_id: str = "cn-beijing"):
        self.cs_url = "cs.{}.aliyuncs.com".format(region_id)
        credential = AccessKeyCredential(access_key_id, access_key_secret)
        self.client = AcsClient(region_id=region_id, credential=credential)

    def _do_request(self, endpoint, method):
        request = CommonRequest()
        request.set_accept_format('json')
        request.set_domain(self.cs_url)
        request.set_method(method)
        request.set_protocol_type('https')  # https | http
        request.set_version('2015-12-15')

        request.add_header('Content-Type', 'application/json')
        request.set_uri_pattern(endpoint)

        body = '''{}'''
        request.set_content(body.encode('utf-8'))

        response = self.client.do_action_with_exception(request)
        return json.loads(response)

    def get_user_config(self, cluster: str):
        endpoint = '/k8s/{}/user_config'.format(cluster)
        return self._do_request(endpoint, 'GET')

    def describe_cluster_detail(self, cluster: str):
        endpoint = '/clusters/{}'.format(cluster)
        return self._do_request(endpoint, 'GET')

