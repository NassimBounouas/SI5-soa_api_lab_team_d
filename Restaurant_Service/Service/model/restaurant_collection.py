#!/usr/bin/env python
# -*- coding: utf-8 -*-
from model.persistent_object import PersistentObject
from model.restaurant import Restaurant


class RestaurantCollection(PersistentObject):

    def __init__(self, dbh):
        super().__init__(dbh)

        self.collection = []

        with self.database_handle.cursor() as cursor:
            sql = "SELECT * FROM restaurant"
            cursor.execute(sql)
            if cursor.rowcount > 0:
                restaurants = cursor.fetchall()
                for restaurant in restaurants:
                    self.collection.append(
                        Restaurant(
                            dbh=dbh,
                            name=restaurant["name"]
                        )
                    )

    def to_json(self):
        json = []
        for restaurant in self.collection:
            json.append(restaurant.to_json())
        return json
