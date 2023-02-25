#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author: Jialiang Shi
from pydantic import BaseModel


class CreateService(BaseModel):
    cluster_id: str
    namespace: str
    content: str


class DeleteService(BaseModel):
    cluster_id: str
    namespace: str
    name: str
