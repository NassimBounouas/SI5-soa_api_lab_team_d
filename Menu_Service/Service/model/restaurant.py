#!/usr/bin/env python
# -*- coding: utf-8 -*-
from model.persistent_object import PersistentObject


class Restaurant(PersistentObject):
    identifier = 0

    name = ""

    def __init__(self, dbh=None, name=""):
        super().__init__(dbh)

        self.name = name

        # Sync
        self.merge()

    def __resolve_identifier(self):
        if self.identifier < 1:
            with self.database_handle.cursor() as cursor:
                sql = "SELECT idrestaurant FROM restaurant WHERE name=%s"
                cursor.execute(sql, self.name)
                if cursor.rowcount > 0:
                    self.identifier = cursor.fetchone()["idrestaurant"]

    def merge(self):
        self.__resolve_identifier()

        # Update fields
        with self.database_handle.cursor() as cursor:
            if self.identifier > 0:
                # Update
                sql = "UPDATE restaurant SET name=%s WHERE idrestaurant=%s"
                cursor.execute(sql, (self.name, self.identifier))
            else:
                # Create
                sql = "INSERT INTO restaurant (name) VALUES (%s)"
                cursor.execute(sql, (self.name,))
                # Fetch identifier
                self.identifier = cursor.lastrowid

    def delete(self):
        self.__resolve_identifier()

        if self.identifier < 1:
            return

        with self.database_handle.cursor() as cursor:
            sql = "DELETE FROM restaurant WHERE idrestaurant=%s"
            cursor.execute(sql, self.identifier)
            self.identifier = 0

    def to_json(self):
        return {
            "id": self.identifier,
            "name": self.name
        }

    @staticmethod
    def get_by_name(name, dbh):
        restaurant = Restaurant(dbh=dbh, name=name)
        if restaurant.identifier == 0:
            return None
        return restaurant
