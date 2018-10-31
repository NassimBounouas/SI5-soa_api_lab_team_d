#!/usr/bin/env python
# -*- coding: utf-8 -*-


def make_kafka_message(action='', message=None):
    """
    Make a new KAFKA message for Uberoo
    """
    import uuid

    if message is None:
        message = {}

    message['request'] = uuid.uuid4().int

    return {
        "action": action.upper(),
        "message": message
    }, message['request']
