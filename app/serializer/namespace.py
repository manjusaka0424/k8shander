#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author: Jialiang Shi
from pydantic import BaseModel


class CreateNamespace(BaseModel):
    cluster_id: str
    name: str


class DeleteNamespace(BaseModel):
    cluster_id: str
    name: str
