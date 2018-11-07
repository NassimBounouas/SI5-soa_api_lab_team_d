#!/usr/bin/env python
# -*- coding: utf-8 -*-
from share.load_config import load_config


def before_all(context):
    behave_config = load_config()
    endpoint = behave_config['api_gateway_endpoint']
    context.endpoint = endpoint
