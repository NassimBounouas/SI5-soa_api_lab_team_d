#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import json
from urllib import request
from urllib.error import HTTPError


def query_callback(callback_url: str, response_key: str):
    """
    Query the Callback URL and return a partial response by JSON key
    :param callback_url: str
    :param response_key: str
    :return: dict
    """
    if len(callback_url) == 0:
        return {}

    http_code = 404
    while http_code == 404:
        try:
            req = request.Request(callback_url)
            with request.urlopen(req) as response:
                ret = json.loads(response.read())
                if response_key in ret:
                    return ret[response_key]
                else:
                    return {}
        except HTTPError as e:
            http_code = int(e.code)
            time.sleep(0.1)
