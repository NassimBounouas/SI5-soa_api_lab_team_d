#!/usr/bin/env python
# -*- coding: utf-8 -*-
from model.category import Category
from model.meal import Meal
from model.persistent_object import PersistentObject
from model.restaurant import Restaurant


class MealCollection(PersistentObject):

    collection = []

    def __init__(self, dbh, category=None, restaurant=None):
        super().__init__(dbh)

        self.collection = []

        with self.database_handle.cursor() as cursor:

            sql = ""

            if category is not None:
                if str(category).isnumeric():
                    category = Category.get_by_id(int(category), self.database_handle)
                else:
                    category = Category.get_by_name(category, self.database_handle)

                if category.identifier > 0:
                    sql = "SELECT * FROM meal WHERE idcategory=%s"
                    cursor.execute(sql, category.identifier)
            elif restaurant is not None:
                if str(restaurant).isnumeric():
                    restaurant = Restaurant.get_by_id(int(restaurant), self.database_handle)
                else:
                    restaurant = Restaurant.get_by_name(restaurant, self.database_handle)

                if restaurant.identifier > 0:
                    sql = "SELECT * FROM meal WHERE idrestaurant=%s"
                    cursor.execute(sql, restaurant.identifier)

            if sql == "":
                sql = "SELECT * FROM meal"
                cursor.execute(sql)

            if cursor.rowcount > 0:
                meals = cursor.fetchall()
                for meal in meals:
                    category = Category.get_by_id(meal["idcategory"], self.database_handle)
                    restaurant = Restaurant.get_by_id(meal["idrestaurant"], self.database_handle)
                    self.collection.append(
                        Meal(
                            dbh=dbh,
                            parent_restaurant=restaurant,
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
