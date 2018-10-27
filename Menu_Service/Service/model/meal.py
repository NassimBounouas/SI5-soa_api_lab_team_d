#!/usr/bin/env python
# -*- coding: utf-8 -*-
import hashlib

from model.category import Category
from model.persistent_object import PersistentObject
from model.restaurant import Restaurant


class Meal(PersistentObject):
    identifier = 0
    parent_category = None
    parent_restaurant = None

    name = ""
    price = 0.0
    is_menu = False
    image = ""

    def __init__(self, dbh=None, pk=0, parent_category=None, parent_restaurant=None, name="", price=0.0, is_menu=False, image=""):
        super().__init__(dbh)

        if parent_category is None:
            raise ValueError('A meal must be bound to a category !')
        if parent_restaurant is None:
            raise ValueError('A meal must be bound to a restaurant !')

        self.identifier = pk

        self.parent_category = parent_category
        self.parent_restaurant = parent_restaurant

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
        else:
            # Verify that the record exists
            with self.database_handle.cursor() as cursor:
                sql = "SELECT * FROM meal WHERE idmeal=%s"
                cursor.execute(sql, self.identifier)
                if cursor.rowcount != 1:
                    raise ValueError('Bad meal identifier !')
                # Complete missing attributes
                row = cursor.fetchone()
                if self.parent_category is None:
                    Category.get_by_id(row['idcategory'], self.database_handle)
                if self.parent_restaurant is None:
                    Restaurant.get_by_id(row['idrestaurant'], self.database_handle)
                if len(self.name) == 0:
                    self.name = row['name']
                if self.price == 0.0:
                    self.price = float(row['price'])
                if not self.is_menu:
                    self.is_menu = bool(row['is_menu'])
                if len(self.image) == 0.0:
                    self.image = row['image']

    def merge(self):
        self.__resolve_identifier()

        # Update fields
        with self.database_handle.cursor() as cursor:
            if self.identifier > 0:
                # Update if required
                sql = "SELECT * FROM meal WHERE idmeal=%s"
                cursor.execute(sql, (self.identifier,))
                row = cursor.fetchone()
                # Compute Hash
                b2s = hashlib.blake2s(digest_size=8)
                h = ''
                for attr in row.items():
                    h = h + str(attr[1])
                b2s.update(h.encode('utf-8'))
                fingerprint = b2s.hexdigest()
                if fingerprint != self.hash_id():
                    sql = "UPDATE meal SET idcategory=%s, idrestaurant=%s, name=%s, price=%s, is_menu=%s, image=%s WHERE idmeal=%s"
                    cursor.execute(sql, (self.parent_category.identifier, self.parent_restaurant.identifier, self.name, self.price, (0, 1)[self.is_menu], self.image, self.identifier))
            else:
                # Create
                sql = "INSERT INTO meal (idcategory, idrestaurant, name, price, is_menu, image) VALUES (%s, %s, %s, %s, %s, %s)"
                cursor.execute(sql, (self.parent_category.identifier, self.parent_restaurant.identifier, self.name, self.price, (0, 1)[self.is_menu], self.image))
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
            "restaurant": self.parent_restaurant.to_json(),
            "name": self.name,
            "price": self.price,
            "is_menu": self.is_menu,
            "image": self.image
        }

    def hash_id(self):
        b2s = hashlib.blake2s(digest_size=8)
        h = str(self.identifier) + self.parent_category.hash_id() + self.parent_restaurant.hash_id() + self.name + str(self.price) + str(self.is_menu) + self.image
        b2s.update(h.encode('utf-8'))
        return b2s.hexdigest()
