#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random


def map_delivery(dbh, request_id, params: dict):
    """
    Find offers around the deliverer (simulated)
    :param dbh: database_handle
    :param request_id: int
    :param params: dict
    :return: json
    """

    r = 3
    res =[]
    longitude = float(params["long"])
    latitude = float(params["lat"])
    rest_gps = dict()
    with dbh.cursor() as cursor:
        # Get list
        sql = "SELECT delivery_address, meal_name, id, pickup_restaurant FROM to_deliver_table WHERE status = %s"
        cursor.execute(sql, (
            "WAITING"
            )
        )
        order_list = cursor.fetchall()
        #mock the restaurant position in a dict
        for order in order_list:
            name = str(order["pickup_restaurant"])
            if name not in rest_gps:
                long = random.uniform(-50.0,50.0)
                lat = random.uniform(-50.0,50.0)
                rest_gps[name] = [long,lat]
            gps = rest_gps[name]
            #if stted within the range 3km, then ok
            if ((latitude - r/111) < gps[1]) and ((latitude + r/111) > gps[1]) and ((longitude - r/76) < gps[0]) and ((longitude + r/76) > gps[0]):
                order['gps'] = gps
                res.append(order)
    return {
        'action' : 'MAP_DELIVERY_AVAILABLE_PICKUPS',
        'message' : {
            'status': 'OK',
            'request': int(request_id),
            'orders' : res
        }
    }