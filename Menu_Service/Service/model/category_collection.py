#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import g
from model.category import Category


class CategoryCollection:

    def __init__(self):
        self.collection = []

        with g.database_handle.cursor() as cursor:
            sql = "SELECT * FROM category"
            cursor.execute(sql)
            if cursor.rowcount > 0:
                categories = cursor.fetchall()
                for category in categories:
                    self.collection.append(
                        Category(
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
