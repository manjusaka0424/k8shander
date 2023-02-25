#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author: Jialiang Shi
from pydantic import BaseModel


class DBModel(BaseModel):
    class Config:
        orm_mode = True

    @classmethod
    def serialize(cls, obj):
        return cls.from_orm(obj).dict()
