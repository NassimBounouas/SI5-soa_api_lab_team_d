#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
from urllib import parse, request


def fetch_callback(endpoint: str, url: str):
    """
    Resolve the Callback URL for an API Gateway Query
    :param endpoint: str
    :param url: str
    :return: str
    """
    if len(endpoint) == 0:
        return ''

    with request.urlopen(
        request.Request(
            endpoint + url
        ),
        data=parse.urlencode({}).encode()
    ) as response:
        return json.loads(response.read())['callbackUrl']
