#!/usr/bin/env python
# -*- coding: utf-8 -*-
from model.persistent_object import PersistentObject


class Meal(PersistentObject):
    identifier = 0
    parent_category = None

    name = ""
    price = 0.0
    is_menu = False
    image = ""

    def __init__(self, parent_category=None, name="", price=0.0, is_menu=False, image=""):
        PersistentObject.__init__(self)

        if parent_category is None:
            raise ValueError('A meal must be bound to a category !')
        self.parent_category = parent_category

        self.name = name
        self.price = price
        self.is_menu = is_menu
        self.image = image

        # Sync
        self.merge()

    def __resolve_identifier(self):
        if self.identifier < 1:
            with self.database_handle.cursor() as cursor:
                sql = "SELECT idmeal FROM meal WHERE name=%s"
                cursor.execute(sql, self.name)
                if cursor.rowcount > 0:
                    self.identifier = cursor.fetchone()["idmeal"]

    def merge(self):
        self.__resolve_identifier()

        # Update fields
        with self.database_handle.cursor() as cursor:
            if self.identifier > 0:
                # Update
                sql = "UPDATE meal SET idcategory=%s, name=%s, price=%s, is_menu=%s, image=%s WHERE idmeal=%s"
                cursor.execute(sql, (self.parent_category.identifier, self.name, self.price, (0, 1)[self.is_menu], self.image, self.identifier))
            else:
                # Create
                sql = "INSERT INTO meal (idcategory, name, price, is_menu, image) VALUES (%s, %s, %s, %s, %s)"
                cursor.execute(sql, (self.parent_category.identifier, self.name, self.price, (0, 1)[self.is_menu], self.image))
                # Fetch identifier
                self.identifier = cursor.lastrowid

    def delete(self):
        self.__resolve_identifier()

        if self.identifier < 1:
            return

        with self.database_handle.cursor() as cursor:
            sql = "DELETE FROM meal WHERE idmeal=%s"
            cursor.execute(sql, self.identifier)
            self.identifier = 0

    def to_json(self):
        return {
            "id": self.identifier,
            "category": self.parent_category.to_json(),
            "name": self.name,
            "price": self.price,
            "is_menu": self.is_menu,
            "image": self.image
        }

    @staticmethod
    def get_by_name(name):
        meal = Meal(name=name)
        if meal.identifier == 0:
            return None
        return meal
