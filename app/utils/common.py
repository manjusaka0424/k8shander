#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author: Jialiang Shi
import os
import json
import uuid
import flask
import requests
from werkzeug.local import LocalProxy
from flask import current_app as app


_datastore = LocalProxy(lambda: app.extensions['security'].datastore)


def get_abs_dir(_file_):
    return os.path.abspath(os.path.dirname(_file_))


def strip_trailing_slash(url):
    while url.endswith('/'):
        url = url[:-1]
    return url


def is_chinese(word):
    for ch in word:
        if '\u4e00' <= ch <= '\u9fff':
            return True

    return False


def parser_dict(data: dict = None):
    """
    {"a": 1, "b": 2, "c": 3} => 'a=1,b=2,c=3'
    """
    if not data:
        return

    items = []
    for key, value in data.items():
        item = "{}={}".format(key, value)
        items.append(item)
    return ",".join(items)
