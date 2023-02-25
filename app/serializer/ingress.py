#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author: Jialiang Shi
from pydantic import BaseModel


class CreateIngress(BaseModel):
    cluster_id: str
    namespace: str
    content: str


class DeleteIngress(BaseModel):
    cluster_id: str
    namespace: str
    name: str
