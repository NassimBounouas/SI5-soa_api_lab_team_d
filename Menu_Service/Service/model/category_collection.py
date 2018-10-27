#!/usr/bin/env python
# -*- coding: utf-8 -*-
from model.category import Category
from model.persistent_object import PersistentObject


class CategoryCollection(PersistentObject):

    def __init__(self, dbh):
        super().__init__(dbh)

        self.collection = []

        with self.database_handle.cursor() as cursor:
            sql = "SELECT * FROM category"
            cursor.execute(sql)
            if cursor.rowcount > 0:
                categories = cursor.fetchall()
                for category in categories:
                    self.collection.append(
                        Category(
                            dbh=dbh,
                            name=category["name"],
                            region=category["region"],
                            image=category["image"]
                        )
                    )

    def to_json(self):
        json_categories = []
        for category in self.collection:
            json_categories.append(category.to_json())
        return json_categories
