#!/usr/bin/env python
# -*- coding: utf-8 -*-


def validate_order(dbh, request_id, params: dict):
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
        id_order = int(params["id_meal"])

    with dbh.cursor() as cursor:
        if id_order > 0:
            # Accepted
            sql = "UPDATE order SET status = %s  WHERE id_order=%s"
            cursor.execute(sql, (
                'Accepted',
                id_order
            ))
    if id_order > 0:
        return {
            'action': 'ORDER_ACCEPTED',
            'message': {
                'status': 'OK',
                'request': int(request_id),
                'order': {
                    'id_order': id_order,
                    'status': 'Accepted'
                }
            }
        }
    return {
        'action': 'ORDER_ACCEPTED',
        'message': {
            'status': 'KO',
            'request': int(request_id),
        }
    }
