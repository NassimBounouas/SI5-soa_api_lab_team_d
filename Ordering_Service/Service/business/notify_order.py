#!/usr/bin/env python
# -*- coding: utf-8 -*-

def notify_order(dbh, request_id, params: dict):
    """
    update the database of order
    :param dbh: database_handle
    :param request_id: int
    :param params: dict
    :return: void
    """
    id_order = params["id_order"]
    with dbh.cursor() as cursor:
        #Get list
        sql = "UPDATE `order` SET status=%s WHERE id_order=%s AND status=%s"
        cursor.execute(sql,(
            "Delivered",
            id_order,
            "Accepted"
            )
        )
    return