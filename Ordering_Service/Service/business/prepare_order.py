#!/usr/bin/env python
# -*- coding: utf-8 -*-


def prepare_order(dbh, request_id, params: dict):
    """
    Notify restaurant service to start preparing the order
    :param dbh: database_handle
    :param request_id: int
    :param params: dict
    :return: json
    """
    # Fetch params
    id_order = 0
    if 'id_order' in params:
        id_order = params["id_order"]
    id_meal = 0
    if 'id_meal' in params:
        id_meal = params["id_meal"]
    id_restaurant = 0
    if 'id_restaurant' in params:
        id_restaurant = params["id_restaurant"]

    return {
        'action': 'PREPARE_ORDER',
        'message': {
            'status': 'OK',
            'request': int(request_id),
            'order': {
                'id_order': id_order,
                'id_meal': id_meal,
                'id_restaurant': id_restaurant
            }
        }
    }