#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime

def notify_delivery(dbh, request_id, params: dict):
    """
    delete from the database the order delivered
    :param dbh: database_handle
    :param request_id: int
    :param params: dict
    :return: void
    """
    id_order = int(params["id_order"])
    with dbh.cursor() as cursor:
        # Get list
        sql = "SELECT pickup_date,id_steed FROM to_deliver_table WHERE id = %s"
        cursor.execute(sql,(
            id_order
            )
        )
        deliver_data = cursor.fetchall()[0]
        id_steed = deliver_data["id_steed"]
        if(deliver_data["id_steed"] == None):
            return
        sql = "SELECT numberOfDelivery, averageTime FROM steed_database WHERE id = %s"
        cursor.execute(sql,(
            id_steed
            )
        )
        steed_data = cursor.fetchall()[0]
        time_pick_up = deliver_data["pickup_date"]
        time_now = datetime.now()
        time = ((time_now.hour * 60) + time_now.minute) - ((time_pick_up.hour * 60)+ time_pick_up.minute)
        sql = "DELETE FROM to_deliver_table WHERE id = %s"
        cursor.execute(sql,(
            id_order
            )
        )
        sql = "UPDATE steed_database SET numberOfDelivery=%s, averageTime=%s WHERE id=%s"
        cursor.execute(sql,(
            steed_data["numberOfDelivery"]+1,
            steed_data["averageTime"] + (time / steed_data["numberOfDelivery"]+1),
            id_steed
            )
        )
    return