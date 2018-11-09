#!/usr/bin/env python
# -*- coding: utf-8 -*-

def map_delivery(dbh, request_id, params: dict):
    """
    Find offers around the deliverer (simulated)
    :param dbh: database_handle
    :param request_id: int
    :param params: dict
    :return: json
    """
    
    longitude = int(params["long"])
    latitude = int(params["lat"])
    
    with dbh.cursor() as cursor:
        # Get list
        sql = "SELECT * FROM to_deliver_table WHERE status = %s"
        cursor.execute(sql, (
            "WAITING"
            )
        )
        order_list = cursor.fetchall()[0]
        
    
    return {
        'action' : 'MAP_DELIVERY_AVAILABLE_PICKUPS',
        'message' : {
            'status': 'OK',
            'request': int(request_id),
            'long': longitude,
            'lat': latitude,
            'orders' : order_list
        }
    }