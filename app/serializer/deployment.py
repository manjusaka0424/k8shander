#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author: Jialiang Shi
from pydantic import BaseModel


class CreateDeployment(BaseModel):
    cluster_id: str
    namespace: str
    content: str


class DeleteDeployment(BaseModel):
    cluster_id: str
    namespace: str
    name: str
