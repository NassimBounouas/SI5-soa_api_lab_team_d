#!/usr/bin/env python
# -*- coding: utf-8 -*-


def get_order_list(dbh, request_id, params: dict):
    """
    Return a list of Order in preparation
    :param dbh: database_handle
    :param request_id: int
    :param params: dict
    :return: json
    """
    id_restaurant_requested = int(params["id_restaurant"])
    with dbh.cursor() as cursor:
        # Get list
        sql = "SELECT id_meal,id_order FROM `order` WHERE status = 'Accepted'  AND id_restaurant = %s"
        cursor.execute(sql,(
                        id_restaurant_requested
                        )
                       )
        list = cursor.fetchall()
    return {
        'action': 'ORDER_LIST_RESPONSE',
        'message': {
            'status': 'OK',
            'request': int(request_id),
            'List': list
            }
        }