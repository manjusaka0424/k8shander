#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author: Jialiang Shi
from pydantic import BaseModel


class ObtainToken(BaseModel):
    username: str
    password: str
