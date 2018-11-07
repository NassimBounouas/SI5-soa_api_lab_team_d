#!/usr/bin/env python
# -*- coding: utf-8 -*-

def send_steed_status(dbh, request_id, params: dict):
    id_steed = int(params["id_steed"])
    with dbh.cursor() as cursor:
        sql = "UPDATE to_deliver_table SET status=%s, id_steed=%s WHERE id_steed=%s"
        cursor.execute(sql,(
            "WAITING",
            None,
            id_steed
            )
        )
    return