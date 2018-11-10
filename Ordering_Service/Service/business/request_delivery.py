#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime

def request_delivery(dbh, request_id, params: dict):
    """
    Update an order as Accepted
    :param dbh: database_handle
    :param request_id: int
    :param params: dict
    :return: json
    """
    # Fetch params
    id_order = 0
    if 'id_order' in params:
        id_order = int(params["id_order"])

    with dbh.cursor() as cursor:
        if id_order > 0:
            sql = "SELECT id_meal, id_restaurant, client_address  FROM `order` WHERE id_order = %s"
            cursor.execute(sql, id_order)
            order = cursor.fetchone()

    if id_order > 0:
        return {
            'action': 'DELIVERY_REQUEST',
            'message': {
                'meal_name': order['id_meal'],
                'request': request_id,
                'pickup_restaurant': order['id_restaurant'],
                'pickup_date': str(datetime.datetime.now() + datetime.timedelta(minutes=20)),
                'delivery_address': order['client_address']
            }
        }
