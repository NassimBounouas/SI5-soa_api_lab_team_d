#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime

def delivery_location(dbh, request_id, params: dict):
    """
    update steed localisation in steed database
    :param dbh: database_handle
    :param request_id: int
    :param params: dict
    :return: void
    """
    id_steed = int(params["id_steed"])
    id_order = int(params["id_order"])
    longitude = int(params["longitude"])
    latitude = int(params["latitude"])
    lastupdate = datetime.now()
    with dbh.cursor() as cursor:
        # Get list
        sql = "UPDATE steed_database SET latitude = %s, longitude = %s, lastUpdate = %s WHERE id = %s"
        cursor.execute(sql,(
            longitude,
            latitude,
            lastupdate,
            id_steed
            )
        )
        sql = "UPDATE to_deliver_table SET status=%s ,id_steed=%s WHERE id =%s AND status=%s"
        cursor.execute(sql,(
            "DELIVERING",
            id_steed,
            id_order,
            "WAITING"
            )
        )
    return

def get_delivery_location(dbh,request_id, params: dict):
    """
    return the last position of the steed
    :param dbh: database_handle
    :param request_id: int
    :param params: dict
    :return: json
    """
    id_order = int(params["id_order"])
    with dbh.cursor() as cursor:
        sql= "SELECT id_steed FROM to_deliver_table WHERE id = %s"
        cursor.execute(sql,(
            id_order
        ))
        res = cursor.fetchall()[0]
        sql = "SELECT latitude, longitude,lastUpdate FROM steed_database WHERE id = %s"
        cursor.execute(sql,(
            res["id_steed"]
            )
        )
        res = cursor.fetchall()[0]
    return {
        'action': 'DELIVERY_LOCATION_STATUS',
        'message': {
            'status': 'OK',
            'request': int(request_id),
            'latitude': res["latitude"],
            'longitude' : res["longitude"],
            'timestamp' : str(res["lastUpdate"])
        }
    }