#!/usr/bin/env python
# -*- coding: utf-8 -*-

def steed_stat_request(dbh, request_id, params: dict):
    id_steed = int(params["id_steed"])
    with dbh.cursor() as cursor:
        sql = "SELECT numberOfDelivery,averagePay,averageTime FROM steed_database WHERE id=%s"
        cursor.execute(sql,(
            id_steed
            )
        )
        res = cursor.fetchall()[0]
    return {
        'action': 'DELIVERY_STAT_RESPONSE',
        'message': {
            'status': 'OK',
            'request': int(request_id),
            'value' :{
                'average_pay':res['averagePay'],
                'average_time':res['averageTime'],
                'number_of_Delivery':res['numberOfDelivery']
            }
        }
    }