#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import g
from model.category import Category
from model.meal import Meal


class MealCollection:

    collection = []

    def __init__(self, category_name=""):
        self.collection = []

        with g.database_handle.cursor() as cursor:
            category = Category.get_by_name(category_name)
            if category.identifier > 0:
                sql = "SELECT * FROM meal WHERE idcategory=%s"
                cursor.execute(sql, category.identifier)
            else:
                sql = "SELECT * FROM meal"
                cursor.execute(sql)
            if cursor.rowcount > 0:
                meals = cursor.fetchall()
                for meal in meals:
                    self.collection.append(
                        Meal(
                            parent_category=category,
                            name=meal["name"],
                            price=meal["price"],
                            is_menu=(meal["is_menu"] > 0),
                            image=meal["image"]
                        )
                    )

    def to_json(self):
        json_meals = []
        for meal in self.collection:
            json_meals.append(meal.to_json())
        return json_meals