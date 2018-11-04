#!/usr/bin/env python
# -*- coding: utf-8 -*-


def create_order(dbh, request_id, params: dict):
    """
    Create a new order from params
    :param dbh: database_handle
    :param request_id: int
    :param params: dict
    :return: json
    """
    # Fetch params
    id_meal = 0
    if 'id_meal' in params:
        id_meal = params["id_meal"]
    id_restaurant = 0
    if 'id_restaurant' in params:
        id_restaurant = params["id_restaurant"]
    id_code = 0
    if 'id_code' in params:
        id_code = params["id_code"]
    client_name = ''
    if 'client_name' in params:
        client_name = params["client_name"]
    client_address = ''
    if 'client_address' in params:
        client_address = params["client_address"]
    status = 'Pending'

    with dbh.cursor() as cursor:
        # Create
        sql = "INSERT INTO order (id_meal, id_restaurant, id_code, client_name, client_address, status) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(sql, (
            id_meal,
            id_restaurant,
            id_code,
            client_name,
            client_address,
            status
        ))
        id_order = dbh.insert_id()
    return {
        'action': 'ORDER_CREATED',
        'message': {
            'status': 'OK',
            'request': int(request_id),
            'order': {
                'id_order': id_order,
                'id_meal': id_meal,
                'id_restaurant': id_restaurant,
                'id_code': id_code,
                'client_name': client_name,
                'client_address': client_address,
                'status': status
            }
        }
    }
